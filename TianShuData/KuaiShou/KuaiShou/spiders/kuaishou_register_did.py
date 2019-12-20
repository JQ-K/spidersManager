# -*- coding: utf-8 -*-
import scrapy

from loguru import logger
import re,time
import json, random

from KuaiShou.utils import ProduceRandomStr
from KuaiShou.items import KuaishouCookieInfoItem


class KuaishouRegisterDidSpider(scrapy.Spider):
    name = 'kuaishou_register_did'
    # allowed_domains = ['live.kuaishou.com/graphql']
    # start_urls = ['http://live.kuaishou.com/graphql/']
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouRedisPipeline': 700
    }}
    headers = {}

    def start_requests(self):
        start_url = 'https://live.kuaishou.com/v/hot/'
        yield scrapy.Request(start_url, method='GET', callback=self.produce_did)

    def produce_did(self, response):
        referer = response.url
        cookie = re.findall('(kuaishou\.live\.bfb1s=[0-9a-z]+; )', str(response.headers))[0] \
                 + re.findall('(clientid=\d{0,}; )', str(response.headers))[0] \
                 + re.findall('(did=web_[0-9a-z]+; )', str(response.headers))[0] \
                 + re.findall('(client_key=[0-9a-z]+; )', str(response.headers))[0] \
                 + re.findall('(didv=\d+)', str(response.headers))[0]
        time_int = int(time.time() * 1000)
        register_url = 'https://live.kuaishou.com/rest/wd/live/web/log'
        payload_data = {
            "base": {
                "session_id": ProduceRandomStr(16),
                "page_id": '{}_{}'.format(ProduceRandomStr(16),time_int-1012),
                "refer_page_id": "",
                "refer_show_id": "",
                "refer_url": referer,
                "page_live_stream_id": "",
                "url": referer,
                "screen": "1280*800",
                "platform": "MacIntel",
                "log_time": "{}".format(time_int)
            },
            "events": [{
                "type": "pv",
                "data": {
                    "event_time": time_int-1012,
                    "from": "/",
                    "to": "/v/hot/",
                    "is_spammer": 'false'
                }
            }]
        }

        self.headers['kpf'] = 'PC_WEB'
        self.headers['kpn'] = 'GAME_ZONE'
        self.headers['Content-Type'] = "text/plain;charset=UTF-8"
        self.headers['Accept-Encoding'] = 'gzip, deflate, br'
        self.headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
        self.headers['Connection'] = 'keep-alive'
        self.headers['Sec-Fetch-Mode'] = 'cors'
        self.headers['Sec-Fetch-Site'] = 'same-origin'
        self.headers['User-Agent'] = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'

        yield scrapy.Request(register_url, headers=self.headers, body=json.dumps(payload_data),
                           method='POST', meta={'cookie': cookie}, callback=self.register_did,
                           dont_filter=True
                           )

    def register_did(self,response):
        kuaishou_cookie_info_item = KuaishouCookieInfoItem()
        cookies = ''
        for cookie in response.headers.getlist('Set-Cookie'):
            cookie_str = cookie.decode().split(';')[0]
            key, value = cookie_str.split('=')
            cookies += '{}={}; '.format(key, value)
            kuaishou_cookie_info_item[key.replace('.', '_')] = value
        logger.info(kuaishou_cookie_info_item)
        time.sleep(random.randint(3, 6))
        yield kuaishou_cookie_info_item




