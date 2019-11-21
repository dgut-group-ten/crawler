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

    cookies = {
        'MUSIC_U': '57c8ae96cd9b39c040d202796af65095e20f265fe0331c2e4ebc806beab2e4306ff9017ffeaf64b87220854add29623541049cea1c6bb9b6',
        '__csrf': 'a2f3983c5c848b7638c7dfbc3a2fd536',
        '__remember_me': 'true',
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.PlayListPipeline': 200,
            'crawler.pipelines.SongPipeline': 200,
            # 'crawler.pipelines.CrawlerPipeline': 300,
        },
        'DOWNLOAD_DELAY': 1,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, cookies=self.cookies)

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
            music_list_item['lid'] = playlist['id']
            music_list_item['name'] = playlist['name']
            music_list_item['description'] = playlist['description']
            music_list_item['tags'] = playlist['tags']

            url = self.base_url + api.format(playlists_id=playlist['id'])
            yield scrapy.Request(url, callback=self.parse_playlist, meta={'lid': playlist['id']})
            yield music_list_item

    def parse_playlist(self, response):
        """
        获取歌单详情
        :param response:
        :return:
        """
        tracks = json.loads(response.text)['playlist']['tracks']
        api = "/song/url?id={m_id}"
        lid = response.meta.get('lid')

        for music in tracks:
            music_item = MusicItem()
            music_item['lid'] = lid
            music_item['sid'] = music['id']
            music_item['name'] = music['name']
            music_item['author'] = music['ar']
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
