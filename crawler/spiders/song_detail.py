import scrapy
import json

from crawler.items import ImgItem, SongDetailItem
from crawler.spiders.song_id import SONG_LIST


class SongDetailSpider(scrapy.Spider):
    name = 'song_detail'
    allowed_domains = ['music-01.niracler.com']
    base_url = 'https://music-01.niracler.com:8003/song/detail?ids='
    start_urls = []

    def __init__(self):
        super().__init__()
        for sid in SONG_LIST.split('\n'):
            self.start_urls.append(self.base_url + sid)

    cookies = {
        'MUSIC_U': '57c8ae96cd9b39c040d202796af65095e20f265fe0331c2e4ebc806beab2e4306ff9017ffeaf64b87220854add29623541049cea1c6bb9b6',
        '__csrf': 'a2f3983c5c848b7638c7dfbc3a2fd536',
        '__remember_me': 'true',
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            # 'crawler.pipelines.CoverImagePipeline': 200,
            'crawler.pipelines.SongDetailPipeline': 200,
            # 'crawler.pipelines.CrawlerPipeline': 300,
        },
        'DOWNLOAD_DELAY': 0,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, cookies=self.cookies)

    def parse(self, response):
        item = SongDetailItem()

        data = json.loads(response.text)
        item['id'] = response.url.split('=')[-1]
        item['cover_url'] = data['songs'][0]['al']['picUrl']
        item['cover_name'] = data['songs'][0]['al']['name']
        yield item
