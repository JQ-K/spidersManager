# -*- coding: utf-8 -*-
import scrapy
import json
import time

from KOL.configure.graphqlQuery import *
from KOL.utils.myredis import RedisClient
from KOL.items import TestCommentUserItem

class TestgraphqlSpider(scrapy.Spider):
    name = 'testGraphql'

    redis_id_set_name = "KuaiShouPrincipalId"
    redisClient = RedisClient('10.8.26.105', 6379, 1)
    #redisClient = RedisClient('10.8.26.26', 6379, 1)

    #principalId = '3xy424mqbve5h82'
    url = "https://live.kuaishou.com/graphql"

    headers = {
        'accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'Host': 'live.kuaishou.com',
        'Origin': 'https://live.kuaishou.com',
    }

    '''headers = {
        'content-type': 'application/json',
    }'''

    cookies = {
        'did': 'web_398544336a2a4c89bafe36006a1c399d'
    }

    def __init__(self):
        self.idSet = self.redisClient.smembers(self.redis_id_set_name)


    def start_requests(self):
        for id in self.idSet:
            print("cur id:")
            print(id)
            feedQuery = publicFeedsQuery
            feedQuery['variables']['principalId'] = str(id, encoding='utf-8')
            feedQuery['variables']['pcursor'] = '0'
            time.sleep(3)
            yield scrapy.Request(self.url, headers=self.headers, body=json.dumps(feedQuery),
                                 method='POST', callback=self.parsePublicFeeds, meta={'bodyJson': feedQuery},
                                 cookies=self.cookies
                                 )


    def parsePublicFeeds(self, response):
        feedQuery = response.meta['bodyJson']
        if response.status != 200:
            print('get url error: ' + feedQuery)
            return
        rltJson = json.loads(response.text)
        flag = False
        if 'data' in rltJson:
            if 'publicFeeds' in rltJson['data']:
                flag = True
        if not flag:
            print('parse public feeds json error: ')
            print(rltJson)
            return
        pcursor = rltJson['data']['publicFeeds']['pcursor']
        feedList = rltJson['data']['publicFeeds']['list']
        for feed in feedList:
            photoId = feed['photoId']
            print('photoId:' + photoId)
            commentQuery = commentListQuery
            commentQuery['variables']['pcursor'] = '0'
            commentQuery['variables']['photoId'] = photoId
            time.sleep(2)
            yield scrapy.Request(self.url, headers=self.headers, body=json.dumps(commentQuery),
                                 method='POST', callback=self.parseCommentByPhotoId, meta={'bodyJson': commentQuery},
                                 cookies=self.cookies
                                 )
        if pcursor != 'no_more':
            feedQuery['variables']['pcursor'] = pcursor
            time.sleep(2)
            yield scrapy.Request(self.url, headers=self.headers, body=json.dumps(feedQuery),
                                 method='POST', callback=self.parsePublicFeeds, meta={'bodyJson': feedQuery},
                                 cookies=self.cookies
                                 )


    def parseCommentByPhotoId(self, response):
        commentQuery = response.meta['bodyJson']
        if response.status != 200:
            print('get url error: ' + commentQuery)
            return
        rltJson = json.loads(response.text)
        flag = False
        if 'data' in rltJson:
            if 'shortVideoCommentList' in rltJson['data']:
                flag = True
        if not flag:
            print('parse comment list json error: ')
            print(rltJson)
            return
        pcursor = rltJson['data']['shortVideoCommentList']['pcursor']
        commentList = rltJson['data']['shortVideoCommentList']['commentList']
        for comment in commentList:
            commentUser = TestCommentUserItem()
            if 'authorId' in comment:
                commentUser['authorId'] = comment['authorId']
            else:
                continue
            if 'authorName' in comment:
                commentUser['authorName'] = comment['authorName']
            else:
                commentUser['authorName'] = 'null'
            if 'headurl' in comment:
                commentUser['headurl'] = comment['headurl']
            else:
                commentUser['headurl'] = 'null'
            if 'authorEid' in comment:
                commentUser['authorEid'] = comment['authorEid']
            else:
                continue
            if self.redisClient.sismember(self.redis_id_set_name, commentUser['authorEid']):
                print('item exist')
                continue
            else:
                self.redisClient.sadd(self.redis_id_set_name, commentUser['authorEid'])
                print('get new item: ' + commentUser['authorEid'])
                yield commentUser
        if pcursor != 'no_more':
            commentQuery['variables']['pcursor'] = pcursor
            time.sleep(2)
            yield scrapy.Request(self.url, headers=self.headers, body=json.dumps(commentQuery),
                                 method='POST', callback=self.parseCommentByPhotoId, meta={'bodyJson': commentQuery},
                                 cookies=self.cookies
                                 )


    def close(self):
        self.redisClient.close()



