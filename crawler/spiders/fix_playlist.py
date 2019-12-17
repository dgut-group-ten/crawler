import scrapy
import json

from .id import PLAYLIST_ID
from crawler.items import SongItem


class PlaylistSpider(scrapy.Spider):
    """爬取歌单的爬虫"""
    name = 'fix_playlist'
    allowed_domains = ['music-01.niracler.com']
    base_url = 'https://music-01.niracler.com:8003'
    start_urls = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for playlist_id in PLAYLIST_ID.split('\n'):
            self.start_urls.append(self.base_url + '/playlist/detail?id=' + playlist_id)

    # 一些简单配置
    cookies = {
        'MUSIC_U': '57c8ae96cd9b39c040d202796af650952db10f015768aa4cd303749029ea7d4b4a82978769a9fb0e6ccf8908efc73cd741049cea1c6bb9b6',
        '__csrf': '4770668dc6cfc7a340f5b2f52586e2ac',
        '__remember_me': 'true',
        'csrftoken': 'iQFvdai1lXkAa5GwSB49inmGTta1YKShEzSXkIshNFguDNmt6HFCd1UeJuGi3aMI',
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    custom_settings = {
        'ITEM_PIPELINES': {
            # 'crawler.pipelines.PlaylistPipeline': 200,
            'crawler.pipelines.FixSongAreaPipeline': 200,
            # 'crawler.pipelines.CrawlerPipeline': 300,
        },
        'DOWNLOAD_DELAY': 0.01,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_playlist, cookies=self.cookies, headers=self.headers)

    def parse_playlist(self, response):
        music_data = json.loads(response.text)
        playlist = music_data['playlist']

        lid = response.url.split('=')[-1]
        area_list = ["华语", "欧美", "日语", "韩语", "粤语", "英伦", "拉丁"]
        area = '未知'
        for i in playlist['tags']:
            if i in area_list:
                area = i
                print(area)
                break

        api = "/song/url?id={sid}"

        for song in playlist['tracks']:
            song_item = SongItem()
            song_item['lid'] = lid
            song_item['sid'] = song['id']
            song_item['name'] = song['name']
            song_item['author'] = song['ar']
            song_item['cover_url'] = song['al']['picUrl']
            song_item['area'] = area
            # url = self.base_url + api.format(sid=song_item['sid'])
            yield song_item
            # yield scrapy.Request(url, callback=self.parse_song, meta={'song_item': song_item})

    def parse_song(self, response):
        """
        获取歌曲详情
        :param response:
        :return:
        """
        song_item = response.meta.get('song_item')
        song = json.loads(response.text)
        song_item['url'] = song['data'][0]['url']

        api = "/lyric?id={sid}"
        url = self.base_url + api.format(sid=song_item['sid'])
        yield scrapy.Request(url, callback=self.parse_song_detail, meta={'song_item': song_item})

    def parse_song_detail(self, response):
        data = json.loads(response.text)
        song_item = response.meta.get('song_item')

        lrc = data.get('lrc', '')
        if lrc:
            song_item['lyric'] = lrc['lyric']
        else:
            song_item['lyric'] = ''

        yield song_item
