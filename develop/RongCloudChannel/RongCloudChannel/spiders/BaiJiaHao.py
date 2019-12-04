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

    #视频:type=v
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

    def start_requests(self):
        print(self.targetDict)
        for targetId, type in self.targetDict.items():
            time.sleep(2)
            yield scrapy.Request(self.url, method='GET', callback='parseVideo')
            break
            if type == 'v':
                scrapy.Request(self.videoAuthorUrl.format(targetId),
                               method='GET', callback=self.parseVideoAuthor, meta={'targetId': targetId})

        #yield scrapy.Request(self.url, method='GET', callback=self.parseVideo)


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
        print(accountItem)
        #yield accountItem



    def parseVideo(self, response):
        #print(response.text)
        url = response.url
        print(url)

        titleList = response.xpath('//h2[@class="videoinfo-title"]/text()').extract()
        title = ""
        print(titleList)
        if len(titleList) == 1:
            title = titleList[0].strip()
        print(title)

        playNumList = response.xpath('//span[starts-with(@class,"videoinfo-playnums")]/text()').extract()
        print(playNumList)
        playNumStr = None
        if len(playNumList) == 1:
            playNumStr = playNumList[0].strip()
        if playNumStr is not None:
            index1 = playNumStr.find("次播放")
            if index1 > 0:
                playNum = playNumStr[0:index1]
                print(playNum)
            publishTimeList = re.findall(r"\d+年\d+月\d+日", playNumStr)
            if len(publishTimeList) == 1:
                publishTime = publishTimeList[0].replace("年", "-").replace("月", "-").replace("日", "") + " 00:00:00"
                print(publishTime)




