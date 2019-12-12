# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json, sys
from pykafka import KafkaClient
from ProxyIP.ProxyIP.settings import HOSTS,TOPIC



class ProxyipPipeline(object):

    def __init__(self):
        client = KafkaClient(hosts=HOSTS)
        topic = client.topics[TOPIC]
        self.producer = topic.get_producer()
        self.producer.start()

    def process_item(self, item, spider):
        msg = json.dumps(str(item).replace('\n', '').replace(' ', '')).encode('utf-8')
        self.producer.produce(msg)
        return item


    def close_spider(self, spider):
        self.producer.stop()






