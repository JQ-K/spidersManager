# -*- coding: utf-8 -*-
import scrapy
import json

from pykafka import KafkaClient
from loguru import logger
from redis import Redis
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouUserInfoIterm


class KuaishouUserInfoSpider(scrapy.Spider):
    name = 'kuaishou_user_info'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700
    }}
    settings = get_project_settings()
    # allowed_domains = ['live.kuaishou.com/graphql']
    # start_urls = ['http://live.kuaishou.com/graphql/']
    # 连接redis
    redis_host = settings.get('REDIS_HOST')
    redis_port = settings.get('REDIS_PORT')

    conn = Redis(host=redis_host, port=redis_port)

    def start_requests(self):
        # 配置kafka连接信息
        kafka_hosts = self.settings.get('KAFKA_HOSTS')
        kafka_topic = self.settings.get('KAFKA_TOPIC')
        reset_offset_on_start = self.settings.get('RESET_OFFSET_ON_START')
        # user_info_query = self.settings.get('SENSITIVE_USER_INFO_QUERY')
        user_info_query = self.settings.get('USER_INFO_QUERY')
        logger.info('kafka info, hosts:{}, topic:{}'.format(kafka_hosts, kafka_topic))
        client = KafkaClient(hosts=kafka_hosts)
        topic = client.topics[kafka_topic]
        # 配置kafka消费信息
        consumer = topic.get_simple_consumer(
            consumer_group=self.name,
            reset_offset_on_start=reset_offset_on_start
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
                user_info_query['variables']['principalId'] = kwai_id
                kuaikan_url = 'http://live.kuaishou.com/graphql'
                headers = {'content-type': 'application/json'}
                # logger.info('kafka message:{}'.format(msg_value))
                yield scrapy.Request(kuaikan_url, headers=headers, body=json.dumps(user_info_query),
                                     method='POST', callback=self.parse_user_info, meta={'bodyJson': user_info_query},
                                     dont_filter=True
                                     )
                # return
            except Exception as e:
                logger.warning('Kafka message structure cannot be resolved :{}'.format(e))

    def parse_user_info(self, response):
        rsp_json = json.loads(response.text)
        user_info = rsp_json['data']['userInfo']
        if user_info == None:
            logger.warning('UserInfoQuery failed, error:{}'.format(str(rsp_json).replace('\n', '')))
            return
        if user_info['id'] == None:
            # 删掉did库中的失效did
            kuaishou_cookie_info = {}
            for cookie in response.headers.getlist('Set-Cookie'):
                cookie_str = cookie.decode().split(';')[0]
                key, value = cookie_str.split('=')
                kuaishou_cookie_info[key.replace('.', '_')] = value
            logger.info(response.headers.getlist('Set-Cookie'))
            logger.info('RedisDid srem invaild did:{}'.format(str(kuaishou_cookie_info)))
            # redis_did_name = self.settings.get('REDIS_DID_NAME')
            # self.conn.srem(redis_did_name,str(kuaishou_cookie_info))
            body_json = response.meta['bodyJson']
            principal_id = body_json['variables']['principalId']
            logger.warning('UserInfoQuery failed, principalId:{}'.format(principal_id))
            return

        kuaishou_user_info_iterm = KuaishouUserInfoIterm()
        kuaishou_user_info_iterm['name'] = self.name
        kuaishou_user_info_iterm['user_info'] = user_info
        return kuaishou_user_info_iterm
