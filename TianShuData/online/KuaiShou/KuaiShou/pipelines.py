# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime, time

from pykafka import KafkaClient
from redis import Redis
from scrapy.utils.project import get_project_settings

from KuaiShou.utils.mysql import MySQLClient
from KuaiShou.utils.spiderplan import SeedsFansPlan


class KuaishouKafkaPipeline(object):

    # def __init__(self):
    def open_spider(self, spider):
        settings = get_project_settings()
        self.kafka_hosts = settings.get('KAFKA_HOSTS')
        self.kafka_topic = settings.get('KAFKA_ONLINE_DAILY_TOPIC')
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
        item['spider_datetime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
        cookie = item['Cookie']
        spider.logger.info('Msg sadd redis[%s]: %s' % (self.redis_host, cookie))
        self.conn.zadd(self.redis_did_name, {cookie:int(time.time())})
        return item


class KuaishouUserSeedsMySQLPipeline(object):

    def open_spider(self, spider):
        settings = get_project_settings()
        self.mysql_host = settings.get('MYSQL_HOST')
        self.mysql_user = settings.get('MYSQL_USER')
        self.mysql_password = settings.get('MYSQL_PASSWORD')
        self.mysql_database = settings.get('MYSQL_DATABASE')
        self.mysql_kuaishou_user_seeds_tablename = settings.get('MYSQL_KUAISHOU_USER_SEEDS_TABLENAME')
        spider.logger.info(
            'MySQLConn:host = %s,user = %s,db = %s' % (self.mysql_host, self.mysql_user, self.mysql_database))
        self.mysql_client = MySQLClient(host=self.mysql_host, user=self.mysql_user, password=self.mysql_password,
                                        dbname=self.mysql_database)

    def process_item(self, item, spider):
        msg = {}
        msg['userId'] = item['userId']
        msg['kwaiId'] = item['kwaiId']
        if msg['kwaiId'] == '':
            msg['kwaiId'] = item['user_id']
        msg['principalId'] = item['kwaiId']
        if 'principalId' in list(item.keys()):
            msg['principalId'] = item['principalId']
        msg['status'] = 1
        # 粉丝数为False，即更新种子库 principalId，更新后我们按照100W的粉丝数给其初始化下次抓取时间
        msg['next_scheduling_date'] = SeedsFansPlan(item['fan'])
        msg['pre_scheduling_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
        select_res = self.mysql_client.select(self.mysql_kuaishou_user_seeds_tablename, {"userId": msg['userId']})
        if select_res == 0:
            self.mysql_client.insert(self.mysql_kuaishou_user_seeds_tablename,msg)
            self.mysql_client.commit()
            spider.logger.info('Msg insert mysql[%s] table[%s]: %s' % (self.mysql_host, self.mysql_kuaishou_user_seeds_tablename, str(msg)))
            return item
        self.mysql_client.update(self.mysql_kuaishou_user_seeds_tablename,msg, {"userId": msg['userId']})
        self.mysql_client.commit()
        spider.logger.info('Msg update mysql[%s] table[%s]: %s' % (self.mysql_host, self.mysql_kuaishou_user_seeds_tablename, str(msg)))
        return item

    def close_spider(self, spider):
        self.mysql_client.close()
        spider.logger.info('Mysql[%s] Conn closed!' % (self.mysql_host))


class KuaishouScrapyLogsPipeline(object):

    def open_spider(self, spider):
        settings = get_project_settings()
        self.mysql_host = settings.get('MYSQL_HOST')
        self.mysql_user = settings.get('MYSQL_USER')
        self.mysql_password = settings.get('MYSQL_PASSWORD')
        self.mysql_database = settings.get('MYSQL_DATABASE')
        self.mysql_kuaishou_scrapy_logs_tablename = settings.get('MYSQL_KUAISHOU_SCRAPY_LOGS_TABLENAME')
        spider.logger.info(
            'MySQLConn:host = %s,user = %s,db = %s' % (self.mysql_host, self.mysql_user, self.mysql_database))
        self.mysql_client = MySQLClient(host=self.mysql_host, user=self.mysql_user, password=self.mysql_password,
                                        dbname=self.mysql_database)

    def process_item(self, item, spider):
        msg = {}
        if 'userId' in list(item.keys()):
            msg['item_id'] = item['userId']
        elif 'principalId' in list(item.keys()):
            msg['item_id'] = item['principalId']
        msg['item_type'] = item['spider_name']
        msg['is_successed'] = item['is_successed']
        msg['scrapy_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.mysql_client.insert(self.mysql_kuaishou_scrapy_logs_tablename,msg)
        self.mysql_client.commit()
        spider.logger.info('Msg insert mysql[%s] table[%s]: %s' % (self.mysql_host, self.mysql_kuaishou_scrapy_logs_tablename, str(msg)))
        return item

    def close_spider(self, spider):
        self.mysql_client.close()
        spider.logger.info('Mysql[%s] Conn closed!' % (self.mysql_host))