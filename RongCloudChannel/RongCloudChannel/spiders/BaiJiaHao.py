# -*- coding: utf-8 -*-
import scrapy
import json

from RongCloudChannel.items import ContentItem
from RongCloudChannel.items import ChannelItem

class BaijiahaoSpider(scrapy.Spider):
    name = 'BaiJiaHao'
    startUrl = "https://baijiahao.baidu.com/builder/article/lists?type=&collection=&pageSize=10&currentPage={}&search=&app_id=1639272210762362&dynamic=1"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'BDUSS=VdlWHNWd0t0a1Q3ZH5odU1GWkRYeXhBfjA4WEpFall0aTVRbDJ2ZWpWRmdBT0pkSVFBQUFBJCQAAAAAAAAAAAEAAAAz910NxOq44rO0w-bM9QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGBzul1gc7pdN'
    }


    def __init__(self):
        self.currentPage = 1
        self.totalPage = 1
        self.beginFlag = True


    def start_requests(self):
        print(self.startUrl.format(self.currentPage))
        print(self.headers)
        cookies = {'Cookie': 'BDUSS=VdlWHNWd0t0a1Q3ZH5odU1GWkRYeXhBfjA4WEpFall0aTVRbDJ2ZWpWRmdBT0pkSVFBQUFBJCQAAAAAAAAAAAEAAAAz910NxOq44rO0w-bM9QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGBzul1gc7pdN'}
        yield scrapy.Request(self.startUrl.format(self.currentPage),
                             callback=self.parseContentPageJson, method='GET', headers=self.headers, cookies=cookies)


    def parseContentPageJson(self, response):
        print(response.text)
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        if self.beginFlag:
            self.totalPage = rltJson['data']['page']['totalPage']
            self.beginFlag = False

        contentList = rltJson['data']['list']
        for contentInfo in contentList:
            contentItem = ContentItem()
            contentItem['id'] = contentInfo['id']
            contentItem['content_link'] = contentInfo['url']
            contentItem['publish_time'] = contentInfo['publish_time']
            contentItem['audit_result'] = contentInfo['audit_msg']
            contentItem['read_count'] = contentInfo['read_amount']
            contentItem['comment_count'] = contentInfo['comment_amount']
            contentItem['share_count'] = contentInfo['share_amount']
            contentItem['collect_count'] = contentInfo['collect_amount']
            contentItem['recommend_count'] = contentInfo['rec_amount']
            contentItem['like_count'] = contentInfo['like_amount']
            print(contentItem)
            #yield contentItem

        self.currentPage += 1
        if self.currentPage <= self.totalPage:
            yield scrapy.Request(self.startUrl.format(self.currentPage),
                                 callback=self.parseContentPageJson, method='GET', headers=self.headers)

