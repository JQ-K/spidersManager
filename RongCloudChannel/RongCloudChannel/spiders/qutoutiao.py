# -*- coding: utf-8 -*-
import scrapy


class QutoutiaoSpider(scrapy.Spider):
    name = 'qutoutiao'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
