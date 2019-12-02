# -*- coding: utf-8 -*-
import scrapy
import json
import time

from scrapy.http import FormRequest
from RongCloudChannel.items import ContentItem
from RongCloudChannel.utils import dateUtil
from RongCloudChannel.utils import pwdUtil
from RongCloudChannel.utils.accountUtil import *


class RenrenSpider(scrapy.Spider):
    name = 'RenRen'
    channel_id = "人人视频"

    loginUrl = "https://ugc-api.rr.tv/user/login"
    videoUrl = "https://ugc-api.rr.tv/video/list"


    def __init__(self):
        self.accountDict = getAllAccountByChannel(self.channel_id)


    def start_requests(self):
        for user, password in self.accountDict.items():
            formdata = {"mobile": user, "password": pwdUtil.md5(password)}
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
            token = rltJson['data']['token']
        except:
            print("登录失败：" + response.text)
            print(response.meta['formdata'])
            return
        time.sleep(5)
        yield scrapy.Request(self.videoUrl, method='GET', callback=self.parseVideoPageJson,
                             headers={'token': token},
                             meta={'account': account})


    def parseVideoPageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        account = response.meta['account']
        rltJson = json.loads(response.text)

        contentList = rltJson['data']
        curTime = dateUtil.getCurDate()
        for contentInfo in contentList:
            contentItem = ContentItem()
            contentItem['channel_id'] = self.channel_id
            contentItem['account_id'] = account
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

