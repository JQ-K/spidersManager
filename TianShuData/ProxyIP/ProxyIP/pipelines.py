# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from redis import Redis
from ProxyIP.settings import REDIS_PORT,REDIS_HOST,REDIS_PROXYIP_BASENAME



class ProxyipPipeline(object):

    def open_spider(self, spider):
        self.conn = Redis(host=REDIS_HOST, port=REDIS_PORT)
        spider.logger.info('RedisConn:host = %s,port = %s' % (REDIS_HOST, REDIS_PORT))

    def process_item(self, item, spider):
        redis_name = '{}_{}'.format(REDIS_PROXYIP_BASENAME, item['url_name'])
        for proxyip in item['proxyip_list']:
            msg = str(proxyip)
            spider.logger.info('Msg sadd redis[%s]: %s' % (redis_name, msg))
            self.conn.sadd(redis_name,msg)
        return item






