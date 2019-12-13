# -*- coding: utf-8 -*-
import scrapy

from scrapy.utils.project import get_project_settings

class KuaishouTestSpider(scrapy.Spider):
    name = 'kuaishou_test'
    allowed_domains = ['dataapi.kuxuan-inc.com']
    start_urls = ['http://live.kuaishou.com']
    Settings = get_project_settings().get('SPIDER_COOKIE_CNT')
    print(Settings)

    # def start_requests(self):
    #     myredis.RedisClient()
    #     yield

    def parse(self, response):
        pass
