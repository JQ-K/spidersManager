# -*- coding: utf-8 -*-
import scrapy
import time
import random

from loguru import logger
from NewsCheck.items import NewsInfo

class HuashuzixunSpider(scrapy.Spider):
    name = 'HuaShuZiXun'
    channel = '华数-资讯板块'

    firstUrl = 'https://all.wasu.cn/index/sort/time/class/program/cid/22'
    head_url = 'https://all.wasu.cn'
    next_page = '/index/sort/time/class/program/cid/22?p=2'

    custom_settings = {'ITEM_PIPELINES': {
        'NewsCheck.pipelines.NewscheckPipeline': 700,
        'NewsCheck.pipelines.KuaishouKafkaPipeline': 701
    }}

    def start_requests(self):
        yield scrapy.Request(self.firstUrl, method='GET', callback=self.parseList)
        time.sleep(random.choice(range(2,5)))
        yield scrapy.Request(self.head_url + self.next_page, method='GET', callback=self.parseList)

    def parseList(self, response):
        href_list = response.xpath('//div[@class="all_hg21"]/a/@href').extract()
        title_list = response.xpath('//div[@class="all_hg21"]/a/@title').extract()
        pubTimeList = response.xpath('//div[@class="all_text"]/p/span/text()').extract()

        # 正常情况下，列表中两个元素，分别是上一页和下一页的连接
        next_page_list = response.xpath("//a[@class='tt']/@href").extract()

        for i in range(len(href_list)):
            try:
                vid = href_list[i].split('/')[-1]
                newsInfo = NewsInfo()
                newsInfo['channel'] = self.channel
                newsInfo['id'] = str(vid)
                newsInfo['url'] = href_list[i]
                newsInfo['title'] = title_list[i]
                newsInfo['publish_time'] = pubTimeList[i].replace('发布时间：', '')
                yield newsInfo
            except:
                logger.info('get vid error: ' + href_list[i])
                continue

        if len(next_page_list) >= 2:
            time.sleep(random.choice(range(2, 5)))
            yield scrapy.Request(self.head_url + next_page_list[1], method='GET', callback=self.parseList)

