# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random

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
    #headers = {'Connection': 'keep-alive'}
    headers = {
        'Referer': ''
    }
    # 参数：itemId
    referer = "https://www.kwaishop.com/merchant/shop/detail/comment?itemId={}"

    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700
    }}
    settings = get_project_settings()

    def getCookie(self):
        token = '58cc04a5b35d446c9d16e65e991214e7-1577168521'
        cookie = {
            'token': token
        }
        return cookie

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
                curHeader = self.headers
                curHeader['Referer'] = self.referer.format(productId)
                yield scrapy.Request(self.productCommentUrl.format(productId, pcursor, offset),
                                     method='GET', callback=self.parse_product_comment, headers=curHeader,
                                     cookies=self.getCookie(),
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
            comments = rltJson['comments']
            for comment in comments:
                if 'commentId' in comment:
                    commentItem = KuaishouShopProductCommentItem()
                    commentItem['spider_name'] = self.name
                    commentItem['productId'] = productId
                    commentItem['commentId'] = comment['commentId']
                    commentItem['productComment'] = comment
                    yield commentItem

        if 'pcursor' not in rltJson:
            return
        pcursor = rltJson['pcursor']
        if pcursor == 'no_more':
            return
        offset += self.pageCount
        curHeader = self.headers
        curHeader['Referer'] = self.referer.format(productId)
        time.sleep(random.choice(range(12,16)))
        yield scrapy.Request(self.productCommentUrl.format(productId, pcursor, offset),
                             method='GET', callback=self.parse_product_comment, headers=curHeader,
                             cookies=self.getCookie(),
                             meta={'productId': productId, 'offset': offset})
