# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pykafka import KafkaClient
from redis import Redis

from KuaiShou.settings import KAFKA_TOPIC, KAFKA_HOSTS, REDIS_HOST, REDIS_PORT, REDIS_DID_NAME


class KuaishouKafkaPipeline(object):

    # def __init__(self):
    def open_spider(self, spider):
        client = KafkaClient(hosts=KAFKA_HOSTS)
        topic = client.topics[KAFKA_TOPIC]
        self.producer = topic.get_producer()
        self.producer.start()
        spider.logger.info('KafkaClient:hosts = %s,topic = %s' % (KAFKA_HOSTS, KAFKA_TOPIC))

    def process_item(self, item, spider):
        # 不同的蜘蛛使用不同的管道，也可以选用如下方法：
        # if spider.name != 'kuxuan_kol_user':
        #     return item
        # if item['name'] != 'kuaishou':
        #     return item
        msg = str(item).replace('\n', '').encode('utf-8')
        self.producer.produce(msg)
        spider.logger.info('Msg Produced kafka[%s]: %s' % (KAFKA_TOPIC, msg))
        return item

    def close_spider(self, spider):
        self.producer.stop()
        spider.logger.info('kafka[%s] Producer stoped!' % (KAFKA_TOPIC))


class KuaishouRedisPipeline(object):

    def open_spider(self, spider):
        self.conn = Redis(host=REDIS_HOST, port=REDIS_PORT)
        spider.logger.info('RedisConn:host = %s,port = %s' % (REDIS_HOST, REDIS_PORT))

    def process_item(self, item, spider):
        msg = str(item).replace('\n', '').encode('utf-8')
        spider.logger.info('Msg sadd redis[%s]: %s' % (REDIS_HOST, msg))
        self.conn.sadd(REDIS_DID_NAME,msg)
        return item
