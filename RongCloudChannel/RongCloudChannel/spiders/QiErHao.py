# -*- coding: utf-8 -*-
import scrapy


class QierhaoSpider(scrapy.Spider):
    name = 'QiErHao'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
