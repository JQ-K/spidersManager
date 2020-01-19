# -*- coding: utf-8 -*-
import scrapy
import re, time
import json, random

from scrapy_splash import SplashRequest
from scrapy.utils.project import get_project_settings
from loguru import logger
from redis import Redis
from urllib.parse import urlencode

from KuaiShou.utils import ProduceRandomStr
from KuaiShou.items import KuaishouCookieInfoItem


class KuaishouRegisterDidSpider(scrapy.Spider):
    name = 'kuaishou_register_did'
    custom_settings = {'ITEM_PIPELINES':
                           {'KuaiShou.pipelines.KuaishouRedisPipeline': 700},
                       'CONCURRENT_REQUESTS': 1,
                       'DOWNLOAD_DELAY' : random.randint(5, 10),
                       'CONCURRENT_REQUESTS_PER_IP' : 1,
                       'DOWNLOADER_MIDDLEWARES':
                           {
                               # 'KuaiShou.middlewares.KuaishouDownloaderMiddleware': 727,
                               'scrapy_splash.SplashCookiesMiddleware': 723,
                               'scrapy_splash.SplashMiddleware': 725,
                               'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
                           },
                       'SPIDER_MIDDLEWARES':
                           {
                               'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
                           },
                       'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
                       'SPLASH_URL': 'http://localhost:8050/',
                       'COOKIES_ENABLED': 'False'
                       }

    def start_requests(self):
        # 设置加载完整的页面
        self.lua_load_all = """
            function main(splash, args)
              -- 自定义请求头
              splash:set_custom_headers({
                    ["Cookie"] = "%s"
                })
              args = {
                url = "http://live.kuaishou.com/search/?keyword=%s"
              }
              assert(splash:go(args.url))
              assert(splash:wait(1))
              splash:evaljs("window.onload")
              assert(splash:wait(3))
              assert(splash:go(args.url))
              assert(splash:wait(1))
              splash:evaljs("window.onload")
              assert(splash:wait(3))
              return {
                html = splash:html(),
                png = splash:png(),
                har = splash:har(),
                cookies = splash:get_cookies(),
              }
            end

        """
        settings = get_project_settings()
        redis_host = settings.get('REDIS_HOST')
        redis_port = settings.get('REDIS_PORT')
        self.redis_did_name = settings.get('REDIS_DID_NAME')
        self.redis_did_expire_time = settings.get('REDIS_DID_EXPIRE_TIME')
        self.redis_proxyip_name = settings.get('REDIS_PROXYIP_NAME')
        self.conn = Redis(host=redis_host, port=redis_port)
        start_url = 'http://live.kuaishou.com/search/?keyword=%s' % random.randint(100, 10000)
        spider_did_supplements_quantity_per_time = self.settings.get('SPIDER_DID_SUPPLEMENTS_QUANTITY_PER_TIME')
        spider_did_pool_warning_line = self.settings.get('SPIDER_DID_POOL_WARNING_LINE')
        while True:
            # zremrangebyscore(name, min, max)
            max_score = int(time.time()) - int(self.redis_did_expire_time)
            self.conn.zremrangebyscore(self.redis_did_name, 0, max_score)
            did_pool_quantity = self.conn.zcard(self.redis_did_name)
            logger.info('Did pool quantity: {}'.format(did_pool_quantity))
            if did_pool_quantity > spider_did_pool_warning_line:
                time.sleep(10)
                continue
            counter = 0
            while counter < spider_did_supplements_quantity_per_time:
                counter += 1
                time.sleep(random.randint(10, 15))
                yield scrapy.Request(start_url, method='GET', callback=self.produce_did, dont_filter=True)

    def produce_did(self, response):
        # 设置代理IP
        # proxy = response.meta['proxy']
        # ua =  response.meta['ua']
        # logger.info(proxy)
        search_url = response.url
        keyword = re.findall('live\.kuaishou\.com/search/\?keyword=([0-9a-z]+)', search_url)[0]
        set_cookie_list = response.headers.getlist('Set-Cookie')
        if set_cookie_list == []:
            return
        cookie_str = ''
        for cookie in set_cookie_list:
            str = cookie.decode().split(' ')[0]
            if 'client_key=' in str:
                n_set = [chr(i) for i in range(48, 58)]
                s_char_set = [chr(i) for i in range(97, 122)]
                n_str = "".join(random.sample(n_set, 4))
                ns_str = "".join(random.sample(n_set + s_char_set, 4))
                cookie_str += 'client_key='+n_str+ns_str
                continue
            cookie_str += str
        lua_load_all = self.lua_load_all % (cookie_str, keyword)
        headers = {
            "Host": "live.kuaishou.com",
            "Connection": "keep-alive",
            # "User-Agent": ua,
        }
        yield SplashRequest(search_url, callback=self.register_did, endpoint='execute', headers=headers, method='GET',
                            args={'lua_source': lua_load_all}, cache_args=['lua_source'],
                            meta={'Cookie': cookie_str})

    def register_did(self, response):
        kuaishou_cookie_info_item = KuaishouCookieInfoItem()
        Cookie = response.meta['Cookie']
        kuaishou_cookie_info_item['Cookie'] = Cookie
        logger.info(kuaishou_cookie_info_item)
        return kuaishou_cookie_info_item
