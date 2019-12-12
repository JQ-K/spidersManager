# -*- coding: utf-8 -*-
import scrapy
import json
import random, time
from loguru import logger

from KuaiShou.items import KuxuanKolUserItem


class KuxuanKolUserSpider(scrapy.Spider):
    name = 'kuxuan_kol_user'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouPipeline': 700
    }}
    allowed_domains = ['dataapi.kuxuan-inc.com']
    start_urls = ['http://dataapi.kuxuan-inc.com/api/kwaiUser/index?sort_type=2&page=1']

    def parse(self, response):
        rsp_json = json.loads(response.text)
        if rsp_json['errno'] != '0':
            logger.error('API response error: %s' % response.text)
            return
        if int(rsp_json['rst']['pageInfo']['page']) < 5:  # int(rsp_json['rst']['pageInfo']['pages']):
            time.sleep(random.randint(3, 7))
            page_url = 'http://dataapi.kuxuan-inc.com/api/kwaiUser/index?sort_type=2&page={}'.format(
                int(rsp_json['rst']['pageInfo']['page']) + 1)
            logger.info('Request page url: %s' % page_url)
            yield scrapy.Request(page_url, callback=self.parse, dont_filter=True)
        data = rsp_json['rst']['data']
        for user_dict in data:
            kuxuan_kol_user_item = KuxuanKolUserItem()
            kuxuan_kol_user_item['name'] = self.name
            for key, value in user_dict.items():
                kuxuan_kol_user_item[key] = value
            logger.info('kuxuan kol user item: %s' % str(user_dict))
            yield kuxuan_kol_user_item
