# -*- coding: utf-8 -*-
import scrapy
import json
import time
import math

from RongCloudChannel.items import ContentItem
from RongCloudChannel.utils import dateUtil


class QierhaoSpider(scrapy.Spider):
    name = 'QiErHao'
    contentListStartUrl = "https://om.qq.com/article/list?index={}&category=&search=&source=&startDate=&endDate=&num=10&relogin=1"
    articleDetailUrl = "https://om.qq.com/mstatistic/statistic/SignalArticle?article={}&channel=0&titleType=0&relogin=1"
    videoDetailUrl = "https://om.qq.com/mstatistic/VideoData/VideoRealStatis?vid={}&fields=2%7C7&source=0&relogin=1"


    headers = {
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    cookies = {
        'userid': '15485831',
        #'omaccesstoken': 'a738767a061f5fb8761e1ef534e23f0f72c19e040b5592a31047508627ff89b52255f0c248e1bf7c6f31631b0e54f32b8023d33cffad67887af524c1323b8f6d2fbe4a77a5399acbbd143eb5390eac30',
        'omaccesstoken': '473ed3861a3b43bfe398a0be7d67f671799e7bb5b7f6af8bb0c72f0eff18f95ee22a2b0b4389ef09f5b28c912a065db7cf4fbc27d8ab84c078650e12f9821dcb144986b32e425618cf7aca2c920a9364',
    }


    def __init__(self):
        self.indexId = 1
        self.maxIndexId = 1
        self.totalNumber = 1
        self.beginFlag = True


    def start_requests(self):
        yield scrapy.Request(self.contentListStartUrl.format(self.indexId),
                             callback=self.parseListPageJson, method='GET', headers=self.headers, cookies=self.cookies)


    def parseListPageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        if self.beginFlag:
            self.totalNumber = rltJson['data']['totalNumber']
            self.maxIndexId = math.ceil(self.totalNumber/10)
            self.beginFlag = False

        contentList = rltJson['data']['articles']
        curTime = dateUtil.getCurDate()
        for contentInfo in contentList:
            contentItem = ContentItem()
            contentItem['channel_id'] = "企鹅号"
            contentItem['account_id'] = "2991941540"  #######test
            contentItem['record_class'] = "content_info"
            contentItem['crawl_time'] = curTime
            contentItem['id'] = contentInfo['article_id']
            contentItem['title'] = contentInfo['title']
            contentItem['content_link'] = contentInfo['url']
            contentItem['publish_time'] = contentInfo['pub_time']
            contentItem['comment_count'] = contentInfo['commentnum']
            if 'vid' in contentInfo:
                vid = contentInfo['vid']
                yield scrapy.Request(self.videoDetailUrl.format(vid),
                                     callback=self.parseVideoDetailPageJson, method='GET', headers=self.headers,
                                     cookies=self.cookies, meta={'item': contentItem})
            else:
                yield scrapy.Request(self.articleDetailUrl.format(contentItem['id'] + '00'),
                                     callback=self.parseArticleDetailPageJson, method='GET', headers=self.headers,
                                     cookies=self.cookies, meta={'item': contentItem})

        self.indexId += 1
        if self.indexId <= self.maxIndexId:
            yield scrapy.Request(self.contentListStartUrl.format(self.indexId),
                                 callback=self.parseListPageJson, method='GET', headers=self.headers,
                                 cookies=self.cookies)


    def parseArticleDetailPageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        read_count = rltJson['data']['read']
        curItem = response.meta['item']
        curItem['read_count'] = read_count
        yield curItem


    def parseVideoDetailPageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        read_count = rltJson['data']['new_total_play_pv']
        curItem = response.meta['item']
        curItem['read_count'] = read_count
        yield curItem







