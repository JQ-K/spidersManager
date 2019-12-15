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
    start_urls = ['http://dataapi.kuxuan-inc.com/api/kwaiUser/index?sort_type={}&page=1001'.format(sort_type)]

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
            kuxuan_kol_user_dic = {}
            kuxuan_kol_user_dic['name'] = self.name
            for key, value in user_dict.items():
                kuxuan_kol_user_dic[key] = value
                kuxuan_kol_user_item[key] = value 
            yield kuxuan_kol_user_item
            # 查询principalId、处理kwaiId(为空的情况)
            # kuaishou_url = 'http://live.kuaishou.com/graphql'
            # search_overview_query = self.settings.get('SEARCH_OVERVIEW_QUERY')
            # headers = {'content-type': 'application/json'}
            # headers[
            #     'Cookie'] = 'userId=1537755176; userId=1537755176; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1575275330,1575340982,1575964896,1576347519; Hm_lpvt_86a27b7db2c5c0ae37fee4a8a35033ee=1576347524; kuaishou.live.bfb1s=9b8f70844293bed778aade6e0a8f9942; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgATU5EUJGakt2uRpJwABd9rwx18j2i5ZzhOidmQh6pk_ZGJS2u0HJ4lvIwLkh0EbcwhIcFbM9_mSg5IERaD3JSyMUHjTqstc-9ekOtalUMCKkgUAYFZI22rJL5b2oo4dfcAMCAp3SLXB7YABxF6dWBUTgNT72_JvdRxz4CgndjJiq5fSLUP1Nw150Vmn6W-Y_NTQTPRkOb2n8kR2LvEPyWnAaEgCrAu8bFEUPixNgRvVq1Nb0ZSIgWWhgVYyBZuCGYlOGJOaUUem08VzV7gCmIxPRQ8QKXwkoBTAB; kuaishou.live.web_ph=c6d3e8dc7b1ad75478d960f87693ef27cfbc'
            # search_overview_query['variables']['keyword'] = str(kuxuan_kol_user_dic['user_name'])
            # yield scrapy.Request(kuaishou_url, headers=headers, body=json.dumps(search_overview_query),
            #                      method='POST',
            #                      meta={'bodyJson': search_overview_query, 'kuxuan_kol_user_dic': kuxuan_kol_user_dic},
            #                      callback=self.parse_search_overview, dont_filter=True
            #                      )

    # def parse_search_overview(self, response):
    #     """
    #     处理SEARCH_OVERVIEW_QUERY查询接口的查询结果，主要是查询 principalId 的值 和 处理 kwaiId 为空的情况
    #     :param response:
    #     :return:
    #     """
    #     kuxuan_kol_user_dic = response.meta['kuxuan_kol_user_dic']
    #     # 查询 principalId
    #     kuxuan_kol_user_item = KuxuanKolUserItem()
    #     for key, value in kuxuan_kol_user_dic.items():
    #         kuxuan_kol_user_item[key] = value
    #     rsp_search_overview_json = json.loads(response.text)
    #     search_overview_list = rsp_search_overview_json['data']['searchOverview']['list']
    #     for search_overview_res in search_overview_list:
    #         if search_overview_res['type'] != 'authors': continue
    #         search_overview_author_list = search_overview_res['list']
    #         if search_overview_author_list == []: continue
    #         for search_overview_author in search_overview_author_list:
    #             # 判断搜索的结果是否匹配
    #             if kuxuan_kol_user_item['user_name'] != search_overview_author['name'] and kuxuan_kol_user_item[
    #                 'kwaiId'] != search_overview_author['id']:
    #                 continue
    #             kuxuan_kol_user_item['principalId'] = search_overview_author['id']
    #     # 第二次处理 principalId
    #     kuaishou_url = 'http://live.kuaishou.com/graphql'
    #     search_detail_query = self.settings.get('SEARCH_DETAIL_QUERY')
    #     headers = {'content-type': 'application/json'}
    #     headers[
    #         'Cookie'] = 'userId=1537755176; userId=1537755176; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1575275330,1575340982,1575964896,1576347519; Hm_lpvt_86a27b7db2c5c0ae37fee4a8a35033ee=1576347524; kuaishou.live.bfb1s=9b8f70844293bed778aade6e0a8f9942; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgATU5EUJGakt2uRpJwABd9rwx18j2i5ZzhOidmQh6pk_ZGJS2u0HJ4lvIwLkh0EbcwhIcFbM9_mSg5IERaD3JSyMUHjTqstc-9ekOtalUMCKkgUAYFZI22rJL5b2oo4dfcAMCAp3SLXB7YABxF6dWBUTgNT72_JvdRxz4CgndjJiq5fSLUP1Nw150Vmn6W-Y_NTQTPRkOb2n8kR2LvEPyWnAaEgCrAu8bFEUPixNgRvVq1Nb0ZSIgWWhgVYyBZuCGYlOGJOaUUem08VzV7gCmIxPRQ8QKXwkoBTAB; kuaishou.live.web_ph=c6d3e8dc7b1ad75478d960f87693ef27cfbc'
    #     if 'principalId' not in list(kuxuan_kol_user_item.keys()) and kuxuan_kol_user_dic['kwaiId'] != '':
    #         search_detail_query['variables']['keyword'] = str(kuxuan_kol_user_dic['kwaiId'])
    #         yield scrapy.Request(kuaishou_url, headers=headers, body=json.dumps(search_detail_query),
    #                              method='POST',
    #                              meta={'bodyJson': search_detail_query, 'kuxuan_kol_user_dic': kuxuan_kol_user_dic},
    #                              callback=self.parse_principal_id, dont_filter=True
    #                              )
    #     elif 'principalId' not in list(kuxuan_kol_user_item.keys()) and kuxuan_kol_user_dic['kwaiId'] == '':
    #         search_detail_query['variables']['keyword'] = str(kuxuan_kol_user_dic['user_id'])
    #         yield scrapy.Request(kuaishou_url, headers=headers, body=json.dumps(search_detail_query),
    #                              method='POST',
    #                              meta={'bodyJson': search_detail_query, 'kuxuan_kol_user_dic': kuxuan_kol_user_dic},
    #                              callback=self.parse_principal_id, dont_filter=True
    #                              )
    #     logger.info('kuxuan kol user item: %s' % str(kuxuan_kol_user_item))
    #     yield kuxuan_kol_user_item
    #
    # def parse_principal_id(self, response):
    #     # 第三次次处理 principalId，通过kuaiid查
    #     kuxuan_kol_user_dic = response.meta['kuxuan_kol_user_dic']
    #     # 查询 principalId
    #     kuxuan_kol_user_item = KuxuanKolUserItem()
    #     for key, value in kuxuan_kol_user_dic.items():
    #         kuxuan_kol_user_item[key] = value
    #     rsp_search_overview_json = json.loads(response.text)
    #     search_overview_list = rsp_search_overview_json['data']['searchOverview']['list']
    #     for search_overview_res in search_overview_list:
    #         if search_overview_res['type'] != 'authors': continue
    #         search_overview_author_list = search_overview_res['list']
    #         if search_overview_author_list == []: continue
    #         for search_overview_author in search_overview_author_list:
    #             # 判断搜索的结果是否匹配
    #             if kuxuan_kol_user_item['user_name'] != search_overview_author['name'] or kuxuan_kol_user_item[
    #                 'kwaiId'] != search_overview_author['id']:
    #                 continue
    #             kuxuan_kol_user_item['principalId'] = search_overview_author['id']
    #     logger.info('kuxuan kol user item: %s' % str(kuxuan_kol_user_item))
    #     yield kuxuan_kol_user_item
