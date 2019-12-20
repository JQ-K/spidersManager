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
        search_overview_query = self.settings.get('SEARCH_DETAIL_QUERY')
        logger.info('======================================')
        headers = {'content-type': 'application/json'}
        headers[
            'Cookie'] = 'userId=1537755176; userId=1537755176; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1575275330,1575340982,1575964896,1576347519; Hm_lpvt_86a27b7db2c5c0ae37fee4a8a35033ee=1576347524; kuaishou.live.bfb1s=9b8f70844293bed778aade6e0a8f9942; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgATU5EUJGakt2uRpJwABd9rwx18j2i5ZzhOidmQh6pk_ZGJS2u0HJ4lvIwLkh0EbcwhIcFbM9_mSg5IERaD3JSyMUHjTqstc-9ekOtalUMCKkgUAYFZI22rJL5b2oo4dfcAMCAp3SLXB7YABxF6dWBUTgNT72_JvdRxz4CgndjJiq5fSLUP1Nw150Vmn6W-Y_NTQTPRkOb2n8kR2LvEPyWnAaEgCrAu8bFEUPixNgRvVq1Nb0ZSIgWWhgVYyBZuCGYlOGJOaUUem08VzV7gCmIxPRQ8QKXwkoBTAB; kuaishou.live.web_ph=c6d3e8dc7b1ad75478d960f87693ef27cfbc'
        search_overview_query['variables']['keyword'] = '逗妹.和平精英'
        for start_url in self.start_urls:
            yield scrapy.Request(start_url, headers=headers, body=json.dumps(search_overview_query),
                                 method='POST', meta={'bodyJson': search_overview_query},
                                 callback=self.parse_search_overview, dont_filter=True
                                 )

    def parse_search_overview(self, response):
        logger.info('======================================')
        logger.info(response.text)
