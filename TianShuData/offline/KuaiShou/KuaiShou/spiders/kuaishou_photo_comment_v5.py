# -*- coding: utf-8 -*-
import scrapy


class KuaishouPhotoCommentV5Spider(scrapy.Spider):
    name = 'kuaishou_photo_comment_v5'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
