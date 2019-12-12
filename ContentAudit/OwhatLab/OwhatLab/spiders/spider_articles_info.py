# -*- coding: utf-8 -*-
import scrapy
import json

import time


from OwhatLab.conf.configure import *
from OwhatLab.utils.myredis import RedisClient
from OwhatLab.items import OwhatLabArticleItem, OwhatLabUserIterm


class SpiderArticlesInfoSpider(scrapy.Spider):
    name = 'spider_articles_info'
    allowed_domains = ['appo4.owhat.cn']
    start_urls = ['http://appo4.owhat.cn/']

    # 首页url：PreUrl + listMainUrl
    PreUrl = "https://appo4.owhat.cn/api?"
    # jalouse频道首页--该频道只有一个用户user_id=8244418,s所以无需遍历整个list直接赋值user_id即可

    flag1 = 0

    # 用户详情页--文章类信息url,各个频道相同：
    #ArticleMainUrl = "apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m=home&cmd_s=userindex&data=%7B%22userid%22%3A{}%2C%22tabtype%22%3A2%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575256658.578629&v=1.0"
    # "apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m=home&cmd_s=userindex&data=%7B%22userid%22%3A%228244418%22%2C%22tabtype%22%3A2%2C%22pagenum%22%3A%221%22%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575283078.534425&v=1.0"


  #爬虫步骤： 先对具体某个频道的主页url进入找到内容list，每页显示20条，可以翻页展示-----再对list中的每一项找到对应的user_id-------然后在ArticleMainUrl中传入user_id参数，抓取该用户的全部文章信息
    def __init__(self):
        # connect redis
        self.redisClient = RedisClient.from_settings(DB_CONF_DIR)
        new_CHANNEL_CONF = json.dumps(CHANNEL_CONF)
        self.redisClient.put("CHANNEL_CONF", new_CHANNEL_CONF, None, False)
        self.article_set_key = REDIS_KEY['article_id']

        channelJsonStr = self.redisClient.get("CHANNEL_CONF", -1)
        self.channelDict = json.loads(channelJsonStr)
        #print(self.channelDict)
        print('Owhat文章信息爬虫开始...')

    def start_requests(self):
        for value in self.channelDict.values():
            if  value['itemIndex'] in  ['1','2','9','10','11','12']:
                self.flag1 = 1
                curPage = 1
                cmd_m = value['cmd_m']
                cmd_s = value['cmd_s']
                itemIndex = value['itemIndex']
                columnid = str(value['columnid'])
                apiv = value['apiv']

                while curPage > 0 and self.flag1 == 1  and curPage < 81:
                    # print('curPage:', curPage)
                    print('文章信息抓取：正在抓取itemIndex={}，频道={}，第{}页内容...'.format(itemIndex, columnid, curPage))
                    if itemIndex == '2':
                        tempUrl = apiv.format(cmd_m, cmd_s, itemIndex, columnid, curPage)
                    else:
                        tempUrl = apiv.format(cmd_m, cmd_s, columnid, itemIndex, curPage)
                    curPage += 1
                    listUrl = self.PreUrl + tempUrl
                    #print('文章信息抓取listUrl：', listUrl)
                    time.sleep(5)
                    yield scrapy.Request(listUrl, method='POST',  # headers=self.headers,
                                        callback=self.parseListUrl)
            else:
                    continue

    def parseListUrl(self, response):
        # print(response.text)
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        content = rltJson['data']
        if content == "":
            print('get list interface error: ' + response.text)
            return
        videoList = content['list']  #返回值是一个数组
        #print('videoList内容：', videoList)
        if len(videoList) > 0:
            for videoInfo in videoList:
                if 'articlestatus' in videoInfo:
                    #print('videoInfo:',videoInfo)
                    article_id = videoInfo['entityid']
                    #print(article_id)
                    flag = self.redisClient.sismember(self.article_set_key, article_id)
                    if flag == 1:
                        #print('该文章信息已爬虫，不再重复爬取')
                        continue
                    else:
                        self.redisClient.sadd(self.article_set_key, article_id)
                        yield self.getArticleInfoItem(videoInfo)  # 此处yield函数不可少
                else:
                    continue
        else:
            #print('该频道主页内容的文章爬虫已完毕！')
            self.flag1 = 0
            return




    def getArticleInfoItem(self, article):
        articleItem = OwhatLabArticleItem()

        if 'entityid' in  article:
            articleItem['article_id'] = article['entityid']
        if 'publishtime' in  article:
            articleItem['publish_time'] = str(article['publishtime'])[0:10]
        if 'title' in  article:
            articleItem['title'] = article['title']
        if 'entityimgurl' in  article:
            articleItem['article_imgurl'] = article['entityimgurl']
        if 'columnid' in  article:
            articleItem['column_id'] = article['columnid']
        if 'columnname' in  article:
            articleItem['column_name'] = article['columnname']
        if 'publisherid' in article:
            articleItem['publisher_id'] = article['publisherid']
        if 'publishername' in article:
            articleItem['publisher_name'] = article['publishername']
        if 'publisheravatarimg' in article:
            articleItem['publisher_pic_url'] = article['publisheravatarimg']

        if 'columnid' not in article:
            articleItem['column_id'] = "未知"
        if 'columnname' not in article:
            articleItem['column_name'] = "未知"

        articleItem['update_time'] = time.time()

        print('articleItem：', articleItem)

        return articleItem  # 此处必须用return返回

