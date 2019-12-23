# -*- coding: utf-8 -*-
import scrapy


class PrincipalIdSpider(scrapy.Spider):
    name = 'principal_id'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
