# -*- coding: utf-8 -*-
import scrapy
import json
import time

from pykafka import KafkaClient
from loguru import logger
from redis import Redis
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouUserInfoIterm


class KuaishouUserInfoSpider(scrapy.Spider):
    name = 'kuaishou_sensitiv_user_info'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700
    }}
    settings = get_project_settings()
    # allowed_domains = ['live.kuaishou.com/graphql']
    # start_urls = ['http://live.kuaishou.com/graphql/']
    # 连接redis
    redis_host = settings.get('REDIS_HOST')
    redis_port = settings.get('REDIS_PORT')
    redis_did_name = settings.get('REDIS_DID_NAME')

    conn = Redis(host=redis_host, port=redis_port)

    def start_requests(self):
        # 配置kafka连接信息
        kafka_hosts = self.settings.get('KAFKA_HOSTS')
        kafka_topic = self.settings.get('KAFKA_TOPIC')
        sensitiv_user_info_query = self.settings.get('SENSITIVE_USER_INFO_QUERY')
        logger.info('kafka info, hosts:{}, topic:{}'.format(kafka_hosts, kafka_topic))
        client = KafkaClient(hosts=kafka_hosts)
        topic = client.topics[kafka_topic]
        # 配置kafka消费信息
        consumer = topic.get_balanced_consumer(
            consumer_group=self.name,
            managed=True,
            auto_commit_enable=True
        )
        kuaishou_url = 'https://live.kuaishou.com/graphql'
        headers = {'content-type': 'application/json'}
        # 获取被消费数据的偏移量和消费内容
        for message in consumer:
            try:
                if message is None:
                    continue
                # 信息分为message.offset, message.value
                msg_value = message.value.decode()
                msg_value_dict = eval(msg_value)
                logger.info(msg_value_dict)
                if msg_value_dict['spider_name'] != 'kuanshou_kol_seeds':
                    continue
                principal_id = msg_value_dict['principalId']
                sensitiv_user_info_query['variables']['principalId'] = principal_id
                logger.info('kafka message:{}'.format(msg_value))
                # logger.info(sensitiv_user_info_query)
                yield scrapy.Request(kuaishou_url, headers=headers, body=json.dumps(sensitiv_user_info_query),
                                     method='POST', callback=self.parse_user_info, meta={'bodyJson': sensitiv_user_info_query},
                                     dont_filter=True
                                     )
            except Exception as e:
                logger.warning('Kafka message structure cannot be resolved :{}'.format(str(e)))

    def parse_user_info(self, response):
        logger.info(response.text)
        rsp_json = json.loads(response.text)
        user_info = rsp_json['data']['sensitiveUserInfo']
        if user_info == None:
            logger.warning('SensitivUserInfoQuery failed, error:{}'.format(str(rsp_json).replace('\n', '')))
            yield
        if user_info['kwaiId'] == None:
            # 删掉did库中的失效did
            kuaishou_cookie_info = response.meta['didJson']
            logger.info('RedisDid srem invaild did:{}'.format(str(kuaishou_cookie_info)))
            self.conn.srem(self.redis_did_name, str(kuaishou_cookie_info).encode('utf-8'))
            body_json = response.meta['bodyJson']
            principal_id = body_json['variables']['principalId']
            logger.warning('SensitivUserInfoQuery failed, principalId:{}'.format(principal_id))
            yield
        kuaishou_user_info_iterm = KuaishouUserInfoIterm()
        kuaishou_user_info_iterm['spider_name'] = self.name
        kuaishou_user_info_iterm['userId'] = user_info['userId']
        kuaishou_user_info_iterm['kwaiId'] = user_info['kwaiId']
        kuaishou_user_info_iterm['principalId'] = response.meta['bodyJson']['variables']['principalId']
        kuaishou_user_info_iterm['constellation'] = user_info['constellation']
        kuaishou_user_info_iterm['cityName'] = user_info['cityName']
        kuaishou_user_info_iterm['fan'] = user_info['countsInfo']['fan']
        kuaishou_user_info_iterm['follow'] = user_info['countsInfo']['follow']
        kuaishou_user_info_iterm['photo'] = user_info['countsInfo']['photo']
        kuaishou_user_info_iterm['liked'] = user_info['countsInfo']['liked']
        kuaishou_user_info_iterm['open'] = user_info['countsInfo']['open']
        kuaishou_user_info_iterm['playback'] = user_info['countsInfo']['playback']
        yield kuaishou_user_info_iterm
