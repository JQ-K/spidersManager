# -*- coding: utf-8 -*-
import scrapy
import json
import math
import time

from scrapy.http import FormRequest
from RongCloudChannel.conf.channelAccount import *
from RongCloudChannel.items import ContentItem
from RongCloudChannel.items import AccountItem
from RongCloudChannel.utils import dateUtil

class SougouSpider(scrapy.Spider):
    name = 'SouGou'
    channel_id = "搜狗"

    loginUrl = "http://mp.sogou.com/api/login"
    articleUrl = "http://mp.sogou.com/api/{}/articles?status="
    fansAnalysisUrl = "http://mp.sogou.com/api/statistics/fans-analysis/{}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    }
    cookies = {
        "mp.sid": "",
        "mp.sid.sig": "",
    }

    def __init__(self):
        self.articleCurrentPage = 1
        self.articleTotalPage = 1
        self.articleBeginFlag = True


    def start_requests(self):
        for user, password in account[self.channel_id].items():
            formData = {"email": user, "pwd": password}
            yield FormRequest(self.loginUrl, method='POST',
                              formdata=formData, callback=self.parseLoginPage)


    def parseLoginPage(self, response):
        headers = response.headers
        set_cookie = headers.getlist('Set-Cookie')

        for tempCookie in set_cookie:
            tempStr = tempCookie.decode('utf-8').split(';')
            for elem in tempStr:
                curElem = elem.strip()
                index = curElem.find('=')
                if index >= 0:
                    key = curElem[0:index]
                    val = curElem[index+1:]
                    if key in self.cookies.keys():
                        self.cookies[key] = val
        print(self.cookies)

        yield scrapy.Request(self.fansAnalysisUrl.format(dateUtil.getYesterday()),
                             method='GET', callback=self.parseFansAnalysisPageJson, cookies=self.cookies, headers=self.headers)

        yield scrapy.Request(self.articleUrl.format(self.articleCurrentPage),
                             method='GET', callback=self.parseArticlePageJson, cookies=self.cookies, headers=self.headers)


    def parseFansAnalysisPageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        accountItem = AccountItem()
        accountItem['channel_id'] = self.channel_id
        accountItem['record_class'] = "channel_info"
        accountItem['crawl_time'] = dateUtil.getCurDate()
        accountItem['new_visit_count'] = rltJson['access']
        accountItem['total_visit_count'] = rltJson['total_access']
        accountItem['new_subscribe_count'] = rltJson['subscribe']
        accountItem['total_subscribe_count'] = rltJson['total_subscribe']
        yield accountItem


    def parseArticlePageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        if self.articleBeginFlag:
            total = int(rltJson['total'])
            self.articleTotalPage = math.ceil(total/10)
            self.articleBeginFlag = False

        contentList = rltJson['list']
        curTime = dateUtil.getCurDate()
        for contentInfo in contentList:
            contentItem = ContentItem()
            contentItem['channel_id'] = self.channel_id
            contentItem['record_class'] = "content_info"
            contentItem['crawl_time'] = curTime
            contentItem['id'] = contentInfo['id']
            contentItem['title'] = contentInfo['title']
            contentItem['content_link'] = contentInfo['url']
            contentItem['publish_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(contentInfo['updatedAt'])))
            contentItem['read_count'] = contentInfo['readingNum']
            contentItem['comment_count'] = contentInfo['commentsNum']
            contentItem['share_count'] = contentInfo['forwardingNum']
            contentItem['collect_count'] = contentInfo['collectionNum']
            contentItem['recommend_count'] = contentInfo['recommendedNum']
            status = int(contentInfo['status'])  # 搜狗：1-已发布；40-未通过；134-草稿

            if status == 1:
                contentItem['publish_status'] = 3
            if status == 40:
                contentItem['publish_status'] = 2
            if status == 134:
                contentItem['publish_status'] = 0
            #print(contentItem)
            yield contentItem

        self.articleCurrentPage += 1
        if self.articleCurrentPage <= self.articleTotalPage:
            yield scrapy.Request(self.articleUrl.format(self.articleCurrentPage),
                                 method='GET', callback=self.parseArticlePageJson, cookies=self.cookies,
                                 headers=self.headers)




