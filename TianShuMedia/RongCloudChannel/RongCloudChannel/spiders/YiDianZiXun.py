# -*- coding: utf-8 -*-
import scrapy

from RongCloudChannel.items import ContentItem
from RongCloudChannel.items import AccountItem
from scrapy.http import FormRequest
from RongCloudChannel.utils import dateUtil
from RongCloudChannel.utils.accountUtil import *


class YidianzixunSpider(scrapy.Spider):
    name = 'YiDianZiXun'
    channel_id = '一点资讯'

    loginUrl = "https://mp.yidianzixun.com/sign_in"
    articleListUrl = "https://mp.yidianzixun.com/model/Article?page={}&page_size=10&status={}&has_data=1&type=original"

    fanUrl = "https://mp.yidianzixun.com/api/get-fans-rate"

    statusMap = {
        '2,6,7': 3, #已发布
        '1,4,5,14': 1, #待审核
        '3': 2, #未通过
        '0': 0, #草稿
        '9': 9, #已删除
    }


    def __init__(self):
        self.accountDict = getAllAccountByChannel(self.channel_id)
        #self.accountDict = {"15802103561": "P@ssword521"}


    def start_requests(self):
        for user, password in self.accountDict.items():
            formdata = {"username": user, "password": password}
            time.sleep(3)
            yield FormRequest(self.loginUrl, method='POST',
                              formdata=formdata, callback=self.parseLoginPage,
                              meta={'formdata': formdata, 'account': user})


    def parseLoginPage(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        account = response.meta['account']
        rltJson = json.loads(response.text)
        try:
            cookieStr = rltJson['cookie']
            tempIdx = cookieStr.find("=")
            if tempIdx < 0:
                print('get cookie error: ' + cookieStr)
                return
            cookieKey = cookieStr[0:tempIdx]
            cookieVal = cookieStr[tempIdx+1:]
            curCookie = {cookieKey: cookieVal}
        except:
            print("登录失败：" + response.text)
            print(response.meta['formdata'])
            ####test
            if isErrorAccount(self.channel_id, response.text):
                postLoginErrorAccount(self.channel_id, account)
            return
        time.sleep(2)
        yield scrapy.Request(self.fanUrl, method='GET', callback=self.parseFansPage,
                             cookies=curCookie, meta={'account': account})
        for statusKey, statusVal in self.statusMap.items():
            time.sleep(2)
            yield scrapy.Request(self.articleListUrl.format(1, statusKey), method='GET',
                                 callback=self.parseArticlePage,
                                 cookies=curCookie,
                                 meta={'account': account, 'cookies': curCookie,
                                       'currentPage': 1, 'totalPage': 1, 'beginFlag': True,
                                       'statusKey': statusKey, 'statusVal': statusVal})


    def parseFansPage(self, response):
        #print(response.text)
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        account = response.meta['account']
        rltJson = json.loads(response.text)
        if 'result' in rltJson:
            accountItem = AccountItem()
            accountItem['channel_id'] = self.channel_id
            accountItem['account_id'] = account
            accountItem['record_class'] = "channel_info"
            accountItem['crawl_time'] = dateUtil.getCurDate()
            if 'fans_add' in rltJson['result']:
                if 'fans_add' in rltJson['result']['fans_add']:
                    accountItem['new_subscribe_count'] = rltJson['result']['fans_add']['fans_add']
            if 'fans_reduce' in rltJson['result']:
                if 'fans_reduce' in rltJson['result']['fans_reduce']:
                    accountItem['cancel_fans_count'] = rltJson['result']['fans_reduce']['fans_reduce']
            if 'fans_total' in rltJson['result']:
                if 'fans_total' in rltJson['result']['fans_total']:
                    accountItem['total_subscribe_count'] = rltJson['result']['fans_total']['fans_total']
            #print(accountItem)
            yield accountItem


    def parseArticlePage(self, response):
        #print(response.text)
        if response.status != 200:
            print('get url error: ' + response.url)
            return

        account = response.meta['account']
        cookies = response.meta['cookies']
        currentPage = response.meta['currentPage']
        totalPage = response.meta['totalPage']
        beginFlag = response.meta['beginFlag']
        statusKey = response.meta['statusKey']
        statusVal = response.meta['statusVal']

        rltJson = json.loads(response.text)
        if beginFlag:
            totalPage = rltJson['page_total']
            beginFlag = False

        contentList = rltJson['posts']
        curTime = dateUtil.getCurDate()
        for contentInfo in contentList:
            contentItem = ContentItem()
            contentItem['channel_id'] = self.channel_id
            contentItem['account_id'] = account
            contentItem['record_class'] = "content_info"
            contentItem['crawl_time'] = curTime

            id = ""
            if 'newsId' in contentInfo:
                id = contentInfo['newsId']
            contentItem['id'] = id

            if statusVal == 3 and len(id) > 0:
                contentItem['content_link'] = "https://www.yidianzixun.com/article/" + str(id)

            if 'title' in contentInfo:
                contentItem['title'] = contentInfo['title']

            if 'date' in contentInfo:
                timeStamp = contentInfo['date']
                if len(str(timeStamp)) == 13:
                    timeStamp = int(timeStamp/1000)
                if len(str(timeStamp)) == 10:
                    contentItem['publish_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeStamp))

            contentItem['publish_status'] = statusVal
            if 'all_data' in contentInfo:
                allData = contentInfo['all_data']
                if 'clickDoc' in allData:
                    contentItem['read_count'] = allData['clickDoc']
                if 'addCommentDoc' in allData:
                    contentItem['comment_count'] = allData['addCommentDoc']
                if 'shareDoc' in allData:
                    contentItem['share_count'] = allData['shareDoc']
                if 'likeDoc' in allData:
                    contentItem['collect_count'] = allData['likeDoc']   #收藏？
                if 'viewDoc' in allData:
                    contentItem['recommend_count'] = allData['viewDoc']
            #print(contentItem)
            yield contentItem
        currentPage += 1
        if currentPage <= totalPage:
            time.sleep(5)
            yield scrapy.Request(self.articleListUrl.format(currentPage, statusKey), method='GET',
                                 callback=self.parseArticlePage,
                                 cookies=cookies,
                                 meta={'account': account, 'cookies': cookies,
                                       'currentPage': currentPage, 'totalPage': totalPage, 'beginFlag': beginFlag,
                                       'statusKey': statusKey, 'statusVal': statusVal})

