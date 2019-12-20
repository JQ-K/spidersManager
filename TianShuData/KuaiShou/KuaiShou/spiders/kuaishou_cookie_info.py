# -*- coding: utf-8 -*-
import scrapy
import time, random, json

from scrapy.utils.project import get_project_settings
from loguru import logger

from KuaiShou.items import KuaishouCookieInfoItem
from KuaiShou.utils.did import RegisterCookie



class KuaishouCookieInfoSpider(scrapy.Spider):
    name = 'kuaishou_cookie_info'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouRedisPipeline': 700
    }}
    settings = get_project_settings()
    # allowed_domains = ['live.kuaishou.com']
    # start_urls = ['http://live.kuaishou.com/']

    def start_requests(self):
        i = 0
        spider_cookie_cnt = self.settings.get('SPIDER_COOKIE_CNT')
        while i < spider_cookie_cnt:
            i += 1
            time.sleep(random.randint(1, 3))
            kuaishou_url = 'http://live.kuaishou.com/graphql'
            search_hot_query = self.settings.get('SEARCH_HOT_QUERY')
            headers = {'content-type': 'application/json'}
            logger.info(search_hot_query)
            yield scrapy.Request(kuaishou_url, headers=headers, body=json.dumps(search_hot_query),
                                 method='POST',
                                 meta={'bodyJson': search_hot_query},
                                 callback=self.parse_produce_cookie, dont_filter=True
                                 )
    def parse_produce_cookie(self, response):
        kuaishou_cookie_info_item = KuaishouCookieInfoItem()
        cookies = ''
        for cookie in response.headers.getlist('Set-Cookie'):
            cookie_str = cookie.decode().split(';')[0]
            key, value = cookie_str.split('=')
            cookies += '{}={}; '.format(key,value)
            kuaishou_cookie_info_item[key.replace('.','_')] = value
        if RegisterCookie(cookies):
            logger.info(kuaishou_cookie_info_item)
            yield kuaishou_cookie_info_item
            time.sleep(random.randint(30, 60))
