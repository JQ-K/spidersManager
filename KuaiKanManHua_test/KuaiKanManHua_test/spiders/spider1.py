# -*- coding: utf-8 -*-
import scrapy


class Spider1Spider(scrapy.Spider):
    name = 'spider1'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
