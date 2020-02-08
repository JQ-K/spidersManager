# -*- coding: utf-8 -*-

import jieba, os

from pykafka import KafkaClient
from scrapy.utils.project import get_project_settings
from loguru import logger
from lxml import etree

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class TianshuPipeline(object):
    def process_item(self, item, spider):
        return item


class TianShuKafkaPipeline(object):

    def open_spider(self, spider):
        settings = get_project_settings()
        self.kafka_hosts = settings.get('KAFKA_HOSTS')
        self.kafka_topic = settings.get('KAFKA_TOPIC_ARTICLE')
        client = KafkaClient(hosts=self.kafka_hosts)
        topic = client.topics[self.kafka_topic]
        self.producer = topic.get_producer()
        self.producer.start()
        spider.logger.info('KafkaClient:hosts = %s,topic = %s' % (self.kafka_hosts, self.kafka_topic))

    def process_item(self, item, spider):
        msg = str(item).replace('\n', '').encode('utf-8')
        self.producer.produce(msg)
        spider.logger.info('Msg Produced kafka[%s]: nickname: %s, title:%s' % (self.kafka_topic, item['fake_alias'], item['msg_title']))
        # return item
    def close_spider(self, spider):
        self.producer.stop()
        spider.logger.info('kafka[%s] Producer stoped!' % (self.kafka_topic))

class TianShuPiYaoKafkaPipeline(object):

    def open_spider(self, spider):
        settings = get_project_settings()
        self.kafka_hosts = settings.get('KAFKA_HOSTS')
        self.kafka_topic = settings.get('KAFKA_TOPIC_PIYAO_ARTICLE')
        client = KafkaClient(hosts=self.kafka_hosts)
        topic = client.topics[self.kafka_topic]
        self.producer = topic.get_producer()
        self.producer.start()
        dict_path = os.path.dirname(os.path.realpath(__file__)) + '/dict.txt'
        jieba.load_userdict(dict_path)
        self.key_words_list = [para[:-1] for para in open(dict_path, 'r', encoding='utf-8').readlines()]
        spider.logger.info('KafkaClient:hosts = %s,topic = %s' % (self.kafka_hosts, self.kafka_topic))

    def process_item(self, item, spider):
        content_html = etree.HTML(item['msg_content'])
        content_text ='\n'.join(content_html.xpath('//text()'))
        item['msg_text'] = content_text
        title = item['msg_title']
        fake_alias = item['fake_alias']
        word_list = list(jieba.cut(title)) + list(jieba.cut(content_text))
        tag_list = list(set(self.key_words_list) & set(word_list))
        if tag_list == []:
            logger.info('Not sasri,nickname: {}, title: {}'.format(fake_alias, title))
            return None
        msg = str(item).replace('\n', '').encode('utf-8')
        self.producer.produce(msg)
        spider.logger.info('Msg Produced kafka[%s]: nickname: %s, title:%s' % (self.kafka_topic, fake_alias, title))
        # return item
    def close_spider(self, spider):
        self.producer.stop()
        spider.logger.info('kafka[%s] Producer stoped!' % (self.kafka_topic))

