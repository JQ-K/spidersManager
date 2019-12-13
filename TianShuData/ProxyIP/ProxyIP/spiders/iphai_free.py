# -*- coding: utf-8 -*-
import scrapy
import json,re
from lxml import etree
from loguru import logger
from scrapy.utils.project import get_project_settings

from ProxyIP.items import FreeProxyIPItem


class IphaiFreeSpider(scrapy.Spider):
    name = 'iphai_free'
    allowed_domains = ['www.iphai.com/free/ng']
    start_urls = ['http://www.iphai.com/free/ng']

    settings = get_project_settings()
    spider_page_start = settings.get('SPIDER_PAGE_START')
    spider_page_end = settings.get('SPIDER_PAGE_END')
    auth_urls_info = settings.get('AUTH_URLS_INFO')
    def start_requests(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "www.iphai.com",
            "Referer": "http://www.iphai.com/free/wp",
            "Upgrade-Insecure-Requests": "1"
        }
        for start_url in self.start_urls:
            yield scrapy.Request(start_url, headers=headers,
                                 callback=self.parse, dont_filter=True)

    def parse(self, response):
        resp_txt = response.text
        html = etree.HTML(resp_txt)
        result_trs = html.xpath('/html/body/div[2]/div[2]/table/tr')[1::]
        for auth_url_info in self.auth_urls_info:
            self.proxy_ip_item = FreeProxyIPItem()
            self.proxy_ip_item['name'] = self.name
            self.proxy_ip_item['url'] = auth_url_info['url']
            self.proxy_ip_item['url_name'] = auth_url_info['name']
            for result_tr in result_trs:
                try:
                    ip = re.findall('([0-9\.]+)',result_tr.xpath('td')[0].text)[0]
                    port = re.findall('([0-9]+)',result_tr.xpath('td')[1].text)[0]
                    ip_types_list = re.findall('([http|https]+)',result_tr.xpath('td')[3].text.lower())
                    if ip_types_list == [] or 'http' in ip_types_list:
                       ip_types = 'http'
                    if 'https' in ip_types_list:
                        ip_types = 'https'
                    respspeed = float(re.findall('([0-9\.]+)',result_tr.xpath('td')[5].text)[0])
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
