__author__ = 'zlx'
# -*- coding: utf-8 -*-

import pymysql
import configparser
import os
import datetime
import json
from pykafka import KafkaClient
from loguru import logger

def bizsToKafka(client,kafka_topic,biz_list):
    #根据按键精灵的点击顺序，对biz_list进行排序，这样可以保证先打开的微信公众号先发送给kafka进行处理
    topics = client.topics
    # # print(topics)
    topic = topics[kafka_topic]
    logger.info(topic)
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




# if __name__ == '__main__':
#     # biz_sendTo_kafka = dataSendToKafka(host='127.0.0.1', user='root', password='root_123', database='weChat')
#     biz_sendTo_kafka = dataSendToKafka()
#     biz_list=biz_sendTo_kafka.getAllAccountFromMySQL('biz')
#     logger.info('biz_list:{}'.format(''.join(biz_list)))
#     biz_sendTo_kafka.bizsToKafka(biz_list)
#     biz_sendTo_kafka.close()

