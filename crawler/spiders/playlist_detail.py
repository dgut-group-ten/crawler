import scrapy
import json

from crawler.items import ImgItem


class MusicSpider(scrapy.Spider):
    name = 'playlist_detail'
    allowed_domains = ['music-03.niracler.com']
    base_url = 'https://music-03.niracler.com:3000/playlist/detail?id='
    start_urls = []
    cur_list = """473759386
481244653
2661580078
2789240978
2829896389
2830604597
2855535857
2861954696
2877097132
2878457256
2889745179
2891313765
2896071794
2899590484
2902135655
2909851267
2915714851
2916766519
2917057835
2925617418
2928393485
2928657214
2929507163
2935597926
2936140764
2939385580
2945759243
2949990721
2950506211
2951533381
2952865222
2953539393
2956668896
2958513795
2958576939
2960261959
2980381668
2995109119
2995540436
2997315097
2997849735
2999999790
3002117558
3004447275
3005581883
3007752099
3011016131
3030771064
3036630431
3042446515"""

    def __init__(self):
        super().__init__()
        for lid in self.cur_list.split('\n'):
            self.start_urls.append(self.base_url + lid)

    cookies = {
        'MUSIC_U': '57c8ae96cd9b39c040d202796af65095e20f265fe0331c2e4ebc806beab2e4306ff9017ffeaf64b87220854add29623541049cea1c6bb9b6',
        '__csrf': 'a2f3983c5c848b7638c7dfbc3a2fd536',
        '__remember_me': 'true',
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.CoverImagePipeline': 200,
            # 'crawler.pipelines.SongPipeline': 200,
            # 'crawler.pipelines.CrawlerPipeline': 300,
        },
        'DOWNLOAD_DELAY': 1,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, cookies=self.cookies)

    def parse(self, response):

        music_data = json.loads(response.text)
        playlist = music_data['playlist']

        item = ImgItem()
        item['id'] = response.url.split('=')[-1]
        item['url'] = playlist['coverImgUrl']

        yield item
