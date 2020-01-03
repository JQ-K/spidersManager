# -*- coding: utf-8 -*-
import scrapy
import json

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouShopInfoIterm


class KuaishouShopInfoSpider(scrapy.Spider):
    name = 'kuaishou_shop_info'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700
    }}
    settings = get_project_settings()

    def start_requests(self):
        # 配置kafka连接信息
        kafka_hosts = self.settings.get('KAFKA_HOSTS')
        kafka_topic = self.settings.get('KAFKA_TOPIC')
        reset_offset_on_start = self.settings.get('RESET_OFFSET_ON_START')
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
                if msg_value_dict['name'] != 'kuanshou_kol_seeds':
                    continue
                user_id = msg_value_dict['userId']
                shopScoreUrl = "https://www.kwaishop.com/rest/app/grocery/ks/shop/score?sellerId={}"
                yield scrapy.Request(shopScoreUrl.format(user_id), method='GET', callback=self.parse_shop)
            except Exception as e:
                logger.warning('Kafka message structure cannot be resolved :{}'.format(e))


    def parse_shop(self, response):
        rsp_json = json.loads(response.text)

