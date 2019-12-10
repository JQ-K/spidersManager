# -*- coding: utf-8 -*-
import scrapy
import json

from pykafka import KafkaClient
from loguru import logger

from KuaiShou.settings import HOSTS, TOPIC, RESET_OFFSET_ON_START, USER_INFO_QUERY
from KuaiShou.items import KuaishouUserInfoIterm

class KuaishouUserInfoSpider(scrapy.Spider):
    name = 'kuaishou_user_info'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouPipeline': 700
    }}
    allowed_domains = ['live.kuaishou.com/graphql']
    # start_urls = ['http://live.kuaishou.com/graphql/']

    def start_requests(self):
        # 配置kafka连接信息
        client = KafkaClient(hosts=HOSTS)
        topic = client.topics[TOPIC]
        # 配置kafka消费信息
        consumer = topic.get_simple_consumer(
            consumer_group=self.name,
            reset_offset_on_start=RESET_OFFSET_ON_START
        )
        # 获取被消费数据的偏移量和消费内容
        for message in consumer:
            try:
                if message is None:
                    continue
                # 信息分为message.offset, message.value
                msg_value = message.value.decode()
                msg_value_dict = eval(msg_value)
                if msg_value_dict['name'] != 'kuxuan_kol_user':
                    continue
                kwai_id = msg_value_dict['kwaiId']
                user_info_query = USER_INFO_QUERY
                user_info_query['variables']['principalId'] = kwai_id
                kuaikan_url = 'https://live.kuaishou.com/graphql'
                headers = {'content-type': 'application/json'}
                yield scrapy.Request(kuaikan_url, headers=headers, body=json.dumps(user_info_query),
                                     method='POST', callback=self.parse_user_info, meta={'bodyJson': user_info_query},
                                     cookies={'did':'web_d54ea5e1190a41e481809b9cd17f92aa'}
                                     )
            except Exception as e:
                logger.warning('Kafka message structure cannot be resolved :{}'.format(e))


    def parse_user_info(self, response):
        rsp_json = json.loads(response.text)
        user_info = rsp_json['data']['userInfo']
        if user_info['id'] == None:
            body_json = response.meta['bodyJson']
            principal_id = body_json['variables']['principalId']
            logger.warning('UserInfoQuery failed, principalId:{}'.format(principal_id))
        kuaishou_user_info_iterm = KuaishouUserInfoIterm()
        kuaishou_user_info_iterm['name'] = self.name
        kuaishou_user_info_iterm['user_info'] = user_info
        return kuaishou_user_info_iterm