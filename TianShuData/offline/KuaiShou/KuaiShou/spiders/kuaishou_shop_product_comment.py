# -*- coding: utf-8 -*-
import scrapy
import json

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouShopProductCommentItem


#cookie中需要token
class KuaishouShopProductCommentSpider(scrapy.Spider):
    name = 'kuaishou_shop_product_comment'
    #参数：itemId、pcursor、offset
    pageCount = 20
    productCommentUrl = "https://www.kwaishop.com/rest/app/grocery/ks/comment/list?type=1&itemId={}&skuId=&tagId=0&pcursor={}&count=20&sourceType=99&limit=20&offset={}"
    headers = {'Connection': 'keep-alive'}
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
                if msg_value_dict['spider_name'] != 'kuaishou_shop_product_list':
                    continue
                productId = msg_value_dict['productId']
                pcursor = ''
                offset = 0
                yield scrapy.Request(self.productCommentUrl.format(productId, pcursor, offset),
                                     method='GET', callback=self.parse_product_comment, headers=self.headers,
                                     meta={'productId': productId, 'offset': offset})
            except Exception as e:
                logger.warning('Kafka message structure cannot be resolved :{}'.format(e))


    def parse_product_comment(self, response):
        rltJson = json.loads(response.text)
        productId = response.meta['productId']
        offset = response.meta['offset']
        if rltJson['result'] != 1:
            print('get interface error: ' + response.text)
            return
        if 'comments' in rltJson:
            commentItem = KuaishouShopProductCommentItem()
            commentItem['spider_name'] = self.name
            commentItem['productId'] = productId
            commentItem['productComment'] = rltJson['comments']
            yield commentItem

        if 'pcursor' not in rltJson:
            return
        pcursor = rltJson['pcursor']
        if pcursor == 'no_more':
            return
        offset += self.pageCount
        yield scrapy.Request(self.productCommentUrl.format(productId, pcursor, offset),
                             method='GET', callback=self.parse_product_comment, headers=self.headers,
                             meta={'productId': productId, 'offset': offset})
