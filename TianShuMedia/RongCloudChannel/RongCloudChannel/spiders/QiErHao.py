# -*- coding: utf-8 -*-
import scrapy
import time
import json

from RongCloudChannel.utils.targetIdUtil import *
from RongCloudChannel.items import *
from RongCloudChannel.utils import dateUtil

class QierhaoSpider(scrapy.Spider):
    name = 'QiErHao'
    channel_id = '企鹅号'

    contentLinkDemo = "https://kuaibao.qq.com/s/{}00"

    videoUrl = "https://kuaibao.qq.com/getVideoRelate?id={}00"
    articalUrl = "https://kuaibao.qq.com/getSubNewsContent?id={}00"


    def __init__(self):
        self.targetDict = getAllTargetIdByChannel(self.channel_id)
        '''self.targetDict = {'20191118V0OC25': 'h',
                           '20191118A0DUG6': 't',}'''


    def start_requests(self):
        for targetId, targetType in self.targetDict.items():
            time.sleep(2)
            if targetType == 'h':
                yield scrapy.Request(self.videoUrl.format(targetId),
                                     method='GET', callback=self.parseVideoUrl, meta={'targetId': targetId})
            if targetType == 't':
                yield scrapy.Request(self.articalUrl.format(targetId),
                                     method='GET', callback=self.parseArticalUrl, meta={'targetId': targetId})


    def parseVideoUrl(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        targetId = response.meta['targetId']
        rltJson = json.loads(response.text)
        if rltJson['ret'] != 0:
            print(targetId + ' response error: ' + response.text)
        curTime = dateUtil.getCurDate()
        account_id = ''
        if 'cardInfo' in rltJson:
            accountItem = AccountItem()
            accountItem['channel_id'] = self.channel_id
            accountItem['record_class'] = 'channel_info'
            accountItem['crawl_time'] = curTime
            if 'chlname' in rltJson['cardInfo']:
                account_id = rltJson['cardInfo']['chlname']
            accountItem['account_id'] = account_id
            if 'subCount' in rltJson['cardInfo']:
                accountItem['total_subscribe_count'] = rltJson['cardInfo']['subCount']
            #print(accountItem)
            yield accountItem
        if 'videoinfo' in rltJson:
            contentItem = ContentItem()
            contentItem['channel_id'] = self.channel_id
            contentItem['account_id'] = account_id
            contentItem['record_class'] = 'content_info'
            contentItem['crawl_time'] = curTime
            contentItem['id'] = targetId
            contentItem['content_link'] = self.contentLinkDemo.format(targetId)
            if 'title' in rltJson['videoinfo']:
                contentItem['title'] = rltJson['videoinfo']['title']
            if 'pubTime' in rltJson['videoinfo']:
                contentItem['publish_time'] = rltJson['videoinfo']['pubTime']
            if 'playcount' in rltJson['videoinfo']:
                contentItem['read_count'] = rltJson['videoinfo']['playcount']
            #print(contentItem)
            yield contentItem


    def parseArticalUrl(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        targetId = response.meta['targetId']
        rltJson = json.loads(response.text)
        if rltJson['ret'] != 0:
            print(targetId + ' response error: ' + response.text)
        curTime = dateUtil.getCurDate()
        account_id = ''
        if 'card' in rltJson:
            accountItem = AccountItem()
            accountItem['channel_id'] = self.channel_id
            accountItem['record_class'] = 'channel_info'
            accountItem['crawl_time'] = curTime
            if 'chlname' in rltJson['card']:
                account_id = rltJson['card']['chlname']
            accountItem['account_id'] = account_id
            if 'subCount' in rltJson['card']:
                accountItem['total_subscribe_count'] = rltJson['card']['subCount']
            #print(accountItem)
            yield accountItem
        if 'title' in rltJson:
            contentItem = ContentItem()
            contentItem['title'] = rltJson['title']
            contentItem['channel_id'] = self.channel_id
            contentItem['account_id'] = account_id
            contentItem['record_class'] = 'content_info'
            contentItem['crawl_time'] = curTime
            contentItem['id'] = targetId
            contentItem['content_link'] = self.contentLinkDemo.format(targetId)
            if 'pub_time' in rltJson:
                contentItem['publish_time'] = rltJson['pub_time']
            if 'count_info' in rltJson:
                if 'comments' in rltJson['count_info']:
                    contentItem['comment_count'] = rltJson['count_info']['comments']
                if 'share_count' in rltJson['count_info']:
                    contentItem['share_count'] = rltJson['count_info']['share_count']
            #print(contentItem)
            yield contentItem
