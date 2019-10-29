# -*- coding: utf-8 -*-
import scrapy
import json
import time

from KuaiKanManHua.items import UserItem
from KuaiKanManHua.conf.configure import *
from KuaiKanManHua.utils.myredis import RedisClient


class ReplyUserSpider(scrapy.Spider):
    name = 'reply_user'
    userContentUrl = "https://social.kkmh.com/v1/graph/users/{}/posts?limit=20&since={}"
    userCommentUrl = "https://social.kkmh.com/v1/graph/posts/{}/comments/v5?filter=1&limit=10&since={}"
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


    def __init__(self):
        self.spiderUrlNums = 0
        # connect redis
        self.redisClient = RedisClient.from_settings(DB_CONF_DIR)
        self.idSet = self.redisClient.smembers(REDIS_KEY['user_id'])


    def start_requests(self):
        for id in self.idSet:
            sinceID = 0
            id_str = id.decode('utf-8')
            yield scrapy.Request(self.userContentUrl.format(id_str, sinceID),
                                 callback=self.parsePageJson, method='GET', headers=self.headers, meta={'id': id_str})
            while sinceID != -1:

                url = "https://social.kkmh.com/v1/graph/users/%s/posts?limit=20&since=%d" % (id_str, sinceID)
                '''try:
                    sinceID, postIdList = getPageJson(url)
                    # print(sinceID)
                    # print(postIdList)
                except:
                    print("get first url error...")
                    sinceID = -1
                    break

                for postId in postIdList:
                    commentSinceID = 0
                    while commentSinceID != -1:
                        commentUrl = "https://social.kkmh.com/v1/graph/posts/%s/comments/v5?filter=1&limit=10&since=%d" % (
                        postId, commentSinceID)
                        try:
                            commentSinceID, userInfoList = getCommentJson(commentUrl)
                            # print(commentSinceID)
                            # print(userInfoList)
                        except:
                            print("get second url error...")
                            commentSinceID = -1
                            break
                        for info in userInfoList:
                            id = info[0]  # int
                            avatar_url = info[1]
                            nickname = info[2]
                            intro = info[3]'''


    def parsePageJson(self, response):
        if response.status != 200:
            return
        id = response.meta['id']
        rltJson = json.loads(response.text)
        sinceID = rltJson['data']['since']
        yield scrapy.Request(self.userContentUrl.format(id, sinceID),
                             callback=self.parsePageJson, method='GET', headers=self.headers, meta={'id': id})
        postIdList = []
        commentSrcList = rltJson['data']['universalModels']
        for commentSrc in commentSrcList:
            try:
                postId = commentSrc['post']['idString']
                yield scrapy.Request(self.userCommentUrl.format(postId, 0),
                                     callback=self.parsePageJson, method='GET', headers=self.headers, meta={'postId': postId})
            except:
                print('get postID error...')
                continue


    def parseCommentJson(self, response):
        if response.status != 200:
            return
        postId = response.meta['postId']
        rltJson = json.loads(response.text)
        sinceID = rltJson['data']['since']
        rltUserInfoList = []
        commentList = rltJson['data']['commentList']
        for commentInfo in commentList:
            try:
                user = commentInfo['postReply']['root']['user']
            except:
                print('get user info error...')
                continue
            item = UserItem()
            item['user_id'] = user['id']  # int
            item['pic_url'] = user['avatar_url']
            item['nickname'] = user['nickname'].strip().replace('\t', '').replace('\n', '').replace('\r', '')
            item['sign_text'] = user['intro'].strip().replace('\t', '').replace('\n', '').replace('\r', '')
            yield item


        return (sinceID, rltUserInfoList)