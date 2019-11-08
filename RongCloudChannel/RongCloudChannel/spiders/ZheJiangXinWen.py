# -*- coding: utf-8 -*-
import scrapy
import json
import time

from scrapy.http import FormRequest
from RongCloudChannel.conf.channelAccount import *
from RongCloudChannel.items import ContentItem
from RongCloudChannel.items import AccountItem
from RongCloudChannel.utils import dateUtil


class ZhejiangxinwenSpider(scrapy.Spider):
    name = 'ZheJiangXinWen'
    channel_id = '浙江新闻'

    articleUrl = "https://mcn.8531.cn/mcn/web/pgcArticle/pubList.do"
    fansAnalysisUrl = "https://mcn.8531.cn/mcn/web/data/pgcSubscribeAnalysis.do"
    viewArticleUrl = "https://mcn.8531.cn/#!/imagetextdetail?articleId={}"
    articleAnalysisUrl = "https://mcn.8531.cn/mcn/web/data/pgcContentAnalysis.do"

    articleAnalysisDict = {}

    headers = {
        'requestToken': '5b425da2-9389-4c4c-9611-69c18b7f6527',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    }

    cookies = {
        'MCNWEBJSESSIONID': 'f88f849e-d00a-4fb6-83c8-eb1fa156ee3d'
    }

    def __init__(self):
        self.curPage = 1
        self.totalPage = 1
        self.beginFlag = True

        self.articleAnalysisCurPage = 1
        self.articleAnalysisTotalPage = 1
        self.articleAnalysisBeginFlag = True


    def start_requests(self):
        yield FormRequest(self.articleAnalysisUrl, method='POST',
                          formdata={'days': '10000', 'channelId': '1', 'sortRule': '1', 'currPage': str(self.articleAnalysisCurPage), 'pageSize': '12'},
                          callback=self.parseArticleAnalysisPage, headers=self.headers, cookies=self.cookies)


    def parseArticlePage(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        if self.beginFlag:
            self.totalPage = rltJson['data']['totalPages']
            self.beginFlag = False

        contentList = rltJson['data']['ldata']
        curTime = dateUtil.getCurDate()
        for contentInfo in contentList:
            contentItem = ContentItem()
            contentItem['channel_id'] = self.channel_id
            contentItem['record_class'] = "content_info"
            contentItem['crawl_time'] = curTime
            contentItem['id'] = contentInfo['id']
            title = contentInfo['articleTitle']
            contentItem['title'] = title
            contentItem['content_link'] = self.viewArticleUrl.format(contentInfo['id'])
            if title in self.articleAnalysisDict:
                contentItem['publish_time'] = self.articleAnalysisDict[title]['publish_time']
                contentItem['read_count'] = self.articleAnalysisDict[title]['read_count']
                contentItem['share_count'] = self.articleAnalysisDict[title]['share_count']
                contentItem['collect_count'] = self.articleAnalysisDict[title]['collect_count']
            else:
                contentItem['publish_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime((int(contentInfo['operTime']))/1000))
                contentItem['read_count'] = 0
                contentItem['share_count'] = 0
                contentItem['collect_count'] = 0
            yield contentItem

        self.curPage += 1
        if self.curPage <= self.totalPage:
            yield FormRequest(self.articleUrl, method='POST',
                              formdata={'currPage': str(self.curPage)}, callback=self.parseArticlePage,
                              headers=self.headers, cookies=self.cookies)


    def parseChannelPage(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        accountItem = AccountItem()
        accountItem['channel_id'] = self.channel_id
        accountItem['record_class'] = "channel_info"
        accountItem['crawl_time'] = dateUtil.getCurDate()
        accountItem['new_subscribe_count'] = rltJson['data'][0]['subscribe_cnt']
        accountItem['total_subscribe_count'] = rltJson['data'][0]['his_subscribe_cnt']
        accountItem['cancel_fans_count'] = rltJson['data'][0]['cancel_subscribe_cnt']

        yield accountItem


    def parseArticleAnalysisPage(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        if self.articleAnalysisBeginFlag:
            self.articleAnalysisTotalPage = rltJson['data']['totalPages']
            self.articleAnalysisBeginFlag = False

        contentList = rltJson['data']['ldata']
        for contentInfo in contentList:
            title = contentInfo['article_title']
            publish_time = contentInfo['publish_time']
            read_count = contentInfo['weighted_his_read_cnt']
            share_count = contentInfo['his_forward_cnt']
            collect_count = contentInfo['his_collect_cnt']
            self.articleAnalysisDict[title] = {'publish_time': publish_time,
                                               'read_count': read_count,
                                               'share_count': share_count,
                                               'collect_count': collect_count}
        self.articleAnalysisCurPage += 1
        if self.articleAnalysisCurPage <= self.articleAnalysisTotalPage:
            yield FormRequest(self.articleAnalysisUrl, method='POST',
                              formdata={'days': '10000', 'channelId': '1', 'sortRule': '1',
                                        'currPage': str(self.articleAnalysisCurPage), 'pageSize': '12'},
                              callback=self.parseArticleAnalysisPage, headers=self.headers, cookies=self.cookies)
        else:
            print(self.articleAnalysisDict)
            yield FormRequest(self.fansAnalysisUrl, method='POST',
                              formdata={'days': '1', 'channelId': '1'}, callback=self.parseChannelPage,
                              headers=self.headers, cookies=self.cookies)

            yield FormRequest(self.articleUrl, method='POST',
                              formdata={'currPage': str(self.curPage)}, callback=self.parseArticlePage,
                              headers=self.headers, cookies=self.cookies)




