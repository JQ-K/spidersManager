# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import time
import random
from ArticleSpider.settings import UA_POOL
from redis import Redis
from scrapy.utils.project import get_project_settings
from ArticleSpider.utils.mysql import MySQLClient

class KuaishoucomplementsSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class KuaishoucomplementsDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        request.headers['User-Agent'] = random.choice(UA_POOL)
        settings = get_project_settings()
        self.use_proxy = settings.get('USE_PROXY')
        # 设置代理IP
        # if self.use_proxy:
        #     proxy_list = self.conn.srandmember(self.redis_proxyip_name, 1)
        #     while proxy_list == []:
        #         spider.logger.warn('Proxy Pool is null, Plase add proxy !')
        #         time.sleep(60)
        #         proxy_list = self.conn.srandmember(self.redis_proxyip_name, 1)
        #     proxy = proxy_list[0].decode()
        #     spider.logger.info('proxy:{}'.format(proxy))
        #     request.meta['proxy'] = proxy
        #
        # if spider.name in ['kuaishou_register_did']:
        #     return None
        #
        # cookies_list = self.conn.srandmember(self.redis_did_name, 1)
        # while cookies_list == []:
        #     spider.logger.warn('Did Pool is null, Plase add did !')
        #     time.sleep(60)
        #     cookies_list = self.conn.srandmember(self.redis_did_name, 1)
        # cookies=cookies_list[0].decode()
        # cookies_dict = eval(cookies)
        # cookies_str = ''
        # for key, value in cookies_dict.items():
        #     cookies_str += '{}={}; '.format(key,value)
        # # 对于用户隐私数据需要带上这个,这里主要是 kuaishou_user_info和kuaishou_search_principalid两个spides用到
        # # if spider.name in ['kuaishou_search_principalid','kuaishou_user_info']:
        # #     for key, value in self.kuaishou_live_web_st.items():
        # #         cookies_str += '{}={}; '.format(key,value)
        # spider.logger.info('Cookie:{}'.format(cookies_str[:-2] ))
        # request.headers.setdefault('Cookie', cookies_str[:-2])


        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        # 处理请求超时的proxy:删除代理池中无效proxy，更新请求中的proxy
        spider.logger.warn('Request error : %s ' % exception)
        if 'connection' in str(exception).lower():
            invaild_proxy = request.meta['proxy']
            spider.logger.info('Proxy : %s is invaild ! Proxy sreming...' % invaild_proxy)
            self.conn.srem(self.redis_proxyip_name, invaild_proxy)
            proxy_list = self.conn.srandmember(self.redis_proxyip_name, 1)
            while proxy_list == []:
                time.sleep(60)
                spider.logger.warn('Proxy Pool is null, Plase add proxy !')
            proxy = proxy_list[0].decode()
            request.meta['proxy'] = proxy
            spider.logger.info('Update proxy : %s ' % proxy)

        pass

    def spider_opened(self, spider):
        settings = get_project_settings()
        # self.kuaishou_live_web_st = settings.get('KUAISHOU_LIVE_WEB_ST')
        # self.uapool = settings.get('UAPOOL')
        self.uapool = UA_POOL
        self.redis_host = settings.get('REDIS_HOST')
        self.redis_port = settings.get('REDIS_PORT')
        self.redis_did_name = settings.get('REDIS_DID_NAME')
        self.redis_proxyip_name = settings.get('REDIS_PROXYIP_NAME')
        self.conn = Redis(host=self.redis_host, port=self.redis_port)
        spider.logger.info('Spider opened: %s' % spider.name)
