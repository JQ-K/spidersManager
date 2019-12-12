# -*- coding: utf-8 -*-
import scrapy
import time, random

from KuaiShou.items import KuaishouCookieInfoItem
from KuaiShou.settings import SPIDER_COOKIE_CNT


class KuaishouCookieInfoSpider(scrapy.Spider):
    name = 'kuaishou_cookie_info'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouRedisPipeline': 700
    }}
    allowed_domains = ['live.kuaishou.com']

    # start_urls = ['http://live.kuaishou.com/']

    def start_requests(self):
        i = 0
        while i < SPIDER_COOKIE_CNT:
            i += 1
            time.sleep(random.randint(1, 3))
            start_url = 'https://live.kuaishou.com'
            headers = {
                "Host": "live.kuaishou.com",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=0",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
            }
            yield scrapy.Request(start_url, headers=headers, callback=self.parse_cookie, dont_filter=True)

    def parse_cookie(self, response):
        kuaishou_cookie_info_item = KuaishouCookieInfoItem()
        kuaishou_cookie_info_item['name'] = self.name
        # kuaishou_cookie_info_item['operation_type'] = 'sadd'
        for cookie in response.headers.getlist('Set-Cookie'):
            cookie_str = cookie.decode().split(';')[0]
            key, value = cookie_str.split('=')
            kuaishou_cookie_info_item[key.replace('.', '_')] = value
        yield kuaishou_cookie_info_item
