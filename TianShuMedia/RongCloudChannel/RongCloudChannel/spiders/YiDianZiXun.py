# -*- coding: utf-8 -*-
import scrapy


class YidianzixunSpider(scrapy.Spider):
    name = 'YiDianZiXun'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
