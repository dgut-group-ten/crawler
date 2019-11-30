# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import uuid

import pymongo
import requests

from .items import MusicItem, MusicListItem

from crawler.tool import sftp_upload


class CoverImagePipeline(object):
    def process_item(self, item, spider):
        ext = item['url'].split('.')[-1]
        new_filename = uuid.uuid4().hex + '.' + ext
        with open('tmp/' + new_filename, 'wb') as f:
            f.write(requests.get(url=item['url']).content)

        headers = {
            "Token": 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjEsIndlYiI6Imdyb3VwdGVuIiwiZXhwIjoxNTc1NzEwMzgxLCJpYXQiOjE1NzUxMDU1ODF9._8tPWLBIb_CcYzJoAthkmCt8GP-Upm8plPW7BsA_3s0'
        }

        url = "https://music-02.niracler.com:8000/playlist/" + str(item['id']) + '/'
        try:
            files = {'cimg': open('tmp/' + new_filename, 'rb')}
            r = requests.patch(url, files=files, headers=headers)
            os.remove('tmp/' + new_filename)
            print(r.text)
        except Exception as e:
            print(str(e))

        return item


class PlayListPipeline(object):
    def process_item(self, item, spider):

        if isinstance(item, MusicListItem):
            url = "https://music-02.niracler.com:8000/playlist/"
            data = {
                "lid": item['lid'],
                "name": item['name'],
                'stags': ' '.join(item['tags']),
                "description": item['description'],
            }
            print(data)

            try:
                r = requests.post(url, data=data)
                print(r.text)
            except Exception as e:
                print(str(e))

        return item


class SongPipeline(object):
    def process_item(self, item, spider):

        if isinstance(item, MusicItem) and item['url']:

            author_list = []

            # 添加作者
            for author in item['author']:
                url = "https://music-02.niracler.com:8000/author/"
                data = {
                    "aid": author['id'] if author['id'] else 1,
                    "name": author['name'] if author['id'] else '神秘歌手(没有ID)',
                }
                try:
                    r = requests.post(url, data=data).json()
                    print(r)
                    author_list.append(data['aid'])
                    print(author_list)
                except Exception as e:
                    print("作者创建有问题：" + str(e))

            # 上传文件
            ext = item['url'].split('.')[-1]
            new_filename = uuid.uuid4().hex + '.' + ext
            with open('tmp/' + new_filename, 'wb') as f:
                f.write(requests.get(url=item['url']).content)

            url = "https://music-02.niracler.com:8000/song/"
            url2 = "https://music-02.niracler.com:8000/playlist/" + str(item['lid']) + '/'
            data = {
                "sid": item['sid'],
                "name": item['name'],
                "authors": author_list,
            }
            try:
                files = {'file': open('tmp/' + new_filename, 'rb')}
                r = requests.post(url, files=files, data=data)
                os.remove('tmp/' + new_filename)
                print(r.text)
                r = requests.put(url2, data={'tracks': [item['sid']]})
                print(r.text)
            except Exception as e:
                print(str(e))

        return item


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_SERVER'),
            mongo_db=crawler.settings.get('MONGODB_DB', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

        if spider.custom_settings and spider.custom_settings.get('MONGODB_COLLECTION'):
            self.collection = spider.custom_settings.get('MONGODB_COLLECTION')
        else:
            self.collection = spider.settings['MONGODB_COLLECTION']
        self.db[self.collection].create_index(spider.item_index, unique=True)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection].insert_one(dict(item))
        return item


class ImgDownloadPipeline(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
    }

    def process_item(self, item, spider):
        img_url = item['img_url']
        img_path = item['img_path']

        with open('.' + img_path, 'wb') as f:
            f.write(requests.get(url=img_url, headers=self.headers).content)

        host = 'test.niracler.com'  # 主机
        port = 22  # 端口
        username = 'niracler'  # 用户名
        password = '159258'  # 密码
        local = '.' + img_path  # 本地文件或目录，与远程一致，当前为windows目录格式，window目录中间需要使用双斜线
        remote = '/home/niracler/PycharmProjects/display-back-end' + img_path  # 远程文件或目录，与本地一致，当前为linux目录格式
        sftp_upload(host, port, username, password, local, remote)  # 上传

        return item
