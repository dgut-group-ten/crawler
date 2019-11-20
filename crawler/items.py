# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MusicListItem(scrapy.Item):
    name = scrapy.Field()  # 歌单名称
    description = scrapy.Field()  # 歌单描述


class MusicItem(scrapy.Item):
    name = scrapy.Field()  # 歌曲名称
    url = scrapy.Field()  # 歌曲文件链接
    author = scrapy.Field()  # 歌曲作者
