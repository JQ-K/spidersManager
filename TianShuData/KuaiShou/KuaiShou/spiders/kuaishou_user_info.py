# -*- coding: utf-8 -*-
import scrapy


class KuaishouUserInfoSpider(scrapy.Spider):
    name = 'kuaishou_user_info'
    allowed_domains = ['live.kuaishou.com/graphql']
    start_urls = ['http://live.kuaishou.com/graphql/']

    def parse(self, response):
        pass



