# -*- coding: utf-8 -*-
import scrapy
import json

class GraphqlSpider(scrapy.Spider):
    name = 'graphql'

    url = "https://live.kuaishou.com/graphql"

    headers = {
        'Content-Type': 'application/json'
    }

    bodyJson = {
        "operationName": "videoFeedsQuery",
        "variables": {
            "count": 20,
            "pcursor": "0"
        },
        "query": "fragment VideoMainInfo on VideoFeed {\n  photoId\n  caption\n  thumbnailUrl\n  poster\n  viewCount\n  likeCount\n  commentCount\n  timestamp\n  workType\n  type\n  useVideoPlayer\n  imgUrls\n  imgSizes\n  magicFace\n  musicName\n  location\n  liked\n  onlyFollowerCanComment\n  width\n  height\n  expTag\n  __typename\n}\n\nquery videoFeedsQuery($pcursor: String, $count: Int) {\n  videoFeeds(pcursor: $pcursor, count: $count) {\n    list {\n      user {\n        id\n        eid\n        profile\n        name\n        __typename\n      }\n      ...VideoMainInfo\n      __typename\n    }\n    pcursor\n    __typename\n  }\n}\n"
    }

    def start_requests(self):
        yield scrapy.Request(self.url, headers=self.headers, body=json.dumps(self.bodyJson),
                             method='POST', callback=self.parseGraphql)


    def parseGraphql(self, response):
        #print(response.text)
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        userList = rltJson['data']['videoFeeds']['list']
        for user in userList:
            id = user['user']['id']
            print(id)