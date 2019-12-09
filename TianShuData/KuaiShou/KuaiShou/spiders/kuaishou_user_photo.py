# -*- coding: utf-8 -*-
import scrapy


class KuaishouUserPhotoSpider(scrapy.Spider):
    name = 'kuaishou_user_photo'
    allowed_domains = ['live.kuaishou.com/graphql']
    start_urls = ['http://live.kuaishou.com/graphql/']

    def parse(self, response):
        pass
