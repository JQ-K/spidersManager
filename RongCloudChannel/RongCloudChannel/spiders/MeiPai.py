# -*- coding: utf-8 -*-
import scrapy
import time
import json

from scrapy.http import FormRequest
from RongCloudChannel.items import ContentItem
from RongCloudChannel.utils import dateUtil
from RongCloudChannel.utils.accountUtil import *


class MeipaiSpider(scrapy.Spider):
    name = 'MeiPai'
    channel_id = "美拍"

    host = "https://www.meipai.com"
    videoListUrl = "https://www.meipai.com/user/{}"
    loginUrl = "https://account.meitu.com/oauth/access_token.json"

    '''headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    }'''

    def __init__(self):
        self.accountDict = getAllAccountByChannel(self.channel_id)

    def start_requests(self):
        for user, password in self.accountDict.items():
            formdata = {"client_id": "1189857310",
                        "password": password,
                        "phone": user,
                        "phone_cc": "86",
                        "grant_type": "phone"}
            time.sleep(3)
            yield FormRequest(self.loginUrl, method='POST',
                              formdata=formdata,
                              callback=self.parseLoginPage,
                              meta={'formdata': formdata, 'account': user})


    def parseLoginPage(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        try:
            rltJson = json.loads(response.text)
            userId = str(rltJson['response']['user']['id'])
        except:
            print('登录失败:' + response.text)
            print(response.meta['formdata'])
            return
        account = response.meta['account']
        yield scrapy.Request(self.videoListUrl.format(userId),
                             method='GET', callback=self.parseVideoList, meta={'account': account})


    def parseVideoList(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        account = response.meta['account']
        videoHrefList = response.xpath('//a[@itemprop="description"]/@href').extract()
        uploadDateList = response.xpath('//meta[@itemprop="uploadDate"]/@content').extract()
        for videoHref, uploadDate in zip(videoHrefList, uploadDateList):
            time.sleep(5)
            yield scrapy.Request(self.host + videoHref, method='GET',
                                 callback=self.parseVideoInfo,
                                 #headers=self.headers,
                                 meta={'uploadDate': uploadDate, 'account': account})

        nextPageHrefList = response.xpath('//a[@class="paging-next dbl"]/@href').extract()

        if len(nextPageHrefList) == 1:
            time.sleep(5)
            yield scrapy.Request(self.host + nextPageHrefList[0],
                                 method='GET', callback=self.parseVideoList, meta={'account': account})


    def parseVideoInfo(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        account = response.meta['account']
        url = response.url
        id = url.split("/")[-1]
        uploadDate = response.meta['uploadDate']

        titleList = response.xpath('//h1[starts-with(@class,"detail-cover-title")]/text()').extract()
        title = ""
        if len(titleList) == 1:
            title = titleList[0].strip()

        publishTimeList = response.xpath('//div[@itemprop="datePublished"]/strong/text()').extract()
        temp_publish_time = ""
        if len(publishTimeList) == 1:
            temp_publish_time = publishTimeList[0].strip()
        if temp_publish_time.find("分钟前") >= 0:
            try:
                minute_count = int(temp_publish_time.replace("分钟前", ""))
            except:
                minute_count = 0
            publish_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-minute_count*60))
        else:
            temp_publish_time += ":00"
            temp_publish_time = temp_publish_time.replace("今天", "")
            temp_time = temp_publish_time.split(" ")[-1]
            publish_time = uploadDate + " " + temp_time


        playCountList = response.xpath('//div[@class="detail-location"]/text()').extract()
        play_count = 0
        if len(playCountList) == 2:
            try:
                play_count = int(playCountList[-1].strip().replace("播放", ""))
            except:
                play_count = 0

        likeCountList = response.xpath('//span[@itemprop="ratingCount"]/text()').extract()
        like_count = 0
        if len(likeCountList) == 1:
            try:
                like_count = int(likeCountList[0].strip())
            except:
                like_count = 0

        commentCountList = response.xpath('//span[@itemprop="reviewCount"]/text()').extract()
        comment_count = 0
        if len(commentCountList) == 1:
            try:
                comment_count = int(commentCountList[0].strip())
            except:
                comment_count = 0

        shareCountList = response.xpath('//span[@class="pr top-3"]/text()').extract()
        share_count = 0
        if len(shareCountList) == 2:
            try:
                share_count = int(shareCountList[1].strip().replace("分享", ""))
            except:
                share_count = 0

        curTime = dateUtil.getCurDate()
        contentItem = ContentItem()
        contentItem['channel_id'] = self.channel_id
        contentItem['account_id'] = account
        contentItem['record_class'] = "content_info"
        contentItem['crawl_time'] = curTime
        contentItem['id'] = id
        contentItem['title'] = title
        contentItem['content_link'] = url
        contentItem['publish_time'] = publish_time
        contentItem['read_count'] = play_count
        contentItem['comment_count'] = comment_count
        contentItem['share_count'] = share_count
        contentItem['like_count'] = like_count
        yield contentItem
