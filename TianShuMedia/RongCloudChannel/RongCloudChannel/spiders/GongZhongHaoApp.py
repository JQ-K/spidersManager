# -*- coding: utf-8 -*-
import scrapy


class GongzhonghaoappSpider(scrapy.Spider):
    name = 'GongZhongHaoApp'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
