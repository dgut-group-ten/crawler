# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import uuid

import requests

from .items import SongItem, PlaylistItem

headers = {
    "Token": 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI1LCJ3ZWIiOiJncm91cHRlbiIsIm5hbWUiOiJyb290IiwiaXNBZG1pbiI6ZmFsc2UsImV4cCI6MTU3Njc1NjAzMSwiaWF0IjoxNTc2MTUxMjMxfQ.VkGwJbnohxGwM6ojlM3T0z-1h5y3RHZ7CFdCoZZq1Hk'
}


class PlaylistPipeline(object):
    """关于歌单的数据存储类"""

    def process_item(self, item, spider):

        if isinstance(item, PlaylistItem):
            # 下载封面
            ext = item['cover_url'].split('.')[-1]
            new_filename = uuid.uuid4().hex + '.' + ext
            with open('tmp/' + new_filename, 'wb') as f:
                f.write(requests.get(url=item['cover_url']).content)
            files = {'cimg': open('tmp/' + new_filename, 'rb')}

            # 装好data
            url = "https://music-01.niracler.com:8002/playlist/"
            data = {
                "lid": item['lid'],
                "name": item['name'],
                'stags': item['stags'],
                "description": item['description'],
            }

            try:
                r = requests.post(url, files=files, data=data, headers=headers)
                os.remove('tmp/' + new_filename)
                print(r.text)
            except Exception as e:
                print(str(e))

        return item


class LyricPipeline(object):
    def process_item(self, item, spider):

        headers = {
            "Token": 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI1LCJ3ZWIiOiJncm91cHRlbiIsIm5hbWUiOiJyb290IiwiaXNBZG1pbiI6ZmFsc2UsImV4cCI6MTU3NjEzMjg3MywiaWF0IjoxNTc1NTI4MDczfQ.Vo-uGd4wVadUvKEI27WSGQ68Gj_XuVVy-2IR_LuNZ6o'
        }

        url = "https://music-01.niracler.com:8002/song/" + str(item['id']) + '/'
        try:
            data = {'lyric': item['lyric']}
            r = requests.patch(url, data=data, headers=headers)
            print(r.text)
        except Exception as e:
            print(str(e))

        return item


class SongPipeline(object):
    def process_item(self, item, spider):

        if isinstance(item, SongItem) and item['url']:

            author_list = []

            # 添加作者
            for author in item['author']:
                url = "https://music-01.niracler.com:8002/author/"
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

            # 上传音乐文件
            ext = item['url'].split('.')[-1]
            song_file = uuid.uuid4().hex + '.' + ext
            with open('tmp/' + song_file, 'wb') as f:
                f.write(requests.get(url=item['url']).content)

            # 上传封面
            ext = item['cover_url'].split('.')[-1]
            cover_file = uuid.uuid4().hex + '.' + ext
            with open('tmp/' + cover_file, 'wb') as f:
                f.write(requests.get(url=item['cover_url']).content)

            files = {
                'file': open('tmp/' + song_file, 'rb'),
                'cimg': open('tmp/' + cover_file, 'rb')
            }

            data = {
                "sid": item['sid'],
                "name": item['name'],
                "authors": author_list,
                'lyric': item['lyric'],
            }

            song_url = "https://music-01.niracler.com:8002/song/"
            playlist_url = "https://music-01.niracler.com:8002/playlist/" + str(item['lid']) + '/'
            try:
                r = requests.post(song_url, headers=headers, files=files, data=data)
                os.remove('tmp/' + song_file)
                os.remove('tmp/' + cover_file)
                print(r.text)
                r = requests.patch(playlist_url, headers=headers).json()
                tracks = r['tracks']
                tracks.append(int(item['sid']))
                r = requests.patch(playlist_url, headers=headers, data={'tracks': tracks})
                print(r.text)
            except Exception as e:
                print(str(e))

        return item


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item
