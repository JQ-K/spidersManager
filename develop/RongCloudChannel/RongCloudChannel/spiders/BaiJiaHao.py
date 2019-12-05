# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
from RongCloudChannel.utils.targetIdUtil import *
from RongCloudChannel.items import *
from RongCloudChannel.utils import dateUtil


class BaijiahaoSpider(scrapy.Spider):
    name = 'BaiJiaHao'
    channel_id = '百家号'

    #视频:type=h
    vid = '16335743810432281251'
    videoUrl = "https://haokan.baidu.com/v?vid={}"
    videoAuthorUrl = "https://haokan.baidu.com/videoui/api/videoauthor?vid={}"
    videoCommentUrl = "https://haokan.baidu.com/videoui/api/commentget?url_key={}"

    #文章:type=t  文章没有作者信息
    tid = '1637929714955564586'
    articalUrl = "http://baijiahao.baidu.com/builder/preview/s?id={}"
    articalCommentUrl = "https://mbd.baidu.com/po/api/comment/getInfo.json?comType=baidumedia&tid={}"


    def __init__(self):
        self.targetDict = getAllTargetIdByChannel(self.channel_id)
        '''self.targetDict = {'16335743810432281251': 'h',
                           '1637929714955564586': 't',}'''


    def start_requests(self):
        #print(self.targetDict)
        for targetId, targetType in self.targetDict.items():
            time.sleep(2)
            if targetType == 'h':
                yield scrapy.Request(self.videoAuthorUrl.format(targetId),
                                     method='GET', callback=self.parseVideoAuthor, meta={'targetId': targetId})
            if targetType == 't':
                yield scrapy.Request(self.articalCommentUrl.format(targetId),
                                     method='GET', callback=self.parseArticalComment, meta={'targetId': targetId})


    def parseVideoAuthor(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        targetId = response.meta['targetId']
        rltJson = json.loads(response.text)
        if rltJson['errno'] != 0:
            return
        fansCnt = rltJson['data']['response']['cnt']['fansCnt']
        accountItem = AccountItem()
        curTime = dateUtil.getCurDate()
        accountItem['channel_id'] = self.channel_id
        accountItem['record_class'] = 'channel_info'
        accountItem['crawl_time'] = curTime
        accountItem['total_subscribe_count'] = fansCnt
        authorName = rltJson['data']['response']['author']['author']
        accountItem['account_id'] = authorName
        #print(accountItem)
        yield accountItem
        time.sleep(2)
        yield scrapy.Request(self.videoCommentUrl.format(targetId),
                             method='GET', callback=self.parseVideoComment,
                             meta={'targetId': targetId, 'authorName': authorName})


    def parseVideoComment(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        targetId = response.meta['targetId']
        authorName = response.meta['authorName']
        rltJson = json.loads(response.text)
        if rltJson['status'] != 0:
            return
        commentCnt = rltJson['data']['comment_count']
        contentItem = ContentItem()
        curTime = dateUtil.getCurDate()
        contentItem['channel_id'] = self.channel_id
        contentItem['account_id'] = authorName
        contentItem['record_class'] = 'content_info'
        contentItem['crawl_time'] = curTime
        contentItem['id'] = targetId
        contentItem['comment_count'] = commentCnt
        time.sleep(2)
        yield scrapy.Request(self.videoUrl.format(targetId),
                             method='GET', callback=self.parseVideo, meta={'contentItem': contentItem})


    def parseVideo(self, response):
        contentItem = response.meta['contentItem']
        link = response.url
        contentItem['content_link'] = link

        titleList = response.xpath('//h2[@class="videoinfo-title"]/text()').extract()
        title = ""
        if len(titleList) == 1:
            title = titleList[0].strip()
        contentItem['title'] = title

        playNumList = response.xpath('//span[starts-with(@class,"videoinfo-playnums")]/text()').extract()
        playNumStr = None
        if len(playNumList) == 1:
            playNumStr = playNumList[0].strip()
        if playNumStr is not None:
            index1 = playNumStr.find("次播放")
            if index1 > 0:
                playNum = playNumStr[0:index1]
                contentItem['read_count'] = playNum
            publishTimeList = re.findall(r"\d+年\d+月\d+日", playNumStr)
            if len(publishTimeList) == 1:
                publishTime = publishTimeList[0].replace("年", "-").replace("月", "-").replace("日", "") + " 00:00:00"
                contentItem['publish_time'] = publishTime

        #print(contentItem)
        yield contentItem


    def parseArticalComment(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        targetId = response.meta['targetId']
        rltJson = json.loads(response.text)
        if rltJson['errno'] != 0:
            return
        commentCnt = rltJson['data']['hasComment']
        contentItem = ContentItem()
        curTime = dateUtil.getCurDate()
        contentItem['channel_id'] = self.channel_id
        contentItem['record_class'] = 'content_info'
        contentItem['crawl_time'] = curTime
        contentItem['id'] = targetId
        contentItem['comment_count'] = commentCnt
        time.sleep(2)
        yield scrapy.Request(self.articalUrl.format(targetId),
                             method='GET', callback=self.parseArtical, meta={'contentItem': contentItem})


    def parseArtical(self, response):
        contentItem = response.meta['contentItem']
        link = response.url
        contentItem['content_link'] = link

        accountItem = AccountItem()
        curTime = dateUtil.getCurDate()
        accountItem['channel_id'] = self.channel_id
        accountItem['record_class'] = 'channel_info'
        accountItem['crawl_time'] = curTime
        authorNameList = response.xpath('//a[@class="authorName"]/text()').extract()
        authorName = ""
        if len(authorNameList) == 1:
            authorName = authorNameList[0].strip()
        accountItem['account_id'] = authorName
        #print(accountItem)
        yield accountItem

        scriptList = response.xpath('//script[@type="application/ld+json"]/text()').extract()
        if len(scriptList) == 1:
            scriptJson = json.loads(scriptList[0])
            if 'title' in scriptJson:
                contentItem['title'] = scriptJson['title']
            if 'pubDate' in scriptJson:
                contentItem['publish_time'] = scriptJson['pubDate'].strip().replace("T", " ")
        contentItem['account_id'] = authorName
        #print(contentItem)
        yield contentItem

