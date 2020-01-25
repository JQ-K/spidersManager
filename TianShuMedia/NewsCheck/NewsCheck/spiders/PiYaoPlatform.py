# -*- coding: utf-8 -*-
import scrapy
import time
import random

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

    def start_requests(self):
        for curUrl in self.urlList:
            time.sleep(random.choice(range(3, 6)))
            yield scrapy.Request(curUrl, method='GET', callback=self.parseList, meta={'headUrl': curUrl})


    def parseList(self, response):
        pubTime_list = response.xpath('//li[@class="listLi"]/span[@class="listSpan"]/text()').extract()
        href_list = response.xpath('//li[@class="listLi"]/a/@href').extract()
        title_list = response.xpath('//li[@class="listLi"]/a/text()').extract()

        if len(pubTime_list) == len(href_list) and len(href_list) == len(title_list):
            for i in range(len(pubTime_list)):
                newsInfo = NewsInfo()
                newsInfo['channel'] = self.channel
                newsInfo['id'] = href_list[i].split('/')[-1].replace('.shtml', '')
                newsInfo['url'] = href_list[i].replace('//', '')
                newsInfo['title'] = title_list[i]
                newsInfo['publish_time'] = pubTime_list[i]
                yield newsInfo

        headUrl = response.meta['headUrl']

        page_text = response.xpath('//span[@class="fenye"]/a/text()').extract()
        page_href = response.xpath('//span[@class="fenye"]/a/@href').extract()
        if len(page_text) == len(page_href):
            for i in range(len(page_text)):
                if page_text[i] == '下一页':
                    time.sleep(random.choice(range(2, 5)))
                    yield scrapy.Request(headUrl + page_href[i], method='GET',
                                         callback=self.parseList, meta={'headUrl': headUrl})



