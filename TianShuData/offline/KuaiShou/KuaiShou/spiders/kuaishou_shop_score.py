# -*- coding: utf-8 -*-
import scrapy
import json

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouShopInfoIterm


class KuaishouShopInfoSpider(scrapy.Spider):
    name = 'kuaishou_shop_score'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700
    }}
    settings = get_project_settings()

    def start_requests(self):
        # 配置kafka连接信息
        kafka_hosts = self.settings.get('KAFKA_HOSTS')
        kafka_topic = self.settings.get('KAFKA_TOPIC')
        client = KafkaClient(hosts=kafka_hosts)
        topic = client.topics[kafka_topic]
        # 配置kafka消费信息
        consumer = topic.get_balanced_consumer(
            consumer_group=self.name,
            managed=True,
            auto_commit_enable=True
        )
        # 获取被消费数据的偏移量和消费内容
        for message in consumer:
            try:
                if message is None:
                    continue
                # 信息分为message.offset, message.value
                msg_value = message.value.decode()
                msg_value_dict = eval(msg_value)
                if msg_value_dict['spider_name'] != 'kuanshou_kol_seeds':
                    continue
                user_id = msg_value_dict['userId']
                shopScoreUrl = "https://www.kwaishop.com/rest/app/grocery/ks/shop/score?sellerId={}"
                yield scrapy.Request(shopScoreUrl.format(user_id), method='GET',
                                     callback=self.parse_shop, meta={'userId': user_id})
            except Exception as e:
                logger.warning('Kafka message structure cannot be resolved :{}'.format(e))


    def parse_shop(self, response):
        rsp_json = json.loads(response.text)
        userId = response.meta['userId']
        if rsp_json['result'] != 1:
            return
        if rsp_json['userShopScoreView'] is None:
            return
        shopInfo = KuaishouShopInfoIterm()
        shopInfo['spider_name'] = self.name
        shopInfo['userId'] = userId
        shopInfo['shopInfo'] = rsp_json
        yield shopInfo


