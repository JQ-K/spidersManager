# -*- coding: utf-8 -*-
import scrapy
import json
import time

from RongCloudChannel.items import ContentItem
from RongCloudChannel.items import AccountItem

class BaijiahaoSpider(scrapy.Spider):
    name = 'BaiJiaHao'
    contentStartUrl = "https://baijiahao.baidu.com/builder/article/lists?type=&collection=&pageSize=10&currentPage={}&search=&app_id=1639272210762362&dynamic=1"
    fansInfoUrl = "https://baijiahao.baidu.com/builder/author/statistic/getFansBasicInfo"

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    cookies = {
        'BDUSS': 'VdlWHNWd0t0a1Q3ZH5odU1GWkRYeXhBfjA4WEpFall0aTVRbDJ2ZWpWRmdBT0pkSVFBQUFBJCQAAAAAAAAAAAEAAAAz910NxOq44rO0w-bM9QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGBzul1gc7pdN'
    }


    def __init__(self):
        self.currentPage = 1
        self.totalPage = 1
        self.beginFlag = True


    def start_requests(self):
        yield scrapy.Request(self.fansInfoUrl,
                             callback=self.parseFansInfoPageJson, method='GET', headers=self.headers, cookies=self.cookies)
        yield scrapy.Request(self.contentStartUrl.format(self.currentPage),
                             callback=self.parseContentPageJson, method='GET', headers=self.headers, cookies=self.cookies)


    def parseFansInfoPageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        accountItem = AccountItem()
        accountItem['channel_id'] = "百家号"
        accountItem['account_id'] = "13656689260"   #######test
        accountItem['record_class'] = "channel_info"
        accountItem['crawl_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        accountItem['new_fans_count'] = rltJson['data']['new_fans']['new_fans_count']
        accountItem['cancel_fans_count'] = rltJson['data']['rm_fans']['rm_fans_count']
        yield accountItem

    def parseContentPageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        if self.beginFlag:
            self.totalPage = rltJson['data']['page']['totalPage']
            self.beginFlag = False

        contentList = rltJson['data']['list']
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #print(len(contentList))
        for contentInfo in contentList:
            contentItem = ContentItem()
            contentItem['channel_id'] = "百家号"
            contentItem['account_id'] = "13656689260"  #######test
            contentItem['record_class'] = "content_info"
            contentItem['crawl_time'] = curTime
            contentItem['id'] = contentInfo['id']
            contentItem['content_link'] = contentInfo['url']
            contentItem['publish_time'] = contentInfo['publish_time']
            contentItem['publish_status'] = contentInfo['status']
            contentItem['audit_result'] = contentInfo['audit_msg']
            contentItem['read_count'] = contentInfo['read_amount']
            contentItem['comment_count'] = contentInfo['comment_amount']
            contentItem['share_count'] = contentInfo['share_amount']
            contentItem['collect_count'] = contentInfo['collection_amount']
            contentItem['recommend_count'] = contentInfo['rec_amount']
            contentItem['like_count'] = contentInfo['like_amount']
            #print(contentItem)
            yield contentItem

        self.currentPage += 1
        if self.currentPage <= self.totalPage:
            yield scrapy.Request(self.contentStartUrl.format(self.currentPage),
                                 callback=self.parseContentPageJson, method='GET', headers=self.headers, cookies=self.cookies)

