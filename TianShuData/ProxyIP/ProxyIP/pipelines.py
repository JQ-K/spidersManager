# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from redis import Redis
from ProxyIP.settings import REDIS_PORT,REDIS_HOST,REDIS_DID_NAME



class ProxyipPipeline(object):

    def open_spider(self, spider):
        self.conn = Redis(host=REDIS_HOST, port=REDIS_PORT)
        spider.logger.info('RedisConn:host = %s,port = %s' % (REDIS_HOST, REDIS_PORT))

    def process_item(self, item, spider):
        msg = str(item).replace('\n', '').encode('utf-8')
        spider.logger.info('Msg sadd redis[%s]: %s' % (REDIS_HOST, msg))
        # self.conn.sadd(REDIS_DID_NAME,msg)
        return item






