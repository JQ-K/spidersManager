# -*- coding: utf-8 -*-
import scrapy
import time
import random
import re
import redis

from loguru import logger
from scrapy.utils.project import get_project_settings
from NewsCheck.items import NewsInfo


class PiyaoplatformSpider(scrapy.Spider):
    name = 'PiYaoPlatform'
    channel = '浙江媒体网站联合辟谣平台'

    urlList = ['https://py.zjol.com.cn/rdgz/',
               'https://py.zjol.com.cn/gzdt/',
               'https://py.zjol.com.cn/pyxw/',
               'https://py.zjol.com.cn/zjsj/']

    custom_settings = {'ITEM_PIPELINES': {
        'NewsCheck.pipelines.NewscheckPipeline': 700,
        'NewsCheck.pipelines.KuaishouKafkaPipeline': 701
    }}


    def __init__(self):
        self.settings = get_project_settings()
        self.redis_host = self.settings.get('REDIS_HOST')
        self.redis_port = self.settings.get('REDIS_PORT')
        self.red = redis.Redis(host=self.redis_host, port=self.redis_port)

    def start_requests(self):
        for curUrl in self.urlList:
            time.sleep(random.choice(range(1, 3)))
            yield scrapy.Request(curUrl, method='GET', callback=self.parseList, meta={'headUrl': curUrl})


    def parseList(self, response):
        pubTime_list = response.xpath('//li[@class="listLi"]/span[@class="listSpan"]/text()').extract()
        href_list = response.xpath('//li[@class="listLi"]/a/@href').extract()
        title_list = response.xpath('//li[@class="listLi"]/a/text()').extract()

        if len(pubTime_list) == len(href_list) and len(href_list) == len(title_list):
            for i in range(len(pubTime_list)):
                id = href_list[i].split('/')[-1].replace('.shtml', '')
                if self.red.sismember(self.name, id):
                    logger.info('id存在: ' + id)
                    continue

                newsInfo = NewsInfo()
                newsInfo['channel'] = self.channel
                newsInfo['id'] = id
                newsInfo['url'] = 'https:' + href_list[i]
                newsInfo['title'] = title_list[i]
                #newsInfo['publish_time'] = pubTime_list[i]
                time.sleep(random.choice(range(1, 3)))
                yield scrapy.Request(newsInfo['url'], method='GET',
                                     callback=self.parseNews, meta={'item': newsInfo})

        headUrl = response.meta['headUrl']

        page_text = response.xpath('//span[@class="fenye"]/a/text()').extract()
        page_href = response.xpath('//span[@class="fenye"]/a/@href').extract()
        if len(page_text) == len(page_href):
            for i in range(len(page_text)):
                if page_text[i] == '下一页':
                    time.sleep(random.choice(range(1, 3)))
                    yield scrapy.Request(headUrl + page_href[i], method='GET',
                                         callback=self.parseList, meta={'headUrl': headUrl})


    def parseNews(self, response):
        newsInfo = response.meta['item']

        newsInfo['content'] = response.text

        p_list = response.xpath('//div[@class="contTxt"]//text()').extract()
        content = ''
        for p in p_list:
            content += re.sub(r'\r\n|\n|\t', "", p)
        newsInfo['text'] = content.strip()

        pubTimeList = response.xpath('//span[@id="pubtime_baidu"]/text()').extract()
        if len(pubTimeList) > 0:
            publish_time = re.sub(r'\r\n|\n|\t', "", pubTimeList[0]).strip()
            newsInfo['publish_time'] = self.strToTimeStamp(publish_time)

        yield newsInfo


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


    def close(self):
        #self.red.close()
        pass
