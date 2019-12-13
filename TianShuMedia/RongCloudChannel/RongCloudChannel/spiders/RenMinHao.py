# -*- coding: utf-8 -*-
import scrapy
import time

from RongCloudChannel.utils.targetIdUtil import *
from RongCloudChannel.items import *
from RongCloudChannel.utils import dateUtil


class RenminhaoSpider(scrapy.Spider):
    name = 'RenMinHao'
    channel_id = '人民号'

    videoUrl = 'https://rmh.pdnews.cn/Pc/ArtInfoApi/video?id={}'
    articleUrl = 'https://rmh.pdnews.cn/Pc/ArtInfoApi/article?id={}'


    def __init__(self):
        self.targetDict = getAllTargetIdByChannel(self.channel_id)
        '''self.targetDict = {'9380179': 'h',
                           '9579251': 't',
                           }'''


    def start_requests(self):
        for targetId, targetType in self.targetDict.items():
            time.sleep(2)
            if targetType == 'h':
                yield scrapy.Request(self.videoUrl.format(targetId),
                                     method='GET', callback=self.parseVideoPage, meta={'targetId': targetId})
            if targetType == 't':
                yield scrapy.Request(self.articleUrl.format(targetId),
                                     method='GET', callback=self.parseArticalPage, meta={'targetId': targetId})


    def parseVideoPage(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        targetId = response.meta['targetId']
        link = response.url
        curTime = dateUtil.getCurDate()

        title = ""
        titleList = response.xpath('//div[@class="title"]/h2/text()').extract()
        if len(titleList) == 1:
            title = titleList[0].strip()
        if title == "":
            return

        contentItem = ContentItem()
        contentItem['channel_id'] = self.channel_id

        authorName = ""
        authorNameList = response.xpath('//div[@class="other clearfix m-t"]/p/a/span/text()').extract()
        if len(authorNameList) == 1:
            authorName = authorNameList[0].strip()
        contentItem['account_id'] = authorName

        contentItem['record_class'] = 'content_info'
        contentItem['crawl_time'] = curTime
        contentItem['id'] = targetId
        contentItem['title'] = title
        contentItem['content_link'] = link

        pubAndReadList = response.xpath('//div[@class="other clearfix m-t"]/p/text()').extract()
        if len(pubAndReadList) >= 1:
            pubTime = pubAndReadList[0].strip()
            contentItem['publish_time'] = pubTime
        if len(pubAndReadList) >= 2:
            readStr = pubAndReadList[1].strip().replace("播放量", "")
            contentItem['read_count'] = readStr

        commentCntList = response.xpath('//div[@class="commnet j-comment"]/text()').extract()
        if len(commentCntList) >= 2:
            commentCnt = commentCntList[1].strip()
            contentItem['comment_count'] = commentCnt

        #print(contentItem)
        yield contentItem


    def parseArticalPage(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        targetId = response.meta['targetId']
        link = response.url
        curTime = dateUtil.getCurDate()

        title = ""
        titleList = response.xpath('//div[@class="title"]/h2/text()').extract()
        if len(titleList) == 1:
            title = titleList[0].strip()
        if title == "":
            return

        contentItem = ContentItem()
        contentItem['channel_id'] = self.channel_id

        authorName = ""
        authorNameList = response.xpath('//div[@class="other clearfix m-t"]/p/a/span/text()').extract()
        if len(authorNameList) == 1:
            authorName = authorNameList[0].strip()
        contentItem['account_id'] = authorName

        contentItem['record_class'] = 'content_info'
        contentItem['crawl_time'] = curTime
        contentItem['id'] = targetId
        contentItem['title'] = title
        contentItem['content_link'] = link

        pubList = response.xpath('//div[@class="other clearfix m-t"]/p/text()').extract()
        if len(pubList) == 1:
            publish_time = pubList[0].strip()
            contentItem['publish_time'] = publish_time

        commentCntList = response.xpath('//div[@class="commnent"]/a/text()').extract()
        if len(commentCntList) >= 2:
            commentCnt = commentCntList[1].strip()
            contentItem['comment_count'] = commentCnt

        #print(contentItem)
        yield contentItem



