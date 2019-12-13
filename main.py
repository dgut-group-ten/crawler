import sys
import os

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

for i in ['华语','新番']:
    execute(['scrapy', 'crawl', 'playlist', '-a', 'keyword='+i])