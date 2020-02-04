# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random
import re
import datetime

from loguru import logger
from NewsCheck.items import NewsInfo

class KuaishoufeedSpider(scrapy.Spider):
    name = 'KuaiShouFeed'

    url = 'https://live.kuaishou.com/m_graphql'

    videoUrl = 'https://live.kuaishou.com/u/{}/{}'

    principalId = "3xet6s5b4u48hia"

    query = {
        "operationName": "publicFeedsQuery",
        "variables": {
            "principalId": principalId,
            "pcursor": "0",
            "count": 24
        },
        "query": "query publicFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  publicFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    live {\n      user {\n        id\n        avatar\n        name\n        __typename\n      }\n      watchingCount\n      poster\n      coverUrl\n      caption\n      id\n      playUrls {\n        quality\n        url\n        __typename\n      }\n      quality\n      gameInfo {\n        category\n        name\n        pubgSurvival\n        type\n        kingHero\n        __typename\n      }\n      hasRedPack\n      liveGuess\n      expTag\n      __typename\n    }\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"
    }

    headers = {
        'Content-Type':'application/json'
    }

    cookies = {
        'did': 'web_54091ed760f84f168198018254a24fec',
    }

    custom_settings = {'ITEM_PIPELINES': {
        'NewsCheck.pipelines.KuaiShouPipeline': 700,
    }}


    def __init__(self, minTime='2020-01-24', *args, **kwargs):
        super(KuaishoufeedSpider, self).__init__(*args, **kwargs)
        self.minTime = minTime + " 00:00:00"
        self.minTimeStamp = self.strToTimeStamp(self.minTime) * 1000

        #self.today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        self.maxTimeStamp = self.strToTimeStamp(self.getYesterday() + " 00:00:00") * 1000


    def start_requests(self):
        yield scrapy.Request(self.url, method='POST', cookies=self.cookies,
                             headers=self.headers, body=json.dumps(self.query),
                             callback=self.parseFeedList, meta={'pid': self.principalId})


    def parseFeedList(self, response):
        pid = response.meta['pid']
        flag = True
        rltJson = json.loads(response.text)
        videoList = rltJson['data']['publicFeeds']['list']
        for videoInfo in videoList:
            curTimeStamp = videoInfo['timestamp']
            if curTimeStamp < self.minTimeStamp or curTimeStamp >= self.maxTimeStamp:
                continue
                #logger.info('已经拿到最小要求发布时间，采集结束')
                #flag = False
                #break
            newsInfo = NewsInfo()
            newsInfo['id'] = videoInfo['id']
            newsInfo['url'] = self.videoUrl.format(pid, newsInfo['id'])
            newsInfo['title'] = re.sub(r'\r\n|\n|\t', "", videoInfo['caption'])
            newsInfo['publish_time'] = self.timeStampToStr(curTimeStamp)
            newsInfo['read_count'] = videoInfo['counts']['displayView']
            newsInfo['like_count'] = videoInfo['counts']['displayLike']
            newsInfo['comment_count'] = videoInfo['counts']['displayComment']
            yield newsInfo

        pcursor = rltJson['data']['publicFeeds']['pcursor']
        if pcursor == 'no_more':
            return
        if flag:
            curQuery = self.query
            curQuery['variables']['pcursor'] = pcursor
            time.sleep(random.choice(range(10,20)))
            yield scrapy.Request(self.url, method='POST', cookies=self.cookies,
                                 headers=self.headers, body=json.dumps(curQuery),
                                 callback=self.parseFeedList, meta={'pid': self.principalId})



    def strToTimeStamp(self, timeStr):
        try:
            # 先转换为时间数组
            timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")
            # 转换为时间戳
            timeStamp = int(time.mktime(timeArray))
            return timeStamp
        except:
            logger.info('str to timestamp error:' + timeStr)
            return None


    def timeStampToStr(self, timeStamp):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(str(timeStamp)[0:10])))


    def getYesterday(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=0)
        yesterday = today - oneday
        return yesterday.strftime('%Y-%m-%d')

