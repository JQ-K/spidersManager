# -*- coding: utf-8 -*-
import scrapy
import time

from RongCloudChannel.utils.targetIdUtil import *

class QierhaoSpider(scrapy.Spider):
    name = 'QiErHao'
    channel_id = '企鹅号'

    videoUrl = "https://kuaibao.qq.com/getVideoRelate?id={}00"
    articalUrl = "https://kuaibao.qq.com/getSubNewsContent?id={}00"


    def __init__(self):
        #self.targetDict = getAllTargetIdByChannel(self.channel_id)
        self.targetDict = {'20191118V0OC25': 'h',
                           '20191118A0DUG6': 't',}


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


    def parseArticalUrl(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
