# -*- coding: utf-8 -*-
import scrapy
import json

from scrapy.utils.project import get_project_settings
from loguru import logger

class KuaishouTestSpider(scrapy.Spider):
    name = 'kuaishou_test'
    # allowed_domains = ['dataapi.kuxuan-inc.com']
    start_urls = ['http://live.kuaishou.com/graphql']
    Settings = get_project_settings().get('SEARCH_OVERVIEW_QUERY')

    def start_requests(self):
        search_overview_query = self.settings.get('SEARCH_OVERVIEW_QUERY')
        logger.info('======================================')
        headers = {'content-type': 'application/json'}
        search_overview_query['variables']['keyword'] = '11'
        for start_url in self.start_urls:
            yield scrapy.Request(start_url, headers=headers, body=json.dumps(search_overview_query),
                                 method='POST', meta={'bodyJson': search_overview_query},
                                 callback=self.parse_search_overview, dont_filter=True
                                 )

    def parse_search_overview(self, response):
        logger.info(response.text)
