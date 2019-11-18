# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import requests

from sqlalchemy.orm import sessionmaker
from .models import db_connect, create_table, Music, MusicList
from .items import MusicItem, MusicListItem

from crawler.tool import sftp_upload


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class MusicPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        Save deals in the database.
        This method is called for every item pipeline component.
        """
        session = self.Session()

        if isinstance(item, MusicItem):
            music = Music()
            music.name = item['name']
            music.url = item['url']
            someone = music
        else:
            music_list = MusicList()
            music_list.name = item['name']
            music_list.description = item['description']
            someone = music_list

        try:
            session.add(someone)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

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
