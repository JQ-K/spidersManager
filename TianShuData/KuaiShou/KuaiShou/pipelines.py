# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

from pykafka import KafkaClient

from KuaiShou.items import *
from KuaiShou.settings import HOSTS,TOPIC


class KuaishouPipeline(object):
    def process_item(self, item, spider):
        if item['name'] != 'kuaishou':
            return item
        return item

class KuxuanKolUserPipeline(object):

    def __init__(self):
        client = KafkaClient(hosts=HOSTS)
        topic = client.topics[TOPIC]
        self.producer = topic.get_producer()
        self.producer.start()

    def process_item(self, item, spider):
        if item['name'] != 'kuxuan_kol_user':
            return item
        msg = json.dumps(str(item).replace('\n', '')).encode('utf-8')
        self.producer.produce(msg)
        spider.logger.info('Msg Produced kafka[%s]: %s' % (TOPIC, msg))
        return item

    def close_spider(self, spider):
        self.producer.stop()
        spider.logger.info('kafka[%s] Producer stoped!' % (TOPIC))


