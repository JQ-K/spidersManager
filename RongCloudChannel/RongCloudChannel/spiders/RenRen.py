# -*- coding: utf-8 -*-
import scrapy
import json
import time

from scrapy.http import FormRequest
from RongCloudChannel.conf.channelAccount import *
from RongCloudChannel.items import ContentItem
from RongCloudChannel.utils import dateUtil
from RongCloudChannel.utils import pwdUtil


class RenrenSpider(scrapy.Spider):
    name = 'RenRen'
    channel_id = "人人"

    loginUrl = "https://ugc-api.rr.tv/user/login"
    videoUrl = "https://ugc-api.rr.tv/video/list"


    def start_requests(self):
        for user, password in account[self.channel_id].items():
            formData = {"mobile": user, "password": pwdUtil.md5(password)}
            yield FormRequest(self.loginUrl, method='POST',
                              formdata=formData, callback=self.parseLoginPage)


    def parseLoginPage(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        token = rltJson['data']['token']
        print(token)
        yield scrapy.Request(self.videoUrl, method='GET', callback=self.parseVideoPageJson,
                             headers={'token':token})


    def parseVideoPageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)

        contentList = rltJson['data']
        curTime = dateUtil.getCurDate()
        for contentInfo in contentList:
            contentItem = ContentItem()
            contentItem['channel_id'] = self.channel_id
            contentItem['record_class'] = "content_info"
            contentItem['crawl_time'] = curTime
            contentItem['id'] = contentInfo['id']
            contentItem['title'] = contentInfo['title']
            contentItem['content_link'] = contentInfo['playLink']
            contentItem['publish_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime((int(contentInfo['createTime']))/1000))
            contentItem['read_count'] = contentInfo['playCount']
            contentItem['comment_count'] = contentInfo['commentCount']
            contentItem['like_count'] = contentInfo['likeCount']
            yield contentItem

