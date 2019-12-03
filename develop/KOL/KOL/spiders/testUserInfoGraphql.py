# -*- coding: utf-8 -*-
import scrapy
import json
import time
from random import choice

from KOL.configure.graphqlQuery import *
from KOL.items import *
from KOL.utils.parsepage import *

class TestuserinfographqlSpider(scrapy.Spider):
    name = 'testUserInfoGraphql'

    principalId = 'yi2658600943'

    url = "https://live.kuaishou.com/graphql"

    headers = {
        #'accept': '*/*',
        #'Accept-Encoding': 'gzip, deflate, br',
        #'Accept-Language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        #'Host': 'live.kuaishou.com',
        #'Origin': 'https://live.kuaishou.com',
    }

    didList = ['web_398544336a2a4c89bafe36006a1c399d',
               'web_d54ea5e1190a41e481809b9cd17f92aa',
               'web_5a63ef3c91c34b8e853c91b68d92208b']

    def getCookie(self):
        tempCookie = {}
        tempCookie['did'] = choice(self.didList)
        return tempCookie

    def start_requests(self):
        userQuery = userInfoQuery
        userQuery['variables']['principalId'] = self.principalId
        yield scrapy.Request(self.url, headers=self.headers, body=json.dumps(userQuery),
                             method='POST', callback=self.parseUserInfo, meta={'bodyJson': userQuery},
                             cookies=self.getCookie()
                             )

    def parseUserInfo(self, response):
        #print(response.text)
        userQuery = response.meta['bodyJson']
        if response.status != 200:
            print('get url error: ' + userQuery)
            return
        rltJson = json.loads(response.text)
        flag = False
        if 'data' in rltJson:
            if 'userInfo' in rltJson['data']:
                if 'principalId' in rltJson['data']['userInfo']:
                    if rltJson['data']['userInfo']['principalId'] is not None:
                        flag = True
        #print(flag)
        if not flag:
            print('parse user info json error: ')
            print(rltJson)
            return

        userInfo = rltJson['data']['userInfo']
        userItem = KuaiShouUserIterm()
        if 'kwaiId' in userInfo:
            userItem['kwaiId'] = userInfo['kwaiId']
        else:
            userItem['kwaiId'] = 'null'

        if 'userId' in userInfo:
            userItem['user_id'] = int(userInfo['userId'])
        else:
            return

        if 'eid' in userInfo:
            userItem['userId'] = userInfo['eid']
        else:
            userItem['userId'] = 'null'

        if 'name' in userInfo:
            userItem['user_name'] = userInfo['name']
        else:
            userItem['user_name'] = 'null'

        if 'sex' in userInfo:
            userItem['user_sex'] = userInfo['sex']
        else:
            userItem['user_sex'] = 'null'

        if 'description' in userInfo:
            userItem['user_text'] = userInfo['description']
        else:
            userItem['user_text'] = 'null'

        if 'profile' in userInfo:
            userItem['head_url'] = userInfo['profile']
        else:
            userItem['head_url'] = 'null'

        userItem['cityCode'] = 'null'

        if 'cityName' in userInfo:
            userItem['cityName'] = userInfo['cityName']
        else:
            userItem['cityName'] = 'null'

        if 'constellation' in userInfo:
            userItem['constellation'] = userInfo['constellation']
        else:
            userItem['constellation'] = 'null'


        if 'countsInfo' in userInfo:
            #mapping = get_mapping(response.text)
            countsInfo = userInfo['countsInfo']
            if 'fan' in countsInfo:
                #userItem['fan'] = decrypt_str(countsInfo['fan'], mapping)
                userItem['fan'] = countsInfo['fan']
            else:
                userItem['fan'] = 'null'

            if 'follow' in countsInfo:
                #userItem['follow'] = decrypt_str(countsInfo['follow'], mapping)
                userItem['follow'] = countsInfo['follow']
            else:
                userItem['follow'] = 'null'

            if 'photo' in countsInfo:
                #userItem['photo'] = decrypt_str(countsInfo['photo'], mapping)
                userItem['photo'] = countsInfo['photo']
            else:
                userItem['photo'] = 'null'

            if 'liked' in countsInfo:
                #userItem['like'] = decrypt_str(countsInfo['liked'], mapping)
                userItem['like'] = countsInfo['liked']
            else:
                userItem['like'] = 'null'

        else:
            userItem['fan'] = 'null'
            userItem['follow'] = 'null'
            userItem['photo'] = 'null'
            userItem['like'] = 'null'

        userItem['article_public'] = 'null'
        userItem['collect'] = 'null'
        userItem['moment'] = 'null'
        userItem['photo_private'] = 'null'
        userItem['photo_public'] = 'null'

        userItem['update_time'] = int(time.time())
        #userItem['user_info_json'] = rltJson

        print(userItem)





