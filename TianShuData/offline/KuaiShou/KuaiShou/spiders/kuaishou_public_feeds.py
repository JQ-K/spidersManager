# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouUserPhotoInfoIterm


class KuaishouUserPhotoSpider(scrapy.Spider):
    name = 'kuaishou_public_feeds'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700,
        'KuaiShou.pipelines.KuaishouScrapyLogsPipeline': 701
    }}
    settings = get_project_settings()


    def __init__(self, partitionIdx='0', useProxy='0', cookieManual='0', cookieIdx='0', *args, **kwargs):
        super(KuaishouUserPhotoSpider, self).__init__(*args, **kwargs)
        self.partitionIdx = int(partitionIdx)
        self.useProxy = int(useProxy)
        self.cookieManual = int(cookieManual)
        self.cookieIdx = int(cookieIdx)


    def start_requests(self):
        # 配置kafka连接信息
        # kafka_hosts = self.settings.get('KAFKA_HOSTS')
        # kafka_topic = self.settings.get('KAFKA_TOPIC')
        # self.public_feeds_query = self.settings.get('PUBLIC_FEEDS_QUERY')
        # client = KafkaClient(hosts=kafka_hosts)
        # topic = client.topics[kafka_topic]
        # # 配置kafka消费信息
        # consumer = topic.get_balanced_consumer(
        #     consumer_group=self.name,
        #     managed=True,
        #     auto_commit_enable=True
        # )

        # 配置kafka连接信息
        kafka_hosts = self.settings.get('KAFKA_HOSTS')
        zookeeper_hosts = self.settings.get('ZOOKEEPER_HOSTS')
        kafka_topic = self.settings.get('KAFKA_TOPIC')
        reset_offset_on_start = self.settings.get('RESET_OFFSET_ON_START')
        logger.info('kafka info, hosts:{}, topic:{}'.format(kafka_hosts, kafka_topic) + '\n')
        self.public_feeds_query = self.settings.get('PUBLIC_FEEDS_QUERY')
        client = KafkaClient(hosts=kafka_hosts, zookeeper_hosts=zookeeper_hosts, broker_version='0.10.1.0')
        topic = client.topics[kafka_topic]
        partitions = topic.partitions
        # 配置kafka消费信息
        consumer = topic.get_simple_consumer(
            consumer_group=self.name,
            reset_offset_on_start=reset_offset_on_start,
            auto_commit_enable=True,
            partitions=[partitions[self.partitionIdx]]
        )
        # self.kuaikan_url = 'https://live.kuaishou.com/graphql'
        self.kuaikan_url = 'https://live.kuaishou.com/m_graphql'
        self.headers = {'content-type': 'application/json'}

        # 获取被消费数据的偏移量和消费内容
        for message in consumer:
            try:
                if message is None:
                    continue
                # 信息分为message.offset, message.value
                msg_value = message.value.decode()
                msg_value_dict = eval(msg_value)
                # if msg_value_dict['spider_name'] != 'kuanshou_kol_seeds':
                if msg_value_dict['spider_name'] != 'kuaishou_user_seeds':
                    continue
                principal_id = msg_value_dict['principalId']
                if principal_id is None or len(principal_id) < 1:
                    logger.info('principal_id is empty: ' + str(principal_id))
                    continue
                logger.info('principal_id: ' + str(principal_id))
                curQuery = self.public_feeds_query
                curQuery['variables']['principalId'] = principal_id
                time.sleep(random.choice(range(10, 20)))
                yield scrapy.Request(self.kuaikan_url, headers=self.headers, body=json.dumps(curQuery),
                                     method='POST', callback=self.parse_user_photo,
                                     meta={'principalId': principal_id}
                                     )
            except Exception as e:
                logger.warning('Kafka message structure cannot be resolved :{}'.format(e))


    def parse_user_photo(self, response):
        rsp_json = json.loads(response.text)
        principalId = response.meta['principalId']

        if 'data' not in rsp_json:
            logger.info('data not in response, principalId: ' + str(principalId))
            return

        if 'publicFeeds' not in rsp_json['data']:
            logger.info('publicFeeds not in response data, principalId: ' + str(principalId))
            return

        public_feeds = rsp_json['data']['publicFeeds']

        if public_feeds is None:
            logger.info('public_feeds is None: ' + str(principalId))
            return

        if 'list' not in public_feeds:
            logger.info('list not in public_feeds, principalId: ' + str(principalId))
            return

        if public_feeds['list'] == []:
            # 删掉did库中的失效did
            # ...待开发
            # body_json = response.meta['bodyJson']
            # principal_id = body_json['variables']['principalId']
            # logger.warning('UserPhotoQuery failed, principalId:{}'.format(principal_id))
            logger.info('response list = [], principalId: ' + str(principalId))
            return
        for user_photo_info in public_feeds['list']:
            kuaishou_user_photo_info_iterm = KuaishouUserPhotoInfoIterm()
            kuaishou_user_photo_info_iterm['spider_name'] = self.name
            kuaishou_user_photo_info_iterm['photo_id'] = user_photo_info['id']
            kuaishou_user_photo_info_iterm['user_photo_info'] = user_photo_info
            logger.info('get one photo record, photo_id: ' + str(user_photo_info['id']))
            yield kuaishou_user_photo_info_iterm
        pcursor = public_feeds['pcursor']
        if pcursor is None or pcursor == 'no_more':
            return

        time.sleep(random.choice(range(10, 20)))
        curQuery = self.public_feeds_query
        curQuery['variables']['principalId'] = principalId
        curQuery['variables']['pcursor'] = pcursor
        yield scrapy.Request(self.kuaikan_url, headers=self.headers, body=json.dumps(curQuery),
                             method='POST', callback=self.parse_user_photo,
                             meta={'principalId': principalId}
                             )
