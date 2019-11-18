# -*- coding: utf-8 -*-
import re

import scrapy
import json
from crawler.items import MusicListItem, MusicItem


class MusicSpider(scrapy.Spider):
    name = 'music'
    allowed_domains = ['music-03.niracler.com']
    base_url = "https://music-03.niracler.com:3000"
    start_urls = [base_url + '/top/playlist/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.MusicPipeline': 200,
            'crawler.pipelines.CrawlerPipeline': 300,
        },
        'DOWNLOAD_DELAY': 0,
    }

    def parse(self, response):
        """
        获取歌单列表
        :param response:
        :return:
        """
        music_data = json.loads(response.text)
        playlists = music_data['playlists']
        api = "/playlist/detail?id={playlists_id}"

        for playlist in playlists:
            music_list_item = MusicListItem()
            music_list_item['name'] = playlist['name']
            music_list_item['description'] = playlist['description']

            url = self.base_url + api.format(playlists_id=playlist['id'])
            # yield music_list_item
            yield scrapy.Request(url, callback=self.parse_playlist)

    def parse_playlist(self, response):
        """
        获取歌单详情
        :param response:
        :return:
        """
        tracks = json.loads(response.text)['playlist']['tracks']
        api = "/song/url?id={m_id}"

        for music in tracks:
            music_item = MusicItem()
            music_item['name'] = music['name']
            url = self.base_url + api.format(m_id=music['id'])
            yield scrapy.Request(url, callback=self.parse_music, meta={'music_item': music_item})

    def parse_music(self, response):
        """
        获取歌曲详情
        :param response:
        :return:
        """
        music_item = response.meta.get('music_item')
        music = json.loads(response.text)
        music_item['url'] = music['data'][0]['url']
        yield music_item
