# -*- coding: utf-8 -*-
import scrapy
import json
import time

from scrapy.http import FormRequest
from RongCloudChannel.conf.channelAccount import *
from RongCloudChannel.items import ContentItem
from RongCloudChannel.utils import dateUtil
from RongCloudChannel.conf.contentStatusMapping import *


class QutoutiaoSpider(scrapy.Spider):
    name = 'QuTouTiao'
    channel_id = "趣头条"
    dtu = "200"
    loginUrl = "https://qac-qupost.qutoutiao.net/member/login"
    articleUrl = "https://mpapi.qutoutiao.net/content/getList?page={}&isMotherMember=false&token={}&dtu={}"
    videoUrl = "https://mpapi.qutoutiao.net/video/getList?page={}&isMotherMember=false&token={}&dtu={}"

    def __init__(self):
        self.loginInfo = {}
        self.articleCurrentPage = 1
        self.articleTotalPage = 1
        self.articleBeginFlag = True
        self.videoCurrentPage = 1
        self.videoTotalPage = 1
        self.videoBeginFlag = True


    def start_requests(self):
        for user, password in account['趣头条'].items():
            time.sleep(3)
            yield FormRequest(self.loginUrl, method='POST',
                              formdata={"email": user,
                                        "password": password,
                                        "is_secret": "0",
                                        "dtu": self.dtu,
                                        # "telephone":"",
                                        # "keep":"",
                                        # "captcha":"",
                                        # "source":"0",
                                        # "k":"",
                                        # "token":"undefined",
                                        }, callback=self.parseLoginPage)


    def parseLoginPage(self, response):
        self.loginInfo = json.loads(response.text)
        if self.loginInfo['code'] != 0:
            print("登录失败：" + response.text)
            return
        time.sleep(5)
        yield scrapy.Request(self.articleUrl.format(self.articleCurrentPage, self.loginInfo['data']['token'], self.dtu),
                             method='GET', callback=self.parseArticlePageJson)
        time.sleep(5)
        yield scrapy.Request(self.videoUrl.format(self.videoCurrentPage, self.loginInfo['data']['token'], self.dtu),
                             method='GET', callback=self.parseVideoPageJson)


    def parseArticlePageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        if self.articleBeginFlag:
            self.articleTotalPage = rltJson['data']['total_page']
            self.articleBeginFlag = False
        contentList = rltJson['data']['data']
        curTime = dateUtil.getCurDate()
        for contentInfo in contentList:
            contentItem = ContentItem()
            contentItem['channel_id'] = self.channel_id
            contentItem['record_class'] = "content_info"
            contentItem['crawl_time'] = curTime
            contentItem['id'] = contentInfo['id']
            contentItem['title'] = contentInfo['title']
            contentItem['content_link'] = contentInfo['url']
            contentItem['publish_time'] = contentInfo['publish_time']
            contentItem['read_count'] = contentInfo['pv']
            contentItem['comment_count'] = contentInfo['comment_num']
            contentItem['share_count'] = contentInfo['share_num']
            contentItem['collect_count'] = contentInfo['fav_num']
            contentItem['recommend_count'] = contentInfo['rec_show_pv']
            status = int(contentInfo['status']) #趣头条：1-草稿；5-待审核；2-已发布；3-审核失败；4-回收站
            contentItem['publish_status'] = publicContentStatus[channelContentStatus[self.channel_id]['article'][status]]
            yield contentItem

        self.articleCurrentPage += 1
        if self.articleCurrentPage <= self.articleTotalPage:
            time.sleep(5)
            yield scrapy.Request(
                self.articleUrl.format(self.articleCurrentPage, self.loginInfo['data']['token'], self.dtu),
                method='GET', callback=self.parseArticlePageJson)


    def parseVideoPageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        if self.videoBeginFlag:
            self.videoTotalPage = rltJson['data']['total_page']
            self.videoBeginFlag = False

        contentList = rltJson['data']['videos']
        curTime = dateUtil.getCurDate()
        for contentInfo in contentList:
            contentItem = ContentItem()
            contentItem['channel_id'] = self.channel_id
            contentItem['record_class'] = "content_info"
            contentItem['crawl_time'] = curTime
            contentItem['id'] = contentInfo['id']
            contentItem['title'] = contentInfo['title']
            contentItem['content_link'] = contentInfo['url']
            contentItem['publish_time'] = contentInfo['update_at']
            contentItem['read_count'] = contentInfo['pv']
            contentItem['comment_count'] = contentInfo['comment_num']
            contentItem['share_count'] = contentInfo['share_num']
            contentItem['collect_count'] = contentInfo['fav_num']
            contentItem['recommend_count'] = contentInfo['rec_show_pv']
            status = int(contentInfo['status'])  # 趣头条：0-草稿；2-待审核；4-已发布；3-审核失败；5-回收站
            contentItem['publish_status'] = publicContentStatus[channelContentStatus[self.channel_id]['video'][status]]
            yield contentItem

        self.videoCurrentPage += 1
        if self.videoCurrentPage <= self.videoTotalPage:
            time.sleep(5)
            yield scrapy.Request(self.videoUrl.format(self.videoCurrentPage, self.loginInfo['data']['token'], self.dtu),
                                 method='GET', callback=self.parseVideoPageJson)

