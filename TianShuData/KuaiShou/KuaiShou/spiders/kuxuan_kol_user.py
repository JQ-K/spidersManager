# -*- coding: utf-8 -*-
import scrapy
import json
import random, time

from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuxuanKolUserItem


class KuxuanKolUserSpider(scrapy.Spider):
    """
    这是一个根据酷炫KOL列表接口获取seeds，并以快手的user_id为切入点，补全相关作者的基本信息，构建KOL种子库的爬虫工程
    """
    name = 'kuxuan_kol_user'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 701,
        'KuaiShou.pipelines.KuaishouUserSeedsMySQLPipeline': 700
    }}
    settings = get_project_settings()
    # allowed_domains = ['dataapi.kuxuan-inc.com']
    sort_type = settings.get('SPIDER_KUXUAN_SORT_TYPE')
    start_urls = ['http://dataapi.kuxuan-inc.com/api/kwaiUser/index?sort_type={}&page=6792'.format(sort_type)]

    def parse(self, response):
        rsp_json = json.loads(response.text)
        logger.info(rsp_json)
        if rsp_json['errno'] != '0':
            logger.error('API response error: %s' % response.text)
            return
        current_page_num = int(rsp_json['rst']['pageInfo']['page'])
        page_limit = self.settings.get('SPIDER_KUXUAN_PAGE_LIMIT')
        if page_limit <= 0:
            page_limit = int(rsp_json['rst']['pageInfo']['pages'])
        if current_page_num < page_limit:
            try:
                time.sleep(random.randint(3, 7))
                page_url = 'http://dataapi.kuxuan-inc.com/api/kwaiUser/index?sort_type={}&page={}'.format(
                    self.sort_type,
                    current_page_num + 1)
                logger.info('Request page url: %s' % page_url)
                yield scrapy.Request(page_url, callback=self.parse, dont_filter=True)
            except Exception as e:
                logger.error('scrapy.Request.errback: %s' % e)
        data = rsp_json['rst']['data']
        for user_dict in data:
            kuxuan_kol_user_item = KuxuanKolUserItem()
            kuxuan_kol_user_item['name'] = self.name
            for key, value in user_dict.items():
                kuxuan_kol_user_item[key] = value 
            yield kuxuan_kol_user_item
