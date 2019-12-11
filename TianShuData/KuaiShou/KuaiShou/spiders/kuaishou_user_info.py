# -*- coding: utf-8 -*-
import scrapy
import json

from pykafka import KafkaClient
from loguru import logger
from redis import Redis

from KuaiShou.settings import KAFKA_HOSTS, KAFKA_TOPIC, RESET_OFFSET_ON_START, USER_INFO_QUERY, REDIS_HOST, REDIS_PORT, \
    REDIS_DID_NAME
from KuaiShou.items import KuaishouUserInfoIterm


class KuaishouUserInfoSpider(scrapy.Spider):
    name = 'kuaishou_user_info'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700
    }}
    allowed_domains = ['live.kuaishou.com/graphql']
    # start_urls = ['http://live.kuaishou.com/graphql/']
    # 连接redis
    conn = Redis(host=REDIS_HOST, port=REDIS_PORT)

    def start_requests(self):
        # 配置kafka连接信息
        client = KafkaClient(hosts=KAFKA_HOSTS)
        topic = client.topics[KAFKA_TOPIC]
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
                                     method='POST', callback=self.parse_user_info, meta={'bodyJson': user_info_query}
                                     )
            except Exception as e:
                logger.warning('Kafka message structure cannot be resolved :{}'.format(e))

    def parse_user_info(self, response):
        rsp_json = json.loads(response.text)
        user_info = rsp_json['data']['userInfo']
        if user_info == None:
            # 删掉did库中的失效did
            kuaishou_cookie_info = {}
            for cookie in response.headers.getlist('Set-Cookie'):
                cookie_str = cookie.decode().split(';')[0]
                key, value = cookie_str.split('=')
                kuaishou_cookie_info[key.replace('.', '_')] = value
            logger.info(response.headers.getlist('Set-Cookie'))
            logger.info('RedisDid srem invaild did:{}'.format(str(kuaishou_cookie_info)))
            # self.conn.srem(REDIS_DID_NAME,str(kuaishou_cookie_info))

            body_json = response.meta['bodyJson']
            principal_id = body_json['variables']['principalId']
            logger.warning('UserInfoQuery failed, principalId:{}'.format(principal_id))
            yield

        kuaishou_user_info_iterm = KuaishouUserInfoIterm()
        kuaishou_user_info_iterm['name'] = self.name
        kuaishou_user_info_iterm['user_info'] = user_info
        yield kuaishou_user_info_iterm
