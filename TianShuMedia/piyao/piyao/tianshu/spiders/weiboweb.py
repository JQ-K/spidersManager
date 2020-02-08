# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from loguru import logger


class CrawTmpSpider(scrapy.Spider):
    name = 'weiboweb'
    # allowed_domains = ['weibo.com']
    start_urls = ['https://weibo.com/cecn?refer_flag=1005050010_&is_hot=1']

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
    }

    # 设置加载完整的页面:包括两个部分，加载页面 和 下滑加载
    lua_load_all = """
        function main(splash)
            splash:go(splash.args.url)
            splash:wait(1)
            splash:runjs('document.getElementsById("Pl_Official_MyProfileFeed__27").scrollIntoView()')
            splash:wait(3) 
            splash:set_viewport_size(1028, 10000)
            local scroll_to = splash:jsfunc("window.scrollTo")
            scroll_to(0, 10)
            splash:wait(10)
            return splash:html()
        end
    """


    def lua_next_page(self, pagenum):
        """
        跳转下一页
        :param pagenum:
        :return:
        """
        lua_next_page = """
                function main(splash)
                    splash:go(splash.args.url)
                    splash:wait(1)
                    splash:runjs("SEARCH.page(%s, true)")
                    splash:wait(1)
                    return splash:url()
                end
                """ % (str(pagenum))
        return lua_next_page

    def start_requests(self):
        start_url = 'https://weibo.com/zjdaily?is_all=1'
        yield SplashRequest(start_url, callback=self.parsetest, endpoint='execute',
                            args={'lua_source': self.lua_load_all}, cache_args=['lua_source'])

    def parsetest(self, response):
        i = 0
        for para in response.xpath('//*[@id="Pl_Official_MyProfileFeed__27"]/div/div[*]/div[1]/div[4]/div[4]'):
            i+=1
            logger.info(para.extract())
            logger.info(i)
