# -*- coding: utf-8 -*-
import scrapy


class BaijiahaoSpider(scrapy.Spider):
    name = 'BaiJiaHao'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
