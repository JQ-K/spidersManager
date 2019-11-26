# -*- coding: utf-8 -*-
import scrapy
import json
import time

from KOL.items import KuaiShouUserIterm
from KOL.utils.signatureUtil import *

class KuaishouSpider(scrapy.Spider):
    name = 'kuaishou'

    listPreUrl = "https://api.gifshow.com/rest/n/feed/hot?"
    listMainUrl = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&type=7&page={}&coldStart=false&count=20&pv=false&id=6&refreshTimes=2&pcursor=&client_key=3c2cd3f3&os=android"

    userPreUrl = "https://api.gifshow.com/rest/n/user/profile/v2?"
    userMainUrl = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&user={}&client_key=3c2cd3f3&os=android"

    sigPart = "&sig={}"

    headers = {
        'X-REQUESTID': '1328313',
        'User-Agent': 'kwai-android',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '144',
        'Host': 'api.gifshow.com',
        'Accept-Encoding': 'gzip',
    }


    def __init__(self):
        self.sigUtil = signatureUtil()


    def start_requests(self):
        curPage = 1
        totalPage = 1
        while curPage <= totalPage:
            tempUrl = self.listMainUrl.format(curPage)
            curPage += 1
            sig = self.sigUtil.getSig(tempUrl)
            listUrl = self.listPreUrl + tempUrl + self.sigPart.format(sig)
            time.sleep(2)
            yield scrapy.Request(listUrl, method='POST', #headers=self.headers,
                                 callback=self.parseListUrl)


    def parseListUrl(self, response):
        #print(response.text)
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        if rltJson['result'] != 1:
            print('get interface error: ' + response.text)
            return
        videoList = rltJson['feeds']
        for videoInfo in videoList:
            user_id = videoInfo['user_id']
            print(user_id)
            tempUrl = self.userMainUrl.format(user_id)
            sig = self.sigUtil.getSig(tempUrl)
            userUrl = self.userPreUrl + tempUrl + self.sigPart.format(sig)
            time.sleep(1)
            print('userUrl:')
            print(userUrl)
            yield scrapy.Request(userUrl, method='POST', #headers=self.headers,
                                 callback=self.parseUserInfoUrl)


    def parseUserInfoUrl(self, response):
        #print(response.text)
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        if rltJson['result'] != 1:
            print('get interface error: ' + response.text)
            return
        userInfo = rltJson['userProfile']
        self.getUserInfoItem(userInfo)


    def getUserInfoItem(self, userInfo):
        userItem = KuaiShouUserIterm()
        if 'profile' in userInfo:
            userProfile = userInfo['profile']
            if 'kwaiId' in userProfile:
                userItem['kwaiId'] = userProfile['kwaiId']
            if 'user_id' in userProfile:
                userItem['user_id'] = userProfile['user_id']
            if 'user_name' in userProfile:
                userItem['user_name'] = userProfile['user_name']
            if 'user_sex' in userProfile:
                userItem['user_sex'] = userProfile['user_sex']
            if 'user_text' in userProfile:
                userItem['user_text'] = userProfile['user_text']
            if 'headurl' in userProfile:
                userItem['head_url'] = userProfile['headurl']

        if 'cityCode' in userInfo:
            userItem['cityCode'] = userInfo['cityCode']
        if 'cityName' in userInfo:
            userItem['cityName'] = userInfo['cityName']
        if 'constellation' in userInfo:
            userItem['constellation'] = userInfo['constellation']

        if 'ownerCount' in userInfo:
            ownerCount = userInfo['ownerCount']
            if 'article_public' in ownerCount:
                userItem['article_public'] = ownerCount['article_public']
            if 'collect' in ownerCount:
                userItem['collect'] = ownerCount['collect']
            if 'fan' in ownerCount:
                userItem['fan'] = ownerCount['fan']
            if 'follow' in ownerCount:
                userItem['follow'] = ownerCount['follow']
            if 'like' in ownerCount:
                userItem['like'] = ownerCount['like']
            if 'moment' in ownerCount:
                userInfo['moment'] = ownerCount['moment']
            if 'photo' in ownerCount:
                userInfo['photo'] = ownerCount['photo']
            if 'photo_private' in ownerCount:
                userItem['photo_private'] = ownerCount['photo_private']
            if 'photo_public' in ownerCount:
                userItem['photo_public'] = ownerCount['photo_public']
        #userItem['user_info_json'] = userInfo
        print(userItem)




