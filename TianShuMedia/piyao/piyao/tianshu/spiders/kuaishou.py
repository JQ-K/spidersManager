# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from loguru import logger

class KuaishouSpider(scrapy.Spider):
    name = 'kuaishou'
    # allowed_domains = ['https://live.kuaishou.com/search/?keyword=500730148']
    # start_urls = ['https://live.kuaishou.com/search/?keyword=500730148/']


    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':
            {
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
        'COOKIES_ENABLED' :'False'
    }

    # 设置加载完整的页面:包括两个部分，加载页面 和 下滑加载
    lua_load_all = """
        function main(splash, args)
          -- 自定义请求头
          splash:set_custom_headers({
                ["Cookie"] = "%s"
            })
          args = {
            url = "https://live.kuaishou.com/search/?keyword=%s"
          }
          assert(splash:go(args.url))
          assert(splash:wait(1))
          splash:evaljs("window.onload")
          assert(splash:wait(3))
          assert(splash:go(args.url))
          assert(splash:wait(1))
          return {
            html = splash:html(),
            png = splash:png(),
            har = splash:har(),
            cookies = splash:get_cookies(),
          }
        end

    """

    def start_requests(self):
        sw_headers = {
            "Host": "live.kuaishou.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            }
        start_url = 'https://live.kuaishou.com/'
        yield SplashRequest(start_url, callback=self.parsetest, endpoint='execute', headers=sw_headers, method='GET',
                            args={'lua_source': self.lua_load_all}, cache_args=['lua_source'])

    def parsetest(self, response):
        logger.info('??')
        logger.info(response.url)
        logger.info(response.status)
        logger.info(response.cookies)
        logger.info(response.headers)

        import re

        r = re.findall('did',response.text)
        logger.info(r)

