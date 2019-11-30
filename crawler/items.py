# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImgItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()


class MusicListItem(scrapy.Item):
    lid = scrapy.Field()  # 歌单ID
    name = scrapy.Field()  # 歌单名称
    description = scrapy.Field()  # 歌单描述
    tags = scrapy.Field()  # 歌单标签
    tracks = scrapy.Field()  # 歌单列表


class MusicItem(scrapy.Item):
    lid = scrapy.Field()
    sid = scrapy.Field()
    name = scrapy.Field()  # 歌曲名称
    url = scrapy.Field()  # 歌曲文件链接
    author = scrapy.Field()  # 歌曲作者
