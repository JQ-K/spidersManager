# -*- coding: utf-8 -*-
import scrapy
import json,re
from lxml import etree
from loguru import logger
from scrapy.utils.project import get_project_settings

from ProxyIP.items import FreeProxyIPItem


class Y89ipFreeSpider(scrapy.Spider):
    name = 'y89ip_free'
    # allowed_domains = ['www.89ip.cn']
    settings = get_project_settings()
    spider_page_start = settings.get('SPIDER_PAGE_START')
    spider_page_end = settings.get('SPIDER_PAGE_END')
    auth_urls_info = settings.get('AUTH_URLS_INFO')
    start_urls = ['http://www.89ip.cn/index_{}.html/'.format(page) for page in
                  range(spider_page_start, spider_page_end)]

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(start_url,
                                 callback=self.parse, dont_filter=True)

    def parse(self, response):
        resp_txt = response.text
        html = etree.HTML(resp_txt)
        result_trs = html.xpath('//tr')
        for auth_url_info in self.auth_urls_info:
            self.proxy_ip_item = FreeProxyIPItem()
            self.proxy_ip_item['name'] = self.name
            self.proxy_ip_item['url'] = auth_url_info['url']
            self.proxy_ip_item['url_name'] = auth_url_info['name']
            for result_tr in result_trs:
                try:
                    if result_tr[0].tag == 'th':
                        continue
                    ip = re.findall('([0-9\.]+)', result_tr[0].text)[0]
                    port = re.findall('([0-9]+)', result_tr[1].text)[0]
                    ip_types = 'http'
                    url_type = re.findall('(http|https)://.*?', auth_url_info['url'])[0].lower()
                    if url_type == 'https' and 'https' not in ip_types:
                        continue
                    proxy = '{}://{}:{}'.format(url_type, ip, port)
                    headers = {'content-type': 'application/json'}
                    yield scrapy.Request(auth_url_info['url'], headers=headers, body=json.dumps(auth_url_info['body']),
                                         method='POST', callback=self.auth_proxyip,
                                         meta={'bodyJson': auth_url_info['body'], 'proxy': proxy},
                                         dont_filter=True
                                         )
                except Exception as e:
                    logger.warning('警告：解析失败！错误提示:{}'.format(e))

    def auth_proxyip(self, response):
        self.proxy_ip_item['proxy'] = response.meta['proxy']
        logger.info(response.meta['proxy'])
        yield self.proxy_ip_item

