# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from ProxyIP.utils.proxy import *
from ProxyIP.settings import AUTH_URLS_INFO, SPIDER_PAGE_START, SPIDER_PAGE_END
from ProxyIP.items import FreeProxyIPItem

class Ip3366FreeSpider(scrapy.Spider):
    name = 'ip3366_free'
    allowed_domains = ['www.ip3366.net']
    start_urls = ['http://www.ip3366.net/free/?stype=1&page={}'.format(page) for page in range(SPIDER_PAGE_START, SPIDER_PAGE_END)]


    def __init__(self,resp_speed_limit=3,ip_type='HTTP'):
        self.resp_speed_limit=resp_speed_limit
        self.ip_type=ip_type


    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(start_url,
                                 callback=self.parse, dont_filter=True)


    def parse(self, response):
        resp_txt = response.text
        html = etree.HTML(resp_txt)
        tbody_trs = html.xpath(('//*[@id="list"]/table/tbody/tr'))
        for auth_url_info in AUTH_URLS_INFO:
            proxy_ips = []
            proxy_ip_item = FreeProxyIPItem()
            proxy_ip_item['name'] = self.name
            proxy_ip_item['url'] = auth_url_info['url']
            proxy_ip_item['url_name'] = auth_url_info['name']
            for tbody_tr in tbody_trs:
                try:
                    ip = tbody_tr.xpath('td')[0].text.replace(' ', '').replace('\r\n', '')
                    port = tbody_tr.xpath('td')[1].text.replace(' ', '').replace('\r\n', '')
                    ip_types = tbody_tr.xpath('td')[3].text.replace(' ', '').replace('\r\n', '')
                    resp_speed = float(tbody_tr.xpath('td')[5].text.replace(' ', '').replace('\r\n', '')[:-1])
                    update_time = tbody_tr.xpath('td')[6].text.replace('\r\n', '')

                    if self.ip_type not in ip_types:
                        continue
                    if resp_speed > self.resp_speed_limit:
                        continue
                    proxy_ip = {self.ip_type: '{}:{}'.format(ip, port)}
                    if ProxyAuthentication(auth_url_info['url'], proxy_ip) == None:
                        continue
                    proxy_ips.append(proxy_ip)
                except Exception as e:
                    print(u'警告：解析失败！错误提示:{}'.format(e))
            proxy_ip_item['proxyip_list'] = proxy_ips
            yield proxy_ip_item

