# -*- coding: utf-8 -*-
import scrapy
import json
import time

from KOL.utils.parsepage import *
from KOL.items import KuaiShouUserIterm
from KOL.utils.myredis import RedisClient


class GraphqlSpider(scrapy.Spider):
    name = 'graphql'

    redis_id_set_name = "KuaiShouGameUserId"
    #redisClient = RedisClient('10.8.26.105', 6379, 1)
    redisClient = RedisClient('10.8.26.26', 6379, 1)

    filePath = "/Users/macbookpro/PycharmProjects/spidersManager/develop/KOL/test/gameUser.txt"

    url = "https://live.kuaishou.com/graphql"

    headers = {
        'Content-Type': 'application/json'
    }

    bodyJson = {
        "operationName": "videoFeedsQuery",
        "variables": {
            "count": 200,
            "pcursor": "0"
        },
        "query": "fragment VideoMainInfo on VideoFeed {\n  photoId\n  caption\n  thumbnailUrl\n  poster\n  viewCount\n  likeCount\n  commentCount\n  timestamp\n  workType\n  type\n  useVideoPlayer\n  imgUrls\n  imgSizes\n  magicFace\n  musicName\n  location\n  liked\n  onlyFollowerCanComment\n  width\n  height\n  expTag\n  __typename\n}\n\nquery videoFeedsQuery($pcursor: String, $count: Int) {\n  videoFeeds(pcursor: $pcursor, count: $count) {\n    list {\n      user {\n        id\n        eid\n        profile\n        name\n        kwaiId\n    __typename\n      }\n      ...VideoMainInfo\n      __typename\n    }\n    pcursor\n    __typename\n  }\n}\n"
    }


    def __init__(self, totalPage=1, *args, **kwargs):
        super(GraphqlSpider, self).__init__(*args, **kwargs)
        self.totalPage = int(totalPage)


    def start_requests(self):
        curPage = 1
        while curPage <= self.totalPage:
            curPage += 1
            time.sleep(3)
            yield scrapy.Request(self.url, headers=self.headers, body=json.dumps(self.bodyJson),
                                 method='POST', callback=self.parseGraphql)


    def parseGraphql(self, response):

        f = open(self.filePath, "a+", encoding='utf-8')
        #print(response.text)
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        userList = rltJson['data']['videoFeeds']['list']
        for user in userList:
            id = user['user']['id']
            #print(id)
            if self.redisClient.sismember(self.redis_id_set_name, id):
                print('id exists: ' + str(id))
                continue
            userItem = KuaiShouUserIterm()
            userItem['user_id'] = -1
            userItem['userId'] = id
            userItem['kwaiId'] = user['user']['kwaiId']
            userItem['head_url'] = user['user']['profile']
            userItem['user_name'] = user['user']['name']
            '''url = 'https://live.kuaishou.com/profile/{}'.format(id)
            time.sleep(1)
            try:
                self.getUserInfoByWeb(url, userItem)
            except:
                print('get user info error:' + str(id))
                continue'''
            self.redisClient.sadd(self.redis_id_set_name, id)
            print('get one item:' + str(id))
            rltStr = userItem['userId'] + '\t' + userItem['kwaiId'] + '\t' + userItem['head_url'] + '\t' + userItem['user_name']
            f.write(rltStr + '\n')
            #yield userItem
            #print(userItem)
        f.close()


    '''def getUserInfoByWeb(self, url, userItem):
        r = get_kuai_page(url)
        print(r.text)
        mapping = get_mapping(r.text)
        print(mapping)
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
        userItem['update_time'] = int(time.time())'''


    def close(self):
        self.redisClient.close()
