# -*- coding: utf-8 -*-
import scrapy


class KuaishouShopProductCommentSpider(scrapy.Spider):
    name = 'kuaishou_shop_product_comment'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
