# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import json
import datetime
from loguru import logger
from scrapy.utils.project import get_project_settings
from pykafka import KafkaClient


class NewscheckPipeline(object):
    def __init__(self):
        self.today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        self.totalNum = 0

    def process_item(self, item, spider):
        item['crawl_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #print(item)
        isSuccess = self.writeItemToTxt(item)
        if not isSuccess:
            logger.info('write file failed: ' + str(item))
        else:
            logger.info('add one news')
            self.totalNum += 1
        return item

    def writeItemToTxt(self, item):
        settings = get_project_settings()
        try:
            f = open(settings.get('NEWS_INFO_ITEM_FILE_PATH') + '{}.txt'.format(self.today), "a+", encoding="utf-8")
            f.write(json.dumps(dict(item)) + '\n')
            f.close()
            return True
        except:
            return False

    def close_spider(self, spider):
        print('此次爬虫抓取统计结果:')
        print(self.totalNum)



class KuaishouKafkaPipeline(object):
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
        msg = bytes(json.dumps(dict(item)), encoding='utf-8')
        self.producer.produce(msg)
        spider.logger.info('Msg Produced kafka[%s]: %s' % (self.kafka_topic, msg))
        return item

    def close_spider(self, spider):
        self.producer.stop()
        spider.logger.info('kafka[%s] Producer stoped!' % (self.kafka_topic))

