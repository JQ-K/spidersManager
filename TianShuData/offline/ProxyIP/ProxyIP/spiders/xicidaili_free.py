# -*- coding: utf-8 -*-
import scrapy
import json,re
from lxml import etree
from loguru import logger
from scrapy.utils.project import get_project_settings

from ProxyIP.items import FreeProxyIPItem

class XicidailiFreeSpider(scrapy.Spider):
    name = 'xicidaili_free'
    # allowed_domains = ['www.xicidaili.com']
    start_urls = ['fs.xicidaili.com:443','www.xicidaili.com:443']

    settings = get_project_settings()
    spider_page_start = settings.get('SPIDER_PAGE_START')
    spider_page_end = settings.get('SPIDER_PAGE_END')
    auth_urls_info = settings.get('AUTH_URLS_INFO')
    def start_requests(self):
        headers = {
            "Proxy-Connection": "keep-alive"
            # "Cookie": "_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTY0MDgyMjgzMjZlM2YwZWYwNGY1MWVkZTNjMGEwMjdjBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUhPVzFpVkFTWHEvSVBUdXg4dWluRVM2ektoa2hvVnRFUXRlRmw3d1N3RTQ9BjsARg%3D%3D--49dff8a15b344fe141db6482f82188335998161c; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1576168612; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1576211530"
        }
        for start_url in self.start_urls:
            yield scrapy.Request(start_url, headers=headers,method="CONNECT",
                                 callback=self.parse, dont_filter=True)

    def parse(self, response):
        resp_txt = response.text
        html = etree.HTML(resp_txt)
        logger.info(html)

