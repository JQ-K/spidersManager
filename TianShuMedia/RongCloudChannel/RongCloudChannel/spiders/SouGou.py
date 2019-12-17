# -*- coding: utf-8 -*-
import scrapy
import json
import math
import time

from scrapy.http import FormRequest
from RongCloudChannel.items import ContentItem
from RongCloudChannel.items import AccountItem
from RongCloudChannel.utils import dateUtil
from RongCloudChannel.conf.contentStatusMapping import *
from RongCloudChannel.utils.accountUtil import *


class SougouSpider(scrapy.Spider):
    name = 'SouGou'
    channel_id = "搜狗号"

    loginUrl = "http://mp.sogou.com/api/login"
    articleUrl = "http://mp.sogou.com/api/{}/articles?status="
    fansAnalysisUrl = "http://mp.sogou.com/api/statistics/fans-analysis/{}"

    '''headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    }'''
    cookies = {
        "mp.sid": "",
        "mp.sid.sig": "",
    }

    def __init__(self):
        self.accountDict = getAllAccountByChannel(self.channel_id)


    def start_requests(self):
        for user, passwordAndId in self.accountDict.items():
            password, curId = passwordAndId
            formdata = {"email": user, "pwd": password}
            time.sleep(3)
            yield FormRequest(self.loginUrl, method='POST',
                              formdata=formdata, callback=self.parseLoginPage,
                              meta={'formdata': formdata,
                                    'account': user,
                                    'curId': curId})


    def parseLoginPage(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        account = response.meta['account']
        curId = response.meta['curId']
        headers = response.headers
        set_cookie = headers.getlist('Set-Cookie')
        rlt_cookie = {}

        for tempCookie in set_cookie:
            tempStr = tempCookie.decode('utf-8').split(';')
            for elem in tempStr:
                curElem = elem.strip()
                index = curElem.find('=')
                if index >= 0:
                    key = curElem[0:index]
                    val = curElem[index+1:]
                    if key in self.cookies.keys():
                        rlt_cookie[key] = val
        time.sleep(5)
        yield scrapy.Request(self.fansAnalysisUrl.format(dateUtil.getYesterday()),
                             method='GET', callback=self.parseFansAnalysisPageJson,
                             cookies=rlt_cookie,
                             #headers=self.headers,
                             meta={'account': account})
        time.sleep(5)
        yield scrapy.Request(self.articleUrl.format(1),
                             method='GET', callback=self.parseArticlePageJson,
                             cookies=rlt_cookie,
                             #headers=self.headers,
                             meta={'cookie': rlt_cookie, 'currentPage': 1, 'totalPage': 1, 'beginFlag': True, 'account': account})


    def parseFansAnalysisPageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        account = response.meta['account']
        rltJson = json.loads(response.text)
        accountItem = AccountItem()
        accountItem['channel_id'] = self.channel_id
        accountItem['account_id'] = account
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
        account = response.meta['account']
        cookie = response.meta['cookie']
        currentPage = response.meta['currentPage']
        totalPage = response.meta['totalPage']
        beginFlag = response.meta['beginFlag']
        rltJson = json.loads(response.text)
        if beginFlag:
            total = int(rltJson['total'])
            totalPage = math.ceil(total/10)
            beginFlag = False

        contentList = rltJson['list']
        curTime = dateUtil.getCurDate()
        for contentInfo in contentList:
            contentItem = ContentItem()
            contentItem['channel_id'] = self.channel_id
            contentItem['account_id'] = account
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

            contentItem['publish_status'] = publicContentStatus[channelContentStatus[self.channel_id][status]]
            yield contentItem

        currentPage += 1
        if currentPage <= totalPage:
            time.sleep(5)
            yield scrapy.Request(self.articleUrl.format(currentPage),
                                 method='GET', callback=self.parseArticlePageJson,
                                 #headers=self.headers,
                                 cookies=cookie,
                                 meta={'cookie': cookie, 'currentPage': currentPage, 'totalPage': totalPage, 'beginFlag': beginFlag, 'account': account})


