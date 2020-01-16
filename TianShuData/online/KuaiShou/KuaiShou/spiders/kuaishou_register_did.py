# -*- coding: utf-8 -*-
import scrapy
import re, time
import json, random

from scrapy.utils.project import get_project_settings
from loguru import logger
from redis import Redis

from KuaiShou.utils import ProduceRandomStr
from KuaiShou.items import KuaishouCookieInfoItem


class KuaishouRegisterDidSpider(scrapy.Spider):
    name = 'kuaishou_register_did'
    # allowed_domains = ['live.kuaishou.com/graphql']
    # start_urls = ['https://live.kuaishou.com/graphql/']
    custom_settings = {'ITEM_PIPELINES':
                           {'KuaiShou.pipelines.KuaishouRedisPipeline': 700},
                       'CONCURRENT_REQUESTS': 16
                       }
    settings = get_project_settings()

    redis_host = settings.get('REDIS_HOST')
    redis_port = settings.get('REDIS_PORT')
    redis_did_name = settings.get('REDIS_DID_NAME')
    redis_did_expire_time = settings.get('REDIS_DID_EXPIRE_TIME')
    conn = Redis(host=redis_host, port=redis_port)

    def __init__(self, useProxy='0', *args, **kwargs):
        super(KuaishouRegisterDidSpider, self).__init__(*args, **kwargs)
        self.useProxy = int(useProxy)

    def start_requests(self):
        start_url = 'http://live.kuaishou.com/v/hot/'
        spider_did_supplements_quantity_per_time = self.settings.get('SPIDER_DID_SUPPLEMENTS_QUANTITY_PER_TIME')
        spider_did_pool_warning_line = self.settings.get('SPIDER_DID_POOL_WARNING_LINE')
        while True:
            # zremrangebyscore(name, min, max)
            max_score = int(time.time()) - int(self.redis_did_expire_time)
            self.conn.zremrangebyscore(self.redis_did_name,0,max_score)
            did_pool_quantity = self.conn.zcard(self.redis_did_name)
            logger.info('Did pool quantity: {}'.format(did_pool_quantity))
            if did_pool_quantity > spider_did_pool_warning_line:
                time.sleep(10)
                continue
            counter = 0
            while counter < spider_did_supplements_quantity_per_time:
                counter += 1
                time.sleep(random.randint(3, 6))
                yield scrapy.Request(start_url, method='GET', callback=self.produce_did, dont_filter=True)

    def produce_did(self, response):
        referer = response.url
        time_int = int(time.time() * 1000)
        register_url = 'http://live.kuaishou.com/rest/wd/live/web/log'
        payload_data = {
            "base": {
                "session_id": ProduceRandomStr(16),
                "page_id": '{}_{}'.format(ProduceRandomStr(16), time_int - 1012),
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
                    "event_time": time_int - 1012,
                    "from": "/",
                    "to": "/v/hot/",
                    "is_spammer": 'false'
                }
            }]
        }
        headers = {
            'kpf': 'PC_WEB',
            'kpn': 'GAME_ZONE',
            'Content-Type': 'text/plain;charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'
        }
        return scrapy.Request(register_url, headers=headers, body=json.dumps(payload_data),
                             method='POST', callback=self.register_did,
                             dont_filter=True
                             )

    def register_did(self, response):
        kuaishou_cookie_info_item = KuaishouCookieInfoItem()
        set_cookie_list = response.headers.getlist('Set-Cookie')
        if set_cookie_list == []:
            return
        cookie_str = ''
        for cookie in set_cookie_list:
            cookie_str += cookie.decode().split(';')[0] + ';'
        kuaishou_cookie_info_item['Cookie'] = cookie_str[:-1]
        logger.info(kuaishou_cookie_info_item)
        return kuaishou_cookie_info_item
