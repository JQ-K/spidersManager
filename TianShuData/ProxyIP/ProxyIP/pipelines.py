# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from redis import Redis
from scrapy.utils.project import get_project_settings


class ProxyipPipeline(object):

    def open_spider(self, spider):
        settings = get_project_settings()
        self.redis_host = settings.get('REDIS_HOST')
        self.redis_port = settings.get('REDIS_PORT')
        self.redis_proxyip_basename = settings.get('REDIS_PROXYIP_BASENAME')
        self.conn = Redis(host=self.redis_host, port=self.redis_port)
        spider.logger.info('RedisConn:host = %s,port = %s' % (self.redis_host, self.redis_port))

    def process_item(self, item, spider):
        redis_name = '{}_{}'.format(self.redis_proxyip_basename, item['url_name'])
        for proxyip in item['proxyip_list']:
            msg = str(proxyip)
            spider.logger.info('Msg sadd redis[%s]: %s' % (redis_name, msg))
            self.conn.sadd(redis_name, msg)
        return item
