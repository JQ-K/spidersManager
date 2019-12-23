# -*- coding: utf-8 -*-
import scrapy


class UserInfoSpider(scrapy.Spider):
    name = 'user_info'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
