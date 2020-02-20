# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouShopProductItem

#抓取商品列表要慢，非常容易返回：操作过于频繁，请稍后再试
class KuaishouShopProductSpider(scrapy.Spider):
    name = 'kuaishou_shop_product_list'

    shopProductListUrl = "https://www.kwaishop.com/rest/app/grocery/product/self/midPage/list"
    # referer参数：user_id
    referer = "https://www.kwaishop.com/merchant/shop/list?id={}&webviewClose=false&biz=merchant&carrierType=3&from=profile&hyId=kwaishop"

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'Referer': ''
    }

    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700,
        'KuaiShou.pipelines.KuaishouScrapyLogsPipeline': 701
    }}
    settings = get_project_settings()


    def __init__(self, partitionIdx='0', useProxy='0', *args, **kwargs):
        super(KuaishouShopProductSpider, self).__init__(*args, **kwargs)
        self.partitionIdx = int(partitionIdx)
        self.useProxy = int(useProxy)


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
                msg_value_dict = json.loads(msg_value)
                if msg_value_dict['spider_name'] != 'kuaishou_shop_score':
                    continue
                user_id = msg_value_dict['userId']
                logger.info('user_id: ' + str(user_id))
                bodyDict = {
                    "listProductParam": {
                        "id": str(user_id),
                        "page": 1
                    }
                }
                curHeaders = self.headers
                curHeaders['referer'] = self.referer.format(user_id)
                time.sleep(random.choice(range(50, 100)))
                yield scrapy.Request(self.shopProductListUrl, method='POST',
                                     headers=curHeaders,
                                     body=json.dumps(bodyDict), callback=self.parse_shop_product,
                                     meta={'userId': user_id, 'bodyDict': bodyDict, 'beginFlag': True, 'curPage': 1, 'totalPage': 1})
            except Exception as e:
                logger.warning('Kafka message structure cannot be resolved :{}'.format(e))


    def parse_shop_product(self, response):
        rltJson = json.loads(response.text)
        userId = response.meta['userId']
        bodyDict = response.meta['bodyDict']
        beginFlag = response.meta['beginFlag']
        curPage = response.meta['curPage']
        totalPage = response.meta['totalPage']
        if rltJson['result'] != 1:
            print('get interface error: ' + response.text)
            return
        if 'itemSize' not in rltJson:
            logger.info('itemSize not in response json, user_id: ' + str(userId))
            return
        else:
            if rltJson['itemSize'] == 0:
                logger.info('itemSize == 0, user_id: ' + str(userId))
                return
        if beginFlag:
            totalPage = rltJson['pageNum']
            beginFlag = False

        if 'products' not in rltJson:
            logger.info('products not in response json, user_id: ' + str(userId))
            return

        products = rltJson['products']
        for product in products:
            productItem = KuaishouShopProductItem()
            productItem['spider_name'] = self.name
            productItem['userId'] = userId
            productItem['productId'] = product['itemId']
            productItem['productInfo'] = product
            #print(productItem)
            logger.info('get shopList, user_id: ' + str(userId))
            yield productItem

        curPage += 1
        if curPage <= totalPage:
            bodyDict['listProductParam']['page'] = curPage
            curHeaders = self.headers
            curHeaders['referer'] = self.referer.format(userId)
            time.sleep(random.choice(range(50, 100)))
            yield scrapy.Request(self.shopProductListUrl, method='POST',
                                 headers=curHeaders,
                                 body=json.dumps(bodyDict), callback=self.parse_shop_product,
                                 meta={'userId': userId, 'bodyDict': bodyDict, 'beginFlag': beginFlag, 'curPage': curPage, 'totalPage': totalPage})
