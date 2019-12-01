# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
from KOL.utils.mysqlUtil import MysqlClient


class KolPipeline(object):
    def process_item(self, item, spider):
        return item


class KuaiShouUserPipeline(object):

    def __init__(self):
        self.mysqlClient = MysqlClient(host='10.8.26.106', user='scrapy', password='Scrapy_123', database='test_kuaishou')
        #self.mysqlClient = MysqlClient(host='10.8.26.23', user='hive', password='Hive_123', database='test_kuaishou')



    def process_item(self, item, spider):
        #print(json.dumps(dict(item)))
        self.mysqlClient.insertOneUserInfoRecord(item)
        return item

    def close_spider(self, spider):
        self.mysqlClient.close()

