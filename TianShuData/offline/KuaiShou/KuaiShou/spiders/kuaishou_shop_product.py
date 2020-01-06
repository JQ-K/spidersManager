# -*- coding: utf-8 -*-
import scrapy
import json

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouShopProductItem

class KuaishouShopProductSpider(scrapy.Spider):
    name = 'kuaishou_shop_product'

    shopProductListUrl = "https://www.kwaishop.com/rest/app/grocery/product/self/midPage/list"

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
        consumer = topic.get_balanced_consumer(
            consumer_group='test',
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
                bodyDict = {
                    "listProductParam": {
                        "id": str(user_id),
                        "page": 1
                    }
                }
                yield scrapy.Request(self.shopProductListUrl, method='POST',
                                     headers={'Content-Type': 'application/json'},
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
            return
        else:
            if rltJson['itemSize'] == 0:
                return
        if beginFlag:
            totalPage = rltJson['pageNum']
            beginFlag = False

        if 'products' not in rltJson:
            return

        products = rltJson['products']
        for product in products:
            productItem = KuaishouShopProductItem()
            productItem['spider_name'] = self.name
            productItem['userId'] = userId
            productItem['productId'] = product['itemId']
            productItem['productInfo'] = product
            yield productItem

        curPage += 1
        if curPage <= totalPage:
            bodyDict['listProductParam']['page'] = curPage
            yield scrapy.Request(self.shopProductListUrl, method='POST',
                                 headers={'Content-Type': 'application/json'},
                                 body=json.dumps(bodyDict), callback=self.parse_shop_product,
                                 meta={'userId': userId, 'bodyDict': bodyDict, 'beginFlag': beginFlag, 'curPage': curPage, 'totalPage': totalPage})
