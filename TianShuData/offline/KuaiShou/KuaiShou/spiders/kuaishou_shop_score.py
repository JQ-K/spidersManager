# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouShopInfoIterm


class KuaishouShopInfoSpider(scrapy.Spider):
    name = 'kuaishou_shop_score'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700,
        'KuaiShou.pipelines.KuaishouScrapyLogsPipeline': 701
    }}
    settings = get_project_settings()


    def __init__(self, partitionIdx='0', useProxy='1', cookieManual='0', cookieIdx='0', *args, **kwargs):
        super(KuaishouShopInfoSpider, self).__init__(*args, **kwargs)
        self.partitionIdx = int(partitionIdx)
        self.useProxy = int(useProxy)
        self.cookieManual = int(cookieManual)
        self.cookieIdx = int(cookieIdx)


    def start_requests(self):
        # 配置kafka连接信息
        # kafka_hosts = self.settings.get('KAFKA_HOSTS')
        # kafka_topic = self.settings.get('KAFKA_TOPIC')
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

        # 获取被消费数据的偏移量和消费内容
        for message in consumer:
            try:
                if message is None:
                    continue
                # 信息分为message.offset, message.value
                msg_value = message.value.decode()
                msg_value_dict = eval(msg_value)
                # #富春云
                # if msg_value_dict['spider_name'] != 'kuaishou_kol_seeds':
                # #战旗beta
                if msg_value_dict['spider_name'] != 'kuaishou_user_seeds':
                    continue
                user_id = msg_value_dict['userId']
                logger.info('user_id: ' + str(user_id))
                shopScoreUrl = "https://www.kwaishop.com/rest/app/grocery/ks/shop/score?sellerId={}"
                time.sleep(random.choice(range(10, 20)))
                yield scrapy.Request(shopScoreUrl.format(user_id), method='GET',
                                     callback=self.parse_shop, meta={'userId': user_id})
            except Exception as e:
                logger.warning('Kafka message structure cannot be resolved :{}'.format(e))


    def parse_shop(self, response):
        rsp_json = json.loads(response.text)
        userId = response.meta['userId']
        if rsp_json['result'] != 1:
            logger.info('response json result != 1, user_id: ' + str(userId))
            return
        if rsp_json['userShopScoreView'] is None:
            logger.info('response json userShopScoreView is None, user_id: ' + str(userId))
            return
        shopInfo = KuaishouShopInfoIterm()
        shopInfo['spider_name'] = self.name
        shopInfo['userId'] = userId
        shopInfo['shopInfo'] = rsp_json
        logger.info('get shopInfo, user_id: ' + str(userId))
        #print(shopInfo)
        yield shopInfo


