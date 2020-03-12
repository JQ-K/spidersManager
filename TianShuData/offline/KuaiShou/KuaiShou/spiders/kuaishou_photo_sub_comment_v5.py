# -*- coding: utf-8 -*-
import scrapy


class KuaishouPhotoSubCommentV5Spider(scrapy.Spider):
    name = 'kuaishou_photo_sub_comment_v5'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
