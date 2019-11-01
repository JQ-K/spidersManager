# -*- coding: utf-8 -*-
import scrapy
import json
import time
import math

from RongCloudChannel.items import ContentItem


class QierhaoSpider(scrapy.Spider):
    name = 'QiErHao'
    contentListStartUrl = "https://om.qq.com/article/list?index={}&category=&search=&source=&startDate=&endDate=&num=10&relogin=1"
    #contentListNextUrl = "https://om.qq.com/article/list?category=&search=&source=&startDate=&endDate=&num=10&index=1&refreshField=2019-10-27+16%3A56%3A01&relogin=1"
    #articleDetailUrl = "https://om.qq.com/article/detailArticleAnalysis?articleId=20191031A0EJOU00&article_type=0&titleType=0"
    #videoDetailUrl = "https://om.qq.com/article/singleVideoStatistic?articleId=k3008b0he8e"

    headers = {
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'RK=dMT0a4k8bo; ptcz=3481bcf105e786bb706f052f54e6d3c3f9c29dc8d6d22656b7289e11bd210b35; pgv_pvi=1417649152; pgv_pvid=3445362121; pgv_info=ssid=s8640282297; ts_refer=www.baidu.com/link; ts_uid=886109250; appDownClose=1; pgv_si=s4442557440; _qpsvr_localtk=0.5305009181646689; ptisp=ctc; ptui_loginuin=2991941540; wxky=1; userid=15485831; omaccesstoken=a738767a061f5fb8761e1ef534e23f0f72c19e040b5592a31047508627ff89b52255f0c248e1bf7c6f31631b0e54f32b8023d33cffad67887af524c1323b8f6d2fbe4a77a5399acbbd143eb5390eac30; omaccesstoken_expire=1572767841; omtoken=a738767a061f5fb8761e1ef534e23f0f72c19e040b5592a31047508627ff89b52255f0c248e1bf7c6f31631b0e54f32b8023d33cffad67887af524c1323b8f6d2fbe4a77a5399acbbd143eb5390eac30; tvfe_boss_uuid=90cdf64eb1a2d595; video_guid=f21b57d1bc9e03d2; video_platform=2; rmod=1; TSID=781gntuh3tvodpvk538dqh38a6; alertclicked=%7C1%7C; ts_last=om.qq.com/article/articleStatistic'
    }


    def __init__(self):
        self.indexId = 1
        self.totalNumber = 1
        self.beginFlag = True


    def start_requests(self):
        yield scrapy.Request(self.contentListStartUrl.format(self.indexId),
                             callback=self.parseListPageJson, method='GET', headers=self.headers)


    def parseListPageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)


'''
class QierhaoSpider(scrapy.Spider):
    name = 'QiErHao'
    #contentListStartUrl = "https://om.qq.com/article/list?index=1&category=&search=&source=&startDate=&endDate=&num=10&relogin=1"
    #contentListNextUrl = "https://om.qq.com/article/list?category=&search=&source=&startDate=&endDate=&num=10&index=1&refreshField=2019-10-27+16%3A56%3A01&relogin=1"
    #articleDetailUrl = "https://om.qq.com/article/detailArticleAnalysis?articleId=20191031A0EJOU00&article_type=0&titleType=0"
    #videoDetailUrl = "https://om.qq.com/article/singleVideoStatistic?articleId=k3008b0he8e"

    articleStatisticUrl = "https://om.qq.com/mstatistic/statistic/ArticleReal?page={}&num=8&relogin=1"
    videoStatisticUrl = "https://om.qq.com/mstatistic/VideoData/MediaVideoList?limit=8&page={}&fields=2%7C3&source=0&relogin=1"

    headers = {
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        #'Referer': 'https://om.qq.com/article/articleStatistic',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'RK=dMT0a4k8bo; ptcz=3481bcf105e786bb706f052f54e6d3c3f9c29dc8d6d22656b7289e11bd210b35; pgv_pvi=1417649152; pgv_pvid=3445362121; pgv_info=ssid=s8640282297; ts_refer=www.baidu.com/link; ts_uid=886109250; appDownClose=1; pgv_si=s4442557440; _qpsvr_localtk=0.5305009181646689; ptisp=ctc; ptui_loginuin=2991941540; wxky=1; userid=15485831; omaccesstoken=a738767a061f5fb8761e1ef534e23f0f72c19e040b5592a31047508627ff89b52255f0c248e1bf7c6f31631b0e54f32b8023d33cffad67887af524c1323b8f6d2fbe4a77a5399acbbd143eb5390eac30; omaccesstoken_expire=1572767841; omtoken=a738767a061f5fb8761e1ef534e23f0f72c19e040b5592a31047508627ff89b52255f0c248e1bf7c6f31631b0e54f32b8023d33cffad67887af524c1323b8f6d2fbe4a77a5399acbbd143eb5390eac30; tvfe_boss_uuid=90cdf64eb1a2d595; video_guid=f21b57d1bc9e03d2; video_platform=2; rmod=1; TSID=781gntuh3tvodpvk538dqh38a6; alertclicked=%7C1%7C; ts_last=om.qq.com/article/articleStatistic'
    }


    def __init__(self):
        self.articleCurrentPage = 1
        self.articleTotalPage = 1
        self.articleBeginFlag = True

        self.videoCurrentPage = 1
        self.videoTotalPage = 1
        self.videoBeginFlag = True


    def start_requests(self):
        yield scrapy.Request(self.articleStatisticUrl.format(self.articleCurrentPage),
                             callback=self.parseArticlePageJson, method='GET', headers=self.headers)


    def parseArticlePageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        print(rltJson)
        if self.articleBeginFlag:
            self.articleTotalPage = rltJson['data']['totalPage']
            self.articleBeginFlag = False

        articleInfoList = rltJson['data']['statistic']
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for info in articleInfoList:
            contentItem = ContentItem()
            contentItem['channel_name'] = "企鹅号"
            contentItem['record_class'] = "content_info"
            contentItem['crawl_time'] = curTime
            contentItem['id'] = info['articleId']
            contentItem['content_link'] = info['url']
            contentItem['publish_time'] = info['pubTime']
            contentItem['read_count'] = info['read']
            yield contentItem

        self.articleCurrentPage += 1
        if self.articleCurrentPage <= self.articleTotalPage:
            yield scrapy.Request(self.articleStatisticUrl.format(self.articleCurrentPage),
                                 callback=self.parseArticlePageJson, method='GET', headers=self.headers)


    def parseVideoPageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        print(rltJson)
        if self.videoBeginFlag:
            totalVideo = rltJson['data']['total']
            self.videoTotalPage = math.ceil(totalVideo/8)
            self.videoBeginFlag = False

        videoInfoList = rltJson['data']['list']
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for info in videoInfoList:
            contentItem = ContentItem()
            contentItem['channel_name'] = "企鹅号"
            contentItem['record_class'] = "content_info"
            contentItem['crawl_time'] = curTime
            contentItem['id'] = info['vid']
            contentItem['content_link'] = info['url']
            contentItem['publish_time'] = info['uploadTime']
            contentItem['read_count'] = info['newTotalPlayPv']
            yield contentItem
'''
