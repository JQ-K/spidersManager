# -*- coding: utf-8 -*-
import scrapy
import json
import time

from KOL.items import KuaiShouUserIterm
from KOL.utils.signatureUtil import *

class KuaishouSpider(scrapy.Spider):
    name = 'kuaishou'

    #首页的url由：listPreUrl + listMainUrl + sigPart 拼接而成，其中listMainUrl进行签名计算
    listPreUrl = "https://api.gifshow.com/rest/n/feed/hot?"
    listMainUrl = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&type=7&page={}&coldStart=false&count=20&pv=false&id=6&refreshTimes=2&pcursor=&client_key=3c2cd3f3&os=android"

    #用户信息的url由：userPreUrl + userMainUrl + sigPart 拼接而成，其中userMainUrl进行签名计算
    userPreUrl = "https://api.gifshow.com/rest/n/user/profile/v2?"
    userMainUrl = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&user={}&client_key=3c2cd3f3&os=android"

    #用户作品列表页url由：photoPreUrl + photoMainUrl + sigPart拼接而成，其中photoMainUrl进行签名计算
    photoPreUrl = "http://api.gifshow.com/rest/n/feed/profile2?"
    photoMainUrl = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&token=&user_id={}&lang=zh&count=30&privacy=public&referer=ks%3A%2F%2Fprofile%2F605395700%2F5221360837644739313%2F1_a%2F2000005775957550673_h495%2F8&client_key=3c2cd3f3&os=android"

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
        #super(KuaishouSpider, self).__init__(*args, **kwargs)
        #self.totalPage = int(totalPage)
        self.totalPage = 1
        self.sigUtil = signatureUtil()


    def start_requests(self):
        curPage = 1
        self.totalPage = 1
        while curPage <= self.totalPage:
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
            print('get list interface error: ' + response.text)
            return
        videoList = rltJson['feeds']
        for videoInfo in videoList:
            user_id = videoInfo['user_id']
            #print(user_id)
            tempUrl = self.userMainUrl.format(user_id)
            sig = self.sigUtil.getSig(tempUrl)
            userUrl = self.userPreUrl + tempUrl + self.sigPart.format(sig)
            time.sleep(1)
            #print('userUrl:')
            #print(userUrl)
            yield scrapy.Request(userUrl, method='POST', #headers=self.headers,
                                 callback=self.parseUserInfoUrl)


    def parseUserInfoUrl(self, response):
        #print(response.text)
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        if rltJson['result'] != 1:
            print('get user interface error: ' + response.text)
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
        #yield userItem




