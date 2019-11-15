# -*- coding: utf-8 -*-
import scrapy
import json
import time

from scrapy.http import FormRequest
from RongCloudChannel.items import ContentItem
from RongCloudChannel.utils import dateUtil
from RongCloudChannel.conf.contentStatusMapping import *
from RongCloudChannel.utils.accountUtil import *


class QutoutiaoSpider(scrapy.Spider):
    name = 'QuTouTiao'
    channel_id = "趣头条"
    dtu = "200"
    loginUrl = "https://qac-qupost.qutoutiao.net/member/login"
    articleUrl = "https://mpapi.qutoutiao.net/content/getList?page={}&isMotherMember=false&token={}&dtu={}"
    videoUrl = "https://mpapi.qutoutiao.net/video/getList?page={}&isMotherMember=false&token={}&dtu={}"

    def __init__(self):
        self.accountDict = getAllAccountByChannel(self.channel_id)


    def start_requests(self):
        for user, password in self.accountDict.items():
            time.sleep(3)
            formdata = {"password": password, "is_secret": "0", "dtu": self.dtu, }
            if user.find("@") > 0:
                formdata["email"] = user
            else:
                formdata["telephone"] = user
                formdata["source"] = "1"
            yield FormRequest(self.loginUrl, method='POST',
                              formdata=formdata, callback=self.parseLoginPage,
                              meta={'formdata': formdata, 'account': user})


    def parseLoginPage(self, response):
        loginInfo = json.loads(response.text)
        if loginInfo['code'] != 0:
            print("登录失败：" + response.text)
            print(response.meta['formdata'])
            return
        account = response.meta['account']
        time.sleep(5)
        yield scrapy.Request(self.articleUrl.format(1, loginInfo['data']['token'], self.dtu),
                             method='GET', callback=self.parseArticlePageJson,
                             meta={'token': loginInfo['data']['token'], 'currentPage': 1, 'totalPage': 1, 'beginFlag': True, 'account': account})
        time.sleep(5)
        yield scrapy.Request(self.videoUrl.format(1, loginInfo['data']['token'], self.dtu),
                             method='GET', callback=self.parseVideoPageJson,
                             meta={'token': loginInfo['data']['token'], 'currentPage': 1, 'totalPage': 1, 'beginFlag': True, 'account': account})


    def parseArticlePageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        account = response.meta['account']
        token = response.meta['token']
        currentPage = response.meta['currentPage']
        totalPage = response.meta['totalPage']
        beginFlag = response.meta['beginFlag']

        rltJson = json.loads(response.text)
        if beginFlag:
            totalPage = rltJson['data']['total_page']
            beginFlag = False
        contentList = rltJson['data']['data']
        curTime = dateUtil.getCurDate()
        for contentInfo in contentList:
            contentItem = ContentItem()
            contentItem['channel_id'] = self.channel_id
            contentItem['account_id'] = account
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

        currentPage += 1
        if currentPage <= totalPage:
            time.sleep(5)
            yield scrapy.Request(
                self.articleUrl.format(currentPage, token, self.dtu),
                method='GET', callback=self.parseArticlePageJson,
                meta={'token': token, 'currentPage': currentPage, 'totalPage': totalPage, 'beginFlag': beginFlag, 'account': account})


    def parseVideoPageJson(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        account = response.meta['account']
        token = response.meta['token']
        currentPage = response.meta['currentPage']
        totalPage = response.meta['totalPage']
        beginFlag = response.meta['beginFlag']
        rltJson = json.loads(response.text)
        if beginFlag:
            totalPage = rltJson['data']['total_page']
            beginFlag = False

        contentList = rltJson['data']['videos']
        curTime = dateUtil.getCurDate()
        for contentInfo in contentList:
            contentItem = ContentItem()
            contentItem['channel_id'] = self.channel_id
            contentItem['account_id'] = account
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

        currentPage += 1
        if currentPage <= totalPage:
            time.sleep(5)
            yield scrapy.Request(self.videoUrl.format(currentPage, token, self.dtu),
                                 method='GET', callback=self.parseVideoPageJson,
                                 meta={'token': token, 'currentPage': currentPage, 'totalPage': totalPage, 'beginFlag': beginFlag, 'account': account})
