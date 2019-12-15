# -*- coding: utf-8 -*-
import scrapy
import json, re
from lxml import etree
from loguru import logger
from scrapy.utils.project import get_project_settings

from ProxyIP.items import FreeProxyIPItem
import time


class KuaidailiFreeSpider(scrapy.Spider):
    name = 'kuaidaili_free'
    settings = get_project_settings()
    spider_page_start = settings.get('SPIDER_PAGE_START')
    spider_page_end = settings.get('SPIDER_PAGE_END')
    auth_urls_info = settings.get('AUTH_URLS_INFO')
    allowed_domains = ['www.kuaidaili.com']
    start_urls = ['https://www.kuaidaili.com/free/intr/{}/'.format(page) for page in
                  range(spider_page_start, spider_page_end)] + ['https://www.kuaidaili.com/free/intr/{}/'.format(page)
                                                                for page in range(spider_page_start, spider_page_end)]

    def start_requests(self):
        for start_url in self.start_urls:
            time.sleep(5)
            yield scrapy.Request(start_url,
                                 callback=self.parse, dont_filter=True)

    def parse(self, response):
        resp_txt = response.text
        html = etree.HTML(resp_txt)
        tbody_trs = html.xpath(('//*[@id="list"]/table/tbody/tr'))[1::]
        for auth_url_info in self.auth_urls_info:
            self.proxy_ip_item = FreeProxyIPItem()
            self.proxy_ip_item['name'] = self.name
            self.proxy_ip_item['url'] = auth_url_info['url']
            self.proxy_ip_item['url_name'] = auth_url_info['name']
            for tbody_tr in tbody_trs:
                try:
                    ip = tbody_tr.xpath('td')[0].text.replace(' ', '').replace('\r\n', '')
                    port = tbody_tr.xpath('td')[1].text.replace(' ', '').replace('\r\n', '')
                    ip_types = tbody_tr.xpath('td')[3].text.replace(' ', '').replace('\r\n', '')
                    resp_speed = float(tbody_tr.xpath('td')[5].text.replace(' ', '').replace('\r\n', '')[:-1])
                    update_time = tbody_tr.xpath('td')[6].text.replace('\r\n', '')
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
