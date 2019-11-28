#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'
import scrapy
from scrapy.http import Request,FormRequest
import time,sys,os,json,re
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from KOL.utils.signatureUtil import *
from KOL.utils.parsepage import *

class Kuaishou1Spider(scrapy.Spider):
    name = 'kuaishou1'

    #首页的url由：listPreUrl + listMainUrl + sigPart 拼接而成，其中listMainUrl进行签名计算
    listPreUrl = "https://api.gifshow.com/rest/n/feed/hot?"
    listMainUrl = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&type=7&page={}&coldStart=false&count=20&pv=false&id=6&refreshTimes=2&pcursor=&client_key=3c2cd3f3&os=android"
    sigPart = "&sig={}"

    def __init__(self, totalPage=1, *args, **kwargs):
        super(Kuaishou1Spider, self).__init__(*args, **kwargs)
        self.totalPage = int(totalPage)
        self.sigUtil = signatureUtil()

    def start_requests(self):
        curPage = 1
        self.totalPage = 5
        while curPage <= self.totalPage:
            tempUrl = self.listMainUrl.format(curPage)
            curPage += 1
            sig = self.sigUtil.getSig(tempUrl)
            listUrl = self.listPreUrl + tempUrl + self.sigPart.format(sig)
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
            share_info = videoInfo["share_info"]
            user_id = re.findall( "userId=([0-9a-z]+)&",share_info)[0]
            url = 'https://live.kuaishou.com/profile/{}'.format(user_id)
            r = get_kuai_page(url)
            mapping = get_mapping(r.text)

            # 解析页面
            fan = decrypt_str(re.search('"fan"\s*:\s*"(.*?)"', r.text).group(1),mapping)
            follow = decrypt_str(re.search('"follow"\s*:\s*"(.*?)"', r.text).group(1), mapping)
            photo = decrypt_str(re.search('"photo"\s*:\s*"(.*?)"', r.text).group(1), mapping)
            liked = decrypt_str(re.search('"liked"\s*:\s*"(.*?)"', r.text).group(1), mapping)
            open = decrypt_str(re.search('"open"\s*:\s*"(.*?)"', r.text).group(1), mapping)
            private = decrypt_str(re.search('"private"\s*:\s*"(.*?)"', r.text).group(1), mapping)
            kwaiId = decrypt_str(re.search('"kwaiId"\s*:\s*"(.*?)"', r.text).group(1), mapping)
            eid = decrypt_str(re.search('"eid"\s*:\s*"(.*?)"', r.text).group(1), mapping)
            userId = decrypt_str(re.search('"userId"\s*:\s*"(.*?)"', r.text).group(1), mapping)
            profile = decrypt_str(re.search('"profile"\s*:\s*"(.*?)"', r.text).group(1), mapping).replace('\\u002F','/')
            name = decrypt_str(re.search(',"name"\s*:\s*"(.*?)",', r.text).group(1), mapping)
            description = decrypt_str(re.search('"description"\s*:\s*"(.*?)"', r.text).group(1), mapping)
            sex = decrypt_str(re.search('"sex"\s*:\s*"(.*?)"', r.text).group(1), mapping)
            constellation = decrypt_str(re.search('"constellation"\s*:\s*"(.*?)"', r.text).group(1), mapping)
            cityName = decrypt_str(re.search('"cityName"\s*:\s*"(.*?)"', r.text).group(1), mapping)
            print(user_id)
            print(fan,follow,photo,liked,open,private,kwaiId,eid,userId,profile,name,description,sex,constellation,cityName)
            break
