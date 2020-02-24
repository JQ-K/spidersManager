__author__ = 'zlx'
# -*- coding: utf-8 -*-

import pymysql
import configparser
import os
import datetime
import json
from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class dataSendToKafka(object):

    def __init__(self):
         # 配置kafka连接信息
        self.kafka_hosts = settings.get('KAFKA_HOSTS')
        self.zookeeper_hosts=settings.get('ZOOKEEPER_HOSTS')
        self.kafka_topic = settings.get('KAFKA_TOPIC_WECHAT')
        self.reset_offset_on_start = settings.get('RESET_OFFSET_ON_START')
        logger.info('reset_offset_on_start:%d,1表示true,0表示false' % self.reset_offset_on_start)
        logger.info('kafka info, hosts:{},zookeeper_hosts:{}, topic:{}'.format(self.kafka_hosts,self.zookeeper_hosts, self.kafka_topic))
        self.kafkaClient = KafkaClient(hosts=self.kafka_hosts,zookeeper_hosts=self.zookeeper_hosts, broker_version='0.10.1.0')



    def bizsToKafka(self,biz_list):
        #根据按键精灵的点击顺序，对biz_list进行排序，这样可以保证先打开的微信公众号先发送给kafka进行处理

        topics = self.kafkaClient.topics
        # print(topics)
        topic = topics[self.kafka_topic]
        print(topic)
        written_msgs = 0
        # one_biz_dict={}
        with topic.get_producer() as producer:
            for onebiz in biz_list:
                content='{"__biz":'+'"'+str(onebiz)+'"}'+'\n'
                # one_biz_dict["__biz"]=str(onebiz)
                producer.produce(bytes(content, encoding='utf-8'))
                written_msgs += 1
            if written_msgs  == 172:
              logger.info("written_msgs: %d" % written_msgs)
        logger.info("written_msgs: %d" % written_msgs)


    def close(self):
        try:
            self.conn.close()
        except:
            print('close connection error')


# if __name__ == '__main__':
#     # biz_sendTo_kafka = dataSendToKafka(host='127.0.0.1', user='root', password='root_123', database='weChat')
#     biz_sendTo_kafka = dataSendToKafka()
#     biz_list=biz_sendTo_kafka.getAllAccountFromMySQL('biz')
#     logger.info('biz_list:{}'.format(''.join(biz_list)))
#     biz_sendTo_kafka.bizsToKafka(biz_list)
#     biz_sendTo_kafka.close()

