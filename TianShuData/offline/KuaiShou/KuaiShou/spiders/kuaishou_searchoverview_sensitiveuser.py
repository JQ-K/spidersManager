# -*- coding: utf-8 -*-
import scrapy
import json

from scrapy.utils.project import get_project_settings
from pykafka import KafkaClient
from loguru import logger

from KuaiShou.items import KuaishouUserInfoIterm

class KuaishouSearchUserSpider(scrapy.Spider):
    name = 'kuaishou_searchoverview_sensitiveuser'
    # allowed_domains = ['live.kuaishou.com/graphql']
    # start_urls = ['http://live.kuaishou.com/graphql/']

    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouUserSeedsMySQLPipeline': 700,
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 701
    }}
    settings = get_project_settings()

    def start_requests(self):
        # 配置kafka连接信息
        kafka_hosts = self.settings.get('KAFKA_HOSTS')
        kafka_topic = self.settings.get('KAFKA_TOPIC')
        search_overview_query = self.settings.get('SEARCH_OVERVIEW_QUERY')
        logger.info('kafka info, hosts:{}, topic:{}'.format(kafka_hosts, kafka_topic))
        client = KafkaClient(hosts=kafka_hosts)
        topic = client.topics[kafka_topic]
        # 配置kafka消费信息
        consumer = topic.get_balanced_consumer(
            consumer_group=self.name,
            managed=True,
            auto_commit_enable=True
        )
        kuaishou_url = 'https://live.kuaishou.com/m_graphql'
        headers = {'content-type': 'application/json'}
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
                if msg_value_dict['spider_name'] != 'kuanshou_seeds_search':
                    continue
                kwai_id = msg_value_dict['kwaiId']
                # 查询principalId、处理kwaiId(为空的情况)
                search_overview_query['variables']['keyword'] = '{}'.format(kwai_id)
                # logger.info(search_overview_query)
                yield scrapy.Request(kuaishou_url, headers=headers, body=json.dumps(search_overview_query),
                                     method='POST',
                                     meta={'bodyJson': search_overview_query, 'msg_value_dict': msg_value_dict},
                                     callback=self.parse_search_overview, dont_filter=True
                                     )
            except Exception as e:
                logger.warning('Kafka message[{}] structure cannot be resolved :{}'.format(str(msg_value_dict),e))


    def parse_search_overview(self, response):
        rsp_search_overview_json = json.loads(response.text)
        logger.info(rsp_search_overview_json)
        pc_search_overview = rsp_search_overview_json['data']['pcSearchOverview']
        if pc_search_overview == None:
            logger.warning('pcSearchOverview failed, result is None')
            return
        kuaishou_url = 'http://live.kuaishou.com/graphql'
        sensitive_user_info_query = self.settings.get('SENSITIVE_USER_INFO_QUERY')
        headers = {'content-type': 'application/json'}
        search_overview_list = pc_search_overview['list']
        for search_overview in search_overview_list:
            if search_overview['type'] != 'authors':
                continue
            author_info_dict = {}
            for  author_info in search_overview['list']:
                author_info_dict['principalId'] = author_info['id']
                author_info_dict['nickname'] = author_info['name']
                author_info_dict['avatar'] = author_info['avatar']
                author_info_dict['sex'] = author_info['sex']
                author_info_dict['description'] = author_info['description']
                author_info_dict['fan'] = author_info['counts']['fan']
                author_info_dict['follow'] = author_info['counts']['follow']
                author_info_dict['photo'] = author_info['counts']['photo']
                sensitive_user_info_query['variables']['principalId'] = author_info_dict['principalId']
                # logger.info(sensitive_user_info_query)
                yield scrapy.Request(kuaishou_url, headers=headers, body=json.dumps(sensitive_user_info_query),
                                     method='POST',
                                     meta={'bodyJson': sensitive_user_info_query,'author_info_dict':author_info_dict},
                                     callback=self.parse_search_user_info, dont_filter=True
                                     )


    def parse_search_user_info(self, response):
        rsp_json = json.loads(response.text)
        user_info = rsp_json['data']['sensitiveUserInfo']
        if user_info == None:
            logger.warning('UserInfoQuery failed, error:{}'.format(str(rsp_json).replace('\n', '')))
            return
        logger.info('Search userinfo reslut: {}'.format(str(user_info)))
        kuaishou_user_info_iterm = KuaishouUserInfoIterm()
        kuaishou_user_info_iterm['spider_name'] = self.name
        kuaishou_user_info_iterm['userId'] = user_info['userId']
        kuaishou_user_info_iterm['kwaiId'] = user_info['kwaiId']
        kuaishou_user_info_iterm['principalId'] = response.meta['author_info_dict']['principalId']
        kuaishou_user_info_iterm['nickname'] = response.meta['author_info_dict']['nickname']
        kuaishou_user_info_iterm['avatar'] = response.meta['author_info_dict']['avatar']
        kuaishou_user_info_iterm['sex'] = response.meta['author_info_dict']['sex']
        kuaishou_user_info_iterm['description'] = response.meta['author_info_dict']['description']
        kuaishou_user_info_iterm['constellation'] = user_info['constellation']
        kuaishou_user_info_iterm['cityName'] = user_info['cityName']
        kuaishou_user_info_iterm['fan'] = response.meta['author_info_dict']['fan']
        kuaishou_user_info_iterm['follow'] = response.meta['author_info_dict']['follow']
        kuaishou_user_info_iterm['photo'] = response.meta['author_info_dict']['photo']
        kuaishou_user_info_iterm['liked'] = user_info['countsInfo']['liked']
        kuaishou_user_info_iterm['open'] = user_info['countsInfo']['open']
        kuaishou_user_info_iterm['playback'] = user_info['countsInfo']['playback']
        yield kuaishou_user_info_iterm
