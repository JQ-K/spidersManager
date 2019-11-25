# -*- coding: utf-8 -*-
import scrapy
import json
import time

from KOL.items import KuaiShouUserIterm;
from KOL.utils.signatureUtil import *

class KuaishouSpider(scrapy.Spider):
    name = 'kuaishou'

    testUserUrl = "http://api.gifshow.com/rest/n/user/profile/v2?mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&user=737297724&client_key=3c2cd3f3&os=android&sig=a6c962b318939cf43a39655e332f2cf9"

    listPreUrl = "http://api.gifshow.com/rest/n/feed/hot?"
    listMainUrl = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&type=7&page={}&coldStart=false&count=20&pv=false&id=6&refreshTimes=2&pcursor=&client_key=3c2cd3f3&os=android"

    userPreUrl = "http://api.gifshow.com/rest/n/user/profile/v2?"
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
        '''yield scrapy.Request(self.testUserUrl, method='POST',  # headers=self.headers,
                             callback=self.parseUserInfoUrl)'''
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
        userItem = KuaiShouUserIterm()
        #userItem['kwaiId'] =
        userItem['user_id'] = userInfo['profile']['user_id']
        userItem['user_name'] = userInfo['profile']['user_name']
        userItem['user_sex'] = userInfo['profile']['user_sex']
        userItem['user_text'] = userInfo['profile']['user_text']
        userItem['head_url'] = userInfo['profile']['headurl']
        userItem['cityCode'] = userInfo['cityCode']
        userItem['cityName'] = userInfo['cityName']
        userItem['constellation'] = userInfo['constellation']
        userItem['article_public'] = userInfo['ownerCount']['article_public']
        userItem['collect'] = userInfo['ownerCount']['collect']
        userItem['fan'] = userInfo['ownerCount']['fan']
        userItem['follow'] = userInfo['ownerCount']['follow']
        userItem['like'] = userInfo['ownerCount']['like']
        userInfo['monent'] = userInfo['ownerCount']['moment']
        userInfo['photo'] = userInfo['ownerCount']['photo']
        userItem['photo_private'] = userInfo['ownerCount']['photo_private']
        userItem['photo_public'] = userInfo['ownerCount']['photo_public']
        #userItem['user_info_json'] = userInfo
        print(userItem)



