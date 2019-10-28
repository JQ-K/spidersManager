# -*- coding: utf-8 -*-
import scrapy
import json
import redis
import time

from KuaiKanManHua.conf.configure import *
from KuaiKanManHua.items import UserItem


class PostUserSpider(scrapy.Spider):
    name = 'post_user'
    startUrl = "https://social.kkmh.com/v1/graph/feedList/v5?feedType={}&limit=20&since={}&targetId={}"
    headers = {
        'x-device': 'I:4D07310D-AD93-4979-8479-7342A0D5824B',
        'package-id': 'com.kuaikan.comic',
        'hw-model': 'iPhone9,1',
        'kkflowtype': 'NotFree',
        'accept-language': 'zh-Hans-CN;q=1',
        'accept-encoding': 'gzip, deflate, br',
        'muid': 'd41f32dc1f3653dc540d7c9808b18d89',
        'user-agent': 'Kuaikan/5.54.1/554001(iPhone;iOS 13.1.3;Scale/2.00;WiFi;1334*750)',
        'lower-flow': 'No',
        'app-info': 'eyJjYSI6MSwib3YiOiIxMy4xLjMiLCJpZGZhIjoiNjgyOEY2MUQtQzUxMi00RjM1LTlBMzUtMkU2M0QzNUNFQjA3IiwiY3QiOjIwLCJ3aWR0aCI6NzUwLCJ2aXNpdG9yX3NpZ24iOiJiNTRhOTIyYzMwYTVlZDk0NzJmMjdmOWIzYzQ4NmIzZSIsImRwaSI6MzI2LCJoZWlnaHQiOjEzMzQsImlkZnYiOiI0RDA3MzEwRC1BRDkzLTQ5NzktODQ3OS03MzQyQTBENTgyNEIiLCJ2aXNpdG9yX2lkIjoiNEQwNzMxMEQtQUQ5My00OTc5LTg0NzktNzM0MkEwRDU4MjRCIiwiZGV2dCI6MSwiYmQiOiJBcHBsZSIsIm1vZGVsIjoiaVBob25lOSwxIn0=',
        'cookie': 'kk_s_t=1571729453697',
    }


    def __init__(self, feedType=8, targetID=14, sinceID=0, maxUrlNum=100, waitSeconds=1, *args, **kwargs):
        super(PostUserSpider, self).__init__(*args, **kwargs)
        self.params = {
            'feedType': int(feedType),
            'targetID': int(targetID),
            'sinceID': int(sinceID),
            'maxUrlNum': int(maxUrlNum),
            'waitSeconds': int(waitSeconds),
        }
        self.spiderUrlNums = 0
        # connect redis
        self.pool = redis.ConnectionPool(host=redisHost, port=redisPort, db=redisDb)
        self.r = redis.Redis(connection_pool=self.pool)


    def start_requests(self):
        yield scrapy.Request(
            self.startUrl.format(self.params['feedType'], self.params['sinceID'], self.params['targetID']),
            callback=self.parsePageJson, method='GET', headers=self.headers)


    def parsePageJson(self, response):
        if response.status != 200:
            return
        rltJson = json.loads(response.text)
        since = rltJson['data']['since']
        infoList = rltJson['data']['universalModels']
        rltUserInfoList = []

        for info in infoList:
            if 'latestVPosts' in info:
                latestUserList = info['latestVPosts']
                for latestUser in latestUserList:
                    user = latestUser['user']
                    id = user['id']
                    avatar_url = user['avatar_url']
                    nickname = user['nickname'].strip().replace('\t', '').replace('\n', '').replace('\r', '')
                    intro = user['intro'].strip().replace('\t', '').replace('\n', '').replace('\r', '')
                    # 添加至结果列表
                    rltUserInfoList.append((id, avatar_url, nickname, intro))
            if 'post' in info:
                user = info['post']['user']
                id = user['id']
                avatar_url = user['avatar_url']
                nickname = user['nickname'].strip().replace('\t', '').replace('\n', '').replace('\r', '')
                intro = user['intro'].strip().replace('\t', '').replace('\n', '').replace('\r', '')
                rltUserInfoList.append((id, avatar_url, nickname, intro))
        print(response.url)

        for info in rltUserInfoList:
            item = UserItem()
            item['user_id'] = info[0]  # int
            item['pic_url'] = info[1]
            item['nickname'] = info[2]
            item['sign_text'] = info[3]
            yield item

        if (-1 != since) and (self.spiderUrlNums < self.params['maxUrlNum']):
            self.spiderUrlNums += 1
            if self.spiderUrlNums % 100 == 0:
                time.sleep(5)
            yield scrapy.Request(
                self.startUrl.format(self.params['feedType'], since, self.params['targetID']),
                callback=self.parsePageJson, method='GET', headers=self.headers)


    def close(self):
        self.pool.disconnect()


