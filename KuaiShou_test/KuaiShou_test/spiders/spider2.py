# -*- coding: utf-8 -*-
import scrapy


class Spider2Spider(scrapy.Spider):
    name = 'spider2'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
