# -*- coding: utf-8 -*-
import scrapy
import json
import time
import re

from RongCloudChannel.utils.targetIdUtil import *
from RongCloudChannel.items import *
from RongCloudChannel.utils import dateUtil
import browsercookie
import requests


class WeiboSpider(scrapy.Spider):
    name = 'WeiBo'
    channel_id = '微博'

    # cookies = {
    #     "SUB": "_2A25w6dWBDeRhGeFN6VcS8CbMwzqIHXVTn0BJrDV8PUNbmtBeLXWhkW9NQEWMQC6XHmRc3jq7eKYF5PW4VLhZojzd",
    # }
    cookies={}
    chrome_cookies = browsercookie.chrome()
    cookies_dict = requests.utils.dict_from_cookiejar(chrome_cookies)
    cookies["SUB"]=cookies_dict["SUB"]
    print("cookies",cookies)

    def __init__(self):
        self.targetDict = getAllTargetIdByChannel(self.channel_id)
        #self.targetDict = {'http://weibo.com/ttarticle/p/show?id=2310474420460149342283': 't',}


    def start_requests(self):
        for targetId, targetType in self.targetDict.items():
            time.sleep(2)
            if targetType == 't':
                curUrl = targetId.replace("http:", "https:")
                yield scrapy.Request(curUrl, method='GET', callback=self.parseArticalUrl,
                                     meta={'targetId': targetId},
                                     cookies=self.cookies
                                     )


    def parseArticalUrl(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        content_link = response.meta['targetId']

        titleList = response.xpath('//div[@class="title"]/text()').extract()
        if len(titleList) != 1:
            return
        title = titleList[0].strip()

        contentItem = ContentItem()
        curTime = dateUtil.getCurDate()
        contentItem['channel_id'] = self.channel_id

        author = ""
        authorList = response.xpath('//em[@class="W_autocut"]/text()').extract()
        if len(authorList) == 1:
            author = authorList[0].strip()
        contentItem['account_id'] = author

        contentItem['record_class'] = 'content_info'
        contentItem['crawl_time'] = curTime
        contentItem['title'] = title
        contentItem['content_link'] = content_link

        idx = content_link.rfind("id=")
        if idx < 0:
            contentItem['id'] = content_link
        else:
            contentItem['id'] = content_link[idx + 3:]

        publish_time = ""
        pubTimeList = response.xpath('//span[@class="time"]/text()').extract()
        if len(pubTimeList) == 1:
            publish_time = pubTimeList[0].strip()
        contentItem['publish_time'] = self.fixPublishTime(publish_time, str(curTime)[0:4])

        readCount = 0
        readCountList = response.xpath('//span[@class="num"]/text()').extract()
        if len(readCountList) == 1:
            readCount = readCountList[0].strip().replace("阅读数：", "")
        contentItem['read_count'] = readCount

        likeCount = 0
        likeCountList = response.xpath('//span[@node-type="like_status"]/em/text()').extract()
        if len(likeCountList) == 1:
            likeCount = likeCountList[0].strip()
        contentItem['like_count'] = likeCount

        #print(contentItem)
        yield contentItem


    def fixPublishTime(self, publish_time, year):
        if re.fullmatch(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', publish_time):
            return publish_time
        elif re.fullmatch(r'\d{2}-\d{2} \d{2}:\d{2}:\d{2}', publish_time):
            return year + '-' + publish_time
        elif re.fullmatch(r'\d{2}-\d{2} \d{2}:\d{2}', publish_time):
            return year + '-' + publish_time + ':00'
        else:
            print('新的时间格式：' + publish_time)
            return '0000-00-00 00:00:00'
