# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

from KOL.utils.mysql import MysqlClient

from KOL.items import *



class KolPipeline(object):
    def process_item(self, item, spider):
        return item


class KuaiShouUserPipeline(object):

    def __init__(self):
        self.mysqlClient = MysqlClient(host='10.8.26.106', user='scrapy', password='Scrapy_123', database='test_kuaishou')
        #self.mysqlClient = MysqlClient(host='10.8.26.23', user='hive', password='Hive_123', database='test_kuaishou')



    def process_item(self, item, spider):
        if 'kwaiId' in item:
            self.mysqlClient.insertOneUserInfoRecord(item)
        if 'authorId' in item:
            self.mysqlClient.insertOneCommentUserInfoRecord(item)
        return item

    def close_spider(self, spider):
        self.mysqlClient.close()

