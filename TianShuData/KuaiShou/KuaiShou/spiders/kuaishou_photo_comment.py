# -*- coding: utf-8 -*-
import scrapy


class KuaishouPhotoCommentSpider(scrapy.Spider):
    name = 'kuaishou_photo_comment'
    allowed_domains = ['live.kuaishou.com/graphql']
    start_urls = ['http://live.kuaishou.com/graphql/']

    def parse(self, response):
        pass
