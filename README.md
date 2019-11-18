# crawler
> 

## 如何团队项目保持同步(重要)

- 第一次时需要,与团队仓库建立联系

```
git remote add upstream https://github.com/ghost-of-fantasy/crawler.git
```

- 工作前后要运行这几条命令,和团队项目保持同步

```
git fetch upstream
git merge upstream/master
```

## 安装并进行单机测试

### 安装依赖包

```sh
pip install --upgrade pip

pip install -r requirements.txt
```

### 尝试运行程序

```bash
scrapy crawl shenshe
```


### 打包命令
```bash
$ cd ..
$ tar -czvf crawler.tar.gz  --exclude=crawler/venv --exclude=crawler/media --exclude=crawler/.git crawler
```

## 参考文章

- [scrapy-redis](https://github.com/rmax/scrapy-redis)
- [小白进阶之Scrapy第三篇（基于Scrapy-Redis的分布式以及cookies池）](https://cuiqingcai.com/4048.html)
- [如何简单高效地部署和监控分布式爬虫项目](https://juejin.im/post/5bebc5fd6fb9a04a053f3a0e)
- [news-please](https://github.com/fhamborg/news-please)
- [who did what, when, where, why, and how?](https://github.com/fhamborg/Giveme5W1H)
- [台湾新闻爬虫](https://github.com/TaiwanStat/Taiwan-news-crawlers)
- [基于给定事件关键词，采集事件资讯，对事件进行挖掘和分析。](https://github.com/liuhuanyong/EventMonitor)
- [An array field in scrapy.Item](https://stackoverflow.com/questions/29227119/an-array-field-in-scrapy-item)
- [Scrapy 使用写死的cookie 来爬需要登录的页面](https://blog.csdn.net/fox64194167/article/details/79775301)
- [新浪微博爬虫，用python爬取新浪微博数据](https://github.com/dataabc/weiboSpider)
- [scrapy爬取新浪微博+cookie池](https://blog.csdn.net/m0_37438418/article/details/80819847)
- [How to set a primary key in MongoDB?](https://stackoverflow.com/questions/3298963/how-to-set-a-primary-key-in-mongodb)
- [Logging](https://docs.scrapy.org/en/latest/topics/logging.html)
- [settings](https://docs.scrapy.org/en/latest/topics/settings.html)
- [item-pipeline](https://docs.scrapy.org/en/latest/topics/item-pipeline.html)
- [使用 privoxy 转发 socks 到 http ](http://einverne.github.io/post/2018/03/privoxy-forward-socks-to-http.html)
- [Make Scrapy work with socket proxy](https://blog.michaelyin.info/scrapy-socket-proxy/)
- [Python向redis批量插入数据](https://my.oschina.net/tigerBin/blog/1842895)