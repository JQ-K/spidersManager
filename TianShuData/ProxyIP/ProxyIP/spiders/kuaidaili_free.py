# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from ProxyIP.utils.proxy import *
from ProxyIP.configs.website import AUTHURLSINFO
from ProxyIP.items import FreeProxyIPItem
import time




class KuaidailiFreeSpider(scrapy.Spider):
    name = 'kuaidaili_free'
    allowed_domains = ['www.kuaidaili.com']
    start_urls = ['https://www.kuaidaili.com/free/inha/{}/'.format(page) for page in range(1, 5)]


    def __init__(self,resp_speed_limit=3,ip_type='HTTP'):
        self.resp_speed_limit=resp_speed_limit
        self.ip_type=ip_type


    def start_requests(self):
        for start_url in self.start_urls:
            time.sleep(5)
            yield scrapy.Request(start_url,
                                 callback=self.parse, dont_filter=True)


    def parse(self, response):
        resp_txt = response.text
        html = etree.HTML(resp_txt)
        tbody_trs = html.xpath(('//*[@id="list"]/table/tbody/tr'))[1::]
        for auth_url_info in AUTHURLSINFO:
            proxy_ips = []
            proxy_ip_item = FreeProxyIPItem()
            proxy_ip_item['name'] = auth_url_info['name']
            proxy_ip_item['url'] = auth_url_info['url']
            proxy_ip_item['source'] = self.name
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
            proxy_ip_item['proxyip'] = proxy_ips
            yield proxy_ip_item