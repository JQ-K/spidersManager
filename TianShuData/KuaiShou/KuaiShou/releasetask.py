#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'


import datetime,re, time
from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger
from pykafka import KafkaClient
from scrapy.utils.project import get_project_settings

from KuaiShou.utils.mysql import MySQLClient



def MySQLSeedsSendKafka():
    settings = get_project_settings()
    mysql_host = settings.get('MYSQL_HOST')
    mysql_user = settings.get('MYSQL_USER')
    mysql_password = settings.get('MYSQL_PASSWORD')
    mysql_database = settings.get('MYSQL_DATABASE')
    mysql_kuaishou_user_seeds_tablename = settings.get('MYSQL_KUAISHOU_USER_SEEDS_TABLENAME')
    logger.info(
        'MySQLConn:host = %s,user = %s,db = %s' % (mysql_host, mysql_user, mysql_database))
    mysql_client = MySQLClient(host=mysql_host, user=mysql_user, password=mysql_password,
                                    dbname=mysql_database)
    kafka_hosts = settings.get('KAFKA_HOSTS')
    kafka_topic = settings.get('KAFKA_TOPIC')
    client = KafkaClient(hosts=kafka_hosts)
    topic = client.topics[kafka_topic]
    producer = topic.get_producer()
    producer.start()
    logger.info('KafkaClient:hosts = %s,topic = %s' % (kafka_hosts, kafka_topic))
    now_time = datetime.datetime.now().strftime('%Y%m%d')
    res = mysql_client.select(mysql_kuaishou_user_seeds_tablename,{'next_scheduling_date':'20191217','status':1})
    if res == 0:
        return
    for user_id,kuai_id,principal_id,_,_,_,_,_ in mysql_client.cur.fetchall()[:100]:
        # 间隔时间
        time.sleep(3)
        if (kuai_id == '' or re.findall('([a-z]+)',kuai_id) == []) and principal_id == '':
            kafka_msg_search = str({'name': 'kuanshou_seeds_search', 'userId': user_id, 'kwaiId': kuai_id}).encode('utf-8')
            producer.produce(kafka_msg_search)
            logger.info('UserId: %s ,KuaiKd: %s, Missing information of principal_id' % (user_id, kuai_id))
            logger.info('Msg Produced kafka[%s]: %s' % (kafka_topic, kafka_msg_search))
            continue
        if kuai_id == '':
            kuai_id = principal_id
        if principal_id == '':
            principal_id = kuai_id
        kafka_msg_seeds = str({'name':'kuanshou_kol_seeds', 'userId':user_id, 'kwaiId':kuai_id, 'principalId': principal_id}).encode('utf-8')
        producer.produce(kafka_msg_seeds)
        logger.info('Msg Produced kafka[%s]: %s' % (kafka_topic, kafka_msg_seeds))
    producer.stop()
    mysql_client.close()



if __name__ == '__main__':
    # sched = BlockingScheduler()
    # # 每24小时触发
    # sched.add_job(MySQLSeedsSendKafka, 'interval', hours=24, jitter=120)
    # sched.start()
    MySQLSeedsSendKafka()