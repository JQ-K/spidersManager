# -*- coding: utf-8 -*-
import scrapy
import time
import json

from RongCloudChannel.utils.targetIdUtil import *
from RongCloudChannel.items import *
from RongCloudChannel.utils import dateUtil


class WangyihaoSpider(scrapy.Spider):
    name = 'WangYiHao'
    channel_id = '网易号'

    vid = "VZQ286CKP"
    videoUrl = 'https://gw.m.163.com/nc-gateway/api/v1/video/detail/{}'  #json
    videoUrlDemo = 'https://v.163.com/static/1/{}.html'

    tid = "EVNRO15405468U2Q"
    articalUrl = 'https://dy.163.com/v2/article/detail/{}.html' #html parse


    def __init__(self):
        #self.targetDict = getAllTargetIdByChannel(self.channel_id)
        self.targetDict = {'VZQK6PRKS': 'h',
                           'ERI0JDJV05468U2Q': 't',
                           'EVNRO15405468U2Q': 't',}


    def start_requests(self):
        #print(self.targetDict)
        for targetId, targetType in self.targetDict.items():
            time.sleep(2)
            if targetType == 'h':
                yield scrapy.Request(self.videoUrl.format(targetId),
                                     method='GET', callback=self.parseVideoPage, meta={'targetId': targetId})
            if targetType == 't':
                yield scrapy.Request(self.articalUrl.format(targetId),
                                     method='GET', callback=self.parseArticalPage, meta={'targetId': targetId})


    def parseVideoPage(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        targetId = response.meta['targetId']
        rltJson = json.loads(response.text)
        if rltJson['code'] != 0:
            return
        if 'data' not in rltJson:
            return
        curTime = dateUtil.getCurDate()
        account_id = ""
        if 'videoTopic' in rltJson['data']:
            accountItem = AccountItem()
            accountItem['channel_id'] = self.channel_id
            accountItem['record_class'] = 'channel_info'
            accountItem['crawl_time'] = curTime
            if 'tname' in rltJson['data']['videoTopic']:
                account_id = rltJson['data']['videoTopic']['tname']
                accountItem['account_id'] = account_id
                print(accountItem)
                #yield accountItem
        if 'title' not in rltJson['data']:
            return
        contentItem = ContentItem()
        contentItem['channel_id'] = self.channel_id
        contentItem['account_id'] = account_id
        contentItem['record_class'] = 'content_info'
        contentItem['crawl_time'] = curTime
        contentItem['id'] = targetId
        contentItem['title'] = rltJson['data']['title']
        contentItem['content_link'] = self.videoUrlDemo.format(targetId)
        if 'ptime' in rltJson['data']:
            contentItem['publish_time'] = rltJson['data']['ptime']
        if 'playCount' in rltJson['data']:
            contentItem['read_count'] = rltJson['data']['playCount']
        if 'replyCount' in rltJson['data']:
            contentItem['comment_count'] = rltJson['data']['replyCount']
        print(contentItem)
        #yield contentItem


    def parseArticalPage(self, response):
        pass


