# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pykafka import KafkaClient
from redis import Redis
from scrapy.utils.project import get_project_settings

class KuaishouKafkaPipeline(object):

    # def __init__(self):
    def open_spider(self, spider):
        settings = get_project_settings()
        self.kafka_hosts = settings.get('KAFKA_HOSTS')
        self.kafka_topic = settings.get('KAFKA_TOPIC')
        client = KafkaClient(hosts=self.kafka_hosts)
        topic = client.topics[self.kafka_topic]
        self.producer = topic.get_producer()
        self.producer.start()
        spider.logger.info('KafkaClient:hosts = %s,topic = %s' % (self.kafka_hosts, self.kafka_topic))

    def process_item(self, item, spider):
        # 不同的蜘蛛使用不同的管道，也可以选用如下方法：
        # if spider.name != 'kuxuan_kol_user':
        #     return item
        # if item['name'] != 'kuaishou':
        #     return item
        msg = str(item).replace('\n', '').encode('utf-8')
        self.producer.produce(msg)
        spider.logger.info('Msg Produced kafka[%s]: %s' % (self.kafka_topic, msg))
        return item

    def close_spider(self, spider):
        self.producer.stop()
        spider.logger.info('kafka[%s] Producer stoped!' % (self.kafka_topic))


class KuaishouRedisPipeline(object):

    def open_spider(self, spider):
        settings = get_project_settings()
        self.redis_host = settings.get('REDIS_HOST')
        self.redis_port = settings.get('REDIS_PORT')
        self.redis_did_expire_time = settings.get('REDIS_DID_EXPIRE_TIME')
        self.redis_did_name = settings.get('REDIS_DID_NAME')
        self.conn = Redis(host=self.redis_host, port=self.redis_port)
        spider.logger.info('RedisConn:host = %s,port = %s' % (self.redis_host, self.redis_port))

    def process_item(self, item, spider):
        msg = str(item).replace('\n', '').encode('utf-8')
        spider.logger.info('Msg sadd redis[%s]: %s' % (self.REDIS_HOST, msg))
        self.conn.sadd(self.redis_did_name,msg)
        self.conn.expire(self.redis_did_name,self.redis_did_expire_time)
        return item
