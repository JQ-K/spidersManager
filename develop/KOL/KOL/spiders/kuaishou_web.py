#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'
import scrapy
from scrapy.http import Request, FormRequest
import time, sys, os, json, re
from KOL.utils.myredis import RedisClient
#sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from KOL.utils.signatureUtil import *
from KOL.utils.parsepage import *
from KOL.items import KuaiShouUserIterm

class KuaishouwebSpider(scrapy.Spider):
    name = 'kuaishouweb'

    #首页的url由：listPreUrl + listMainUrl + sigPart 拼接而成，
    #其中listMainUrl进行签名计算
    listPreUrl = "https://api.gifshow.com/rest/n/feed/hot?"
    listMainUrl = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&type=7&page={}&coldStart=false&count=20&pv=false&id=6&refreshTimes=2&pcursor=&client_key=3c2cd3f3&os=android"
    sigPart = "&sig={}"

    redis_id_set_name = "KuaiShouUserId"

    redisClient = RedisClient('10.8.26.105', 6379, 1)
    #redisClient = RedisClient('10.8.26.26', 6379, 1)


    def __init__(self, totalPage=1, *args, **kwargs):
        super(KuaishouwebSpider, self).__init__(*args, **kwargs)
        self.totalPage = int(totalPage)
        self.sigUtil = signatureUtil()


    def start_requests(self):
        curPage = 1
        while curPage <= self.totalPage:
            tempUrl = self.listMainUrl.format(curPage)
            curPage += 1
            sig = self.sigUtil.getSig(tempUrl)
            listUrl = self.listPreUrl + tempUrl + self.sigPart.format(sig)
            time.sleep(3)
            yield scrapy.Request(listUrl, method='POST',
                                 callback=self.parseListUrl)


    def parseListUrl(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        if rltJson['result'] != 1:
            print('get list interface error: ' + response.text)
            return
        videoList = rltJson['feeds']
        for videoInfo in videoList:
            # print(videoInfo)
            user_id = videoInfo['user_id']
            #判断user_id是否存在redis
            if self.redisClient.sismember(self.redis_id_set_name, user_id):
                print('user_id exists: ' + str(user_id))
                continue
            share_info = videoInfo["share_info"]
            userId = re.findall("userId=([0-9a-z]+)&", share_info)[0]
            userItem = KuaiShouUserIterm()
            userItem['user_id'] = user_id
            userItem['userId'] = userId
            url = 'https://live.kuaishou.com/profile/{}'.format(userId)
            time.sleep(1)
            try:
                self.getUserInfoByWeb(url, userItem)
            except Exception as e:
                print('parse page error')
                print(e.args)
                continue
            self.redisClient.sadd(self.redis_id_set_name, user_id)
            print('get one item')
            yield userItem


    def getUserInfoByWeb(self, url, userItem):
        r = get_kuai_page(url)
        mapping = get_mapping(r.text)

        # 解析页面
        fan = decrypt_str(re.search('"fan"\s*:\s*"(.*?)"', r.text).group(1), mapping)
        follow = decrypt_str(re.search('"follow"\s*:\s*"(.*?)"', r.text).group(1), mapping)
        photo = decrypt_str(re.search('"photo"\s*:\s*"(.*?)"', r.text).group(1), mapping)
        liked = decrypt_str(re.search('"liked"\s*:\s*"(.*?)"', r.text).group(1), mapping)
        open = decrypt_str(re.search('"open"\s*:\s*"(.*?)"', r.text).group(1), mapping)
        private = decrypt_str(re.search('"private"\s*:\s*"(.*?)"', r.text).group(1), mapping)
        kwaiId = decrypt_str(re.search('"kwaiId"\s*:\s*"(.*?)"', r.text).group(1), mapping)
        eid = decrypt_str(re.search('"eid"\s*:\s*"(.*?)"', r.text).group(1), mapping)
        userId = decrypt_str(re.search('"userId"\s*:\s*"(.*?)"', r.text).group(1), mapping)
        profile = decrypt_str(re.search('"profile"\s*:\s*"([^"]+_s\.jpg)","name"', r.text).group(1), mapping).replace('\\u002F', '/')
        name = decrypt_str(re.search(',"name"\s*:\s*"(.*?)",', r.text).group(1), mapping)
        description = decrypt_str(re.search('"description"\s*:\s*"(.*?)"', r.text).group(1), mapping)
        sex = decrypt_str(re.search('"sex"\s*:\s*"(.*?)"', r.text).group(1), mapping)
        constellation = decrypt_str(re.search('"constellation"\s*:\s*"(.*?)"', r.text).group(1), mapping)
        cityName = decrypt_str(re.search('"cityName"\s*:\s*"(.*?)"', r.text).group(1), mapping)
        '''print(userId)
        print(fan, follow, photo, liked, open, private, kwaiId, eid, userId, profile, name, description, sex,
              constellation, cityName)'''
        userItem['kwaiId'] = kwaiId
        userItem['user_name'] = name
        userItem['user_sex'] = sex
        userItem['user_text'] = description
        userItem['head_url'] = profile
        #userItem['cityCode'] =
        userItem['cityName'] = cityName
        userItem['constellation'] = constellation
        #userItem['article_public'] =
        #userItem['collect'] =
        userItem['fan'] = fan
        userItem['follow'] = follow
        userItem['like'] = liked
        #userItem['moment'] =
        userItem['photo'] = photo
        #userItem['photo_private'] =
        #userItem['photo_public'] =
        userItem['update_time'] = int(time.time())


    def close(self):
        self.redisClient.close()
