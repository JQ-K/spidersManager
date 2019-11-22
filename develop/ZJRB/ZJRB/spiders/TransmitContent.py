# -*- coding: utf-8 -*-
import scrapy
from ZJRB.utils.mysqlUtil import *

class TransmitcontentSpider(scrapy.Spider):
    name = 'TransmitContent'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'SUB=_2AkMqi8mRf8NxqwJRmfwWxWnhb4xxzwvEieKc1zhKJRMxHRl-yT83qkpftRB6AQvnfUXimls9hl2GSsUajCG-eXZ0XHs4; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWzsxWWsMuH7dIjfPwSPm-o; _s_tentry=passport.weibo.com; Apache=5971602491889.376.1574389416544; SINAGLOBAL=5971602491889.376.1574389416544; ULV=1574389416593:1:1:1:5971602491889.376.1574389416544:; Ugrow-G0=5c7144e56a57a456abed1d1511ad79e8; YF-V5-G0=260e732907e3bd813efaef67866e5183; login_sid_t=3b90273524ad6125679f07666451ea2f; cross_origin_proto=SSL; wb_view_log=1280*7201.5; YF-Page-G0=96c3bfa80dc53c34a567607076bb434e|1574412911|1574412911',
        'Host': 'weibo.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    }

    def __init__(self):
        mysqlClient = MysqlClient('10.8.26.23', 'hive', 'Hive_123', 'zjrb')
        self.urlList = mysqlClient.getUrlListByHost('http://weibo.com')
        mysqlClient.close()

    def start_requests(self):
        for urlInfo in self.urlList:
            id, source_title, title, url = urlInfo
            print(id)
            print(source_title)
            print(title)
            print(url)
            url = 'https://weibo.com/1036713140/Igj2um9gI?type=comment'
            #url = 'https://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=https%3A%2F%2Fweibo.com%2F1036713140%2FIgj2um9gI&domain=.weibo.com&ua=php-sso_sdk_client-0.6.28&_rand=1574414652.2118'
            yield scrapy.Request(url, method='GET', callback=self.parseFirstPage,
                                 headers=self.headers, dont_filter=True)
            break

    def parseFirstPage(self, response):
        print(response.status)
        print(response.text)
