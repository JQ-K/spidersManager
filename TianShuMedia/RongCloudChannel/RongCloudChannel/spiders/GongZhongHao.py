# -*- coding: utf-8 -*-
import scrapy


class GongzhonghaoSpider(scrapy.Spider):
    name = 'GongZhongHao'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
