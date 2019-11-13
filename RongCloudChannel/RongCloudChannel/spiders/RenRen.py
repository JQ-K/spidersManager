# -*- coding: utf-8 -*-
import scrapy
import json
import time

from scrapy.http import FormRequest
from RongCloudChannel.items import ContentItem
from RongCloudChannel.utils import dateUtil
from RongCloudChannel.utils import pwdUtil
from RongCloudChannel.utils.mysqlUtil import MysqlClient
from RongCloudChannel.conf.configure import *


class RenrenSpider(scrapy.Spider):
    name = 'RenRen'
    channel_id = "人人视频"

    loginUrl = "https://ugc-api.rr.tv/user/login"
    videoUrl = "https://ugc-api.rr.tv/video/list"


    def __init__(self):
        self.mysqlClient = MysqlClient.from_settings(DB_CONF_DIR)
        self.channelIdList = self.mysqlClient.getChannelIdList(TB_AUTH_NAME, self.channel_id)


    def start_requests(self):
        for channelId in self.channelIdList:
            userAndPwd = self.mysqlClient.getUserAndPwdByChannelId(TB_AUTH_NAME, channelId)
            if userAndPwd is None:
                continue
            formdata = {"mobile": userAndPwd[0], "password": pwdUtil.md5(userAndPwd[1])}
            time.sleep(3)
            yield FormRequest(self.loginUrl, method='POST',
                              formdata=formdata, callback=self.parseLoginPage, meta={'formdata': formdata})


    def parseLoginPage(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        try:
            token = rltJson['data']['token']
        except:
            print("登录失败：" + response.text)
            print(response.meta['formdata'])
            return
        time.sleep(5)
        yield scrapy.Request(self.videoUrl, method='GET', callback=self.parseVideoPageJson,
                             headers={'token': token})


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


    def close(self):
        self.mysqlClient.close()