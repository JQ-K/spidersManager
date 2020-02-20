# -*- coding: utf-8 -*-
import scrapy
import time
import json
import random
import datetime

from loguru import logger


class SinapiyaoSpider(scrapy.Spider):
    name = 'SinaPiYao'

    url = 'https://interface.sina.cn/homepage/search.d.json?t=&q=%E8%BE%9F%E8%B0%A3&pf=0&ps=0&page={}&stime={}&etime={}&sort=rel&highlight=1&num=10'

    headers = {
        'Referer': 'http://www.sina.com.cn/mid/search.shtml?range=all&c=news&q=%E8%BE%9F%E8%B0%A3&from=home',
    }


    def __init__(self, stime='2019-12-01', etime='', *args, **kwargs):
        super(SinapiyaoSpider, self).__init__(*args, **kwargs)
        self.stime = stime
        self.etime = etime
        if etime == '':
            self.etime = self.getEtime()
        logger.info('stime:{}, etime:{}'.format(self.stime, self.etime))


    def start_requests(self):
        yield scrapy.Request(self.url.format(1, self.stime, self.etime), method='GET',
                             callback=self.parseList, headers=self.headers,
                             meta={'curPage': 1, 'beginFlag': True, 'totalPage': 1})


    def parseList(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        curPage = response.meta['curPage']
        beginFlag = response.meta['beginFlag']
        totalPage = response.meta['totalPage']

        if 'result' not in rltJson:
            logger.info('result not in response')
            return

        if 'status' not in rltJson['result']:
            logger.info('status not in response')
            return

        if 'code' not in rltJson['result']['status']:
            logger.info('code not in response')
            return

        if rltJson['result']['status']['code'] != 0:
            logger.info('code != 0')
            return

        if beginFlag:
            totalPage = rltJson['result']['page']
            beginFlag = False

        newsList = rltJson['result']['list']
        for newsInfo in newsList:
            print(newsInfo)

        if curPage < totalPage:
            curPage += 1
            time.sleep(random.choice(range(3, 6)))
            yield scrapy.Request(self.url.format(curPage, self.stime, self.etime), method='GET',
                                 callback=self.parseList, headers=self.headers,
                                 meta={'curPage': curPage, 'beginFlag': beginFlag, 'totalPage': totalPage})


    def getEtime(self):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        return str(tomorrow)