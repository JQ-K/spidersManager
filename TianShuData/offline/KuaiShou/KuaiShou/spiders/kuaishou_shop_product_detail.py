# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouShopProductDetailItem


#cookie中需要did
class KuaishouShopProductDetailSpider(scrapy.Spider):
    name = 'kuaishou_shop_product_detail'
    productDetailUrl = "https://www.kwaishop.com/rest/app/grocery/product/self/detail?itemId={}"

    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700
    }}
    settings = get_project_settings()


    def __init__(self, partitionIdx='0', useProxy='0', cookieManual='0', cookieIdx='0', *args, **kwargs):
        super(KuaishouShopProductDetailSpider, self).__init__(*args, **kwargs)
        self.partitionIdx = int(partitionIdx)
        self.useProxy = int(useProxy)
        self.cookieManual = int(cookieManual)
        self.cookieIdx = int(cookieIdx)


    def start_requests(self):
        # 配置kafka连接信息
        # kafka_hosts = self.settings.get('KAFKA_HOSTS')
        # kafka_topic = self.settings.get('KAFKA_TOPIC')
        # reset_offset_on_start = self.settings.get('RESET_OFFSET_ON_START')
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
        kafka_topic = self.settings.get('KAFKA_TOPIC_DATA')
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
                #msg_value_dicte) = eval(msg_value)
                msg_value_dict = json.loads(msg_value)
                if msg_value_dict['spider_name'] != 'kuaishou_shop_product_list':
                    continue
                productId = msg_value_dict['productId']
                logger.info('product_id: ' + str(productId))
                time.sleep(random.choice(range(15, 25)))
                header = {
                    'Referer': 'https://www.kwaishop.com/merchant/shop/detail?id={}'.format(productId)
                }
                yield scrapy.Request(self.productDetailUrl.format(productId), method='GET',
                                     callback=self.parse_product_detail, headers=header,
                                     meta={'productId': productId})
            except Exception as e:
                logger.warning('Kafka message structure cannot be resolved :{}'.format(e))


    def parse_product_detail(self, response):
        rsp_json = json.loads(response.text)
        productId = response.meta['productId']
        if rsp_json['result'] != 1:
            logger.info('response json result != 1, product_id: ' + str(productId))
            return
        if rsp_json['productDetail'] is None:
            logger.info('response json productDetail is None, product_id: ' + str(productId))
            return
        productDetail = KuaishouShopProductDetailItem()
        productDetail['spider_name'] = self.name
        productDetail['productId'] = productId
        productDetail['productDetail'] = rsp_json['productDetail']
        logger.info('get one record, product_id: ' + str(productId))
        yield productDetail




