# -*- coding: utf-8 -*-
import scrapy
import json,re
from lxml import etree
from loguru import logger
from scrapy.utils.project import get_project_settings

from ProxyIP.items import FreeProxyIPItem


class IpyqieFreeSpider(scrapy.Spider):
    name = 'ipyqie_free'
    # allowed_domains = ['ip.yqie.com']
    start_urls = ['http://ip.yqie.com/ipproxy.htm']

    settings = get_project_settings()
    spider_page_start = settings.get('SPIDER_PAGE_START')
    spider_page_end = settings.get('SPIDER_PAGE_END')
    auth_urls_info = settings.get('AUTH_URLS_INFO')
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
                    ip =result_tr[0].text
                    port = result_tr[1].text
                    ip_types_list = result_tr[4].text.lower()
                    if ip_types_list == [] or 'http' in ip_types_list:
                       ip_types = 'http'
                    if 'https' in ip_types_list:
                        ip_types = 'https'
                    url_type = re.findall('(http|https)://.*?', auth_url_info['url'])[0].lower()
                    if url_type == 'https' and 'https' not in ip_types:
                        continue
                    proxy = '{}://{}:{}'.format(url_type, ip, port)
                    headers = {'content-type': 'application/json'}
                    yield scrapy.Request(auth_url_info['url'], headers=headers,
                                         body=json.dumps(auth_url_info['body']),
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