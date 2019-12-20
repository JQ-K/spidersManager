# -*- coding: utf-8 -*-
import scrapy
import json

from loguru import logger
from scrapy.utils.project import get_project_settings
from pykafka import KafkaClient
from loguru import logger

from KuaiShou.items import KuxuanKolUserItem
from KuaiShou.utils.did import RegisterCookie

class KuaishouSearchUserSpider(scrapy.Spider):
    name = 'kuaishou_search_user'
    # allowed_domains = ['live.kuaishou.com/graphql']
    # start_urls = ['http://live.kuaishou.com/graphql/']

    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouUserSeedsMySQLPipeline': 700
    }}
    settings = get_project_settings()

    def start_requests(self):
        # 配置kafka连接信息
        kafka_hosts = self.settings.get('KAFKA_HOSTS')
        kafka_topic = self.settings.get('KAFKA_TOPIC')
        reset_offset_on_start = self.settings.get('RESET_OFFSET_ON_START')
        search_overview_query = self.settings.get('SEARCH_OVERVIEW_QUERY')
        logger.info('kafka info, hosts:{}, topic:{}'.format(kafka_hosts, kafka_topic))
        client = KafkaClient(hosts=kafka_hosts)
        topic = client.topics[kafka_topic]
        # 配置kafka消费信息
        consumer = topic.get_simple_consumer(
            consumer_group=self.name,
            reset_offset_on_start=False
        )
        # 获取被消费数据的偏移量和消费内容
        for message in consumer:
            try:
                if message is None:
                    continue
                # 信息分为message.offset, message.value
                msg_value = message.value.decode()
                msg_value_dict = eval(msg_value)
                if 'name' not in list(msg_value_dict.keys()):
                    continue
                if msg_value_dict['name'] != 'kuanshou_seeds_search':
                    continue
                kwai_id = msg_value_dict['kwaiId']
                # 查询principalId、处理kwaiId(为空的情况)
                kuaishou_url = 'https://live.kuaishou.com/graphql'
                search_overview_query = self.settings.get('SEARCH_OVERVIEW_QUERY')
                headers = {'content-type': 'application/json'}
                headers['Cookie'] = 'did=web_7ef156e926594648990971638b830053'
                search_overview_query['variables']['keyword'] = '{}'.format(kwai_id)
                logger.info(search_overview_query)
                yield scrapy.Request(kuaishou_url, headers=headers, body=json.dumps(search_overview_query),
                                     method='POST',
                                     meta={'bodyJson': search_overview_query, 'msg_value_dict': msg_value_dict},
                                     callback=self.parse_search_overview, dont_filter=True
                                     )
                break
            except Exception as e:
                logger.warning('Kafka message[{}] structure cannot be resolved :{}'.format(str(msg_value_dict),e))


    def parse_search_overview(self, response):
        rsp_search_overview_json = json.loads(response.text)
        logger.info(rsp_search_overview_json)
        search_overview_list = rsp_search_overview_json['data']['searchOverview']['list']
        for search_overview in search_overview_list:
            if search_overview['type'] != 'authors':
                continue
            for  author_info in search_overview['list']:
                principal_id = author_info['id']
                kuaishou_url = 'http://live.kuaishou.com/graphql'
                user_info_query = self.settings.get('USER_INFO_QUERY')
                headers = {'content-type': 'application/json'}
                headers['Cookie'] = 'did=web_7ef156e926594648990971638b830053'
                user_info_query['variables']['principalId'] = '3xbyt4rb5kwkh9w'#principal_id
                logger.info(user_info_query)
                yield scrapy.Request(kuaishou_url, headers=headers, body=json.dumps(user_info_query),
                                     method='POST',
                                     meta={'bodyJson': user_info_query},
                                     callback=self.parse_search_user_info, dont_filter=True
                                     )


    def parse_search_user_info(self, response):
        rsp_json = json.loads(response.text)
        user_info = rsp_json['data']['userInfo']
        if user_info == None:
            logger.warning('UserInfoQuery failed, error:{}'.format(str(rsp_json).replace('\n', '')))
            return
        logger.info('Search userinfo reslut: {}'.format(str(user_info)))
        kuxuan_kol_user_item = KuxuanKolUserItem()
        kuxuan_kol_user_item['user_id'] = user_info['userId']
        kuxuan_kol_user_item['kwaiId'] = user_info['kwaiId']
        kuxuan_kol_user_item['principalId'] = user_info['principalId']
        kuxuan_kol_user_item['fan'] = False
        # yield kuxuan_kol_user_item
