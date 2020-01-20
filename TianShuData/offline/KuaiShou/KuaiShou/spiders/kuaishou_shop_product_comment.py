# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random
import redis

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
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700,
        'KuaiShou.pipelines.KuaishouScrapyLogsPipeline': 701
    }}
    settings = get_project_settings()


    def __init__(self, partitionIdx='0', useProxy='0', cookieManual='1', cookieIdx='0', *args, **kwargs):
        super(KuaishouShopProductCommentSpider, self).__init__(*args, **kwargs)
        self.partitionIdx = int(partitionIdx)
        self.useProxy = int(useProxy)
        self.cookieManual = int(cookieManual)
        self.cookieIdx = int(cookieIdx)

        # self.redis_host = self.settings.get('REDIS_HOST')
        # self.redis_port = self.settings.get('REDIS_PORT')
        # self.red = redis.Redis(host=self.redis_host, port=self.redis_port)


    # def getCookie(self, cookieIdx):
    #     tempCookie = self.red.hgetall('kuaishou_app_cookie_{}'.format(cookieIdx))
    #     rltCookie = {}
    #     for key, val in tempCookie.items():
    #         rltCookie[str(key, encoding="utf-8")] = str(val, encoding="utf-8")
    #     print({'token': rltCookie['token']})
    #     return {'token': rltCookie['token']}


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
                #msg_value_dict = eval(msg_value)
                msg_value_dict = json.loads(msg_value)
                if msg_value_dict['spider_name'] != 'kuaishou_shop_product_list':
                    continue
                productId = msg_value_dict['productId']
                logger.info('product_id: ' + str(productId))
                pcursor = ''
                offset = 0
                curHeader = self.headers
                curHeader['Referer'] = self.referer.format(productId)
                time.sleep(random.choice(range(12, 20)))
                yield scrapy.Request(self.productCommentUrl.format(productId, pcursor, offset),
                                     method='GET', callback=self.parse_product_comment, headers=curHeader,
                                     #cookies=self.getCookie(self.cookieIdx),
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
                    logger.info('add one comment record, product_id: ' + str(productId))
                    yield commentItem

        if 'pcursor' not in rltJson:
            return
        pcursor = rltJson['pcursor']
        if pcursor == 'no_more':
            return
        offset += self.pageCount
        curHeader = self.headers
        curHeader['Referer'] = self.referer.format(productId)
        time.sleep(random.choice(range(6, 10)))
        yield scrapy.Request(self.productCommentUrl.format(productId, pcursor, offset),
                             method='GET', callback=self.parse_product_comment, headers=curHeader,
                             #cookies=self.getCookie(self.cookieIdx),
                             meta={'productId': productId, 'offset': offset})


    # def close(self):
    #     self.red.close()
