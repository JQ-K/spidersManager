# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from OwhatLab.utils.mysqlUtil import MysqlClient


class OwhatLabPipeline(object):
    def process_item(self, item, spider):
        return item

class OwhatLabUserPipeline(object):

    def __init__(self):
        #self.mysqlClient = MysqlClient(host='10.8.26.106', user='scrapy', password='Scrapy_123', database='test_kuaishou')
        #self.mysqlClient = MysqlClient(host='10.8.26.23', user='hive', password='Hive_123', database='test_kuaishou')

        #self.mysqlClient = MysqlClient(host='127.0.0.1', user='root', password='',
        #database='test_owhatlab')
        self.mysqlClient = MysqlClient(host='10.8.26.23', user='hive', password='Hive_123',
                                        database='test_OwhatLab')
        #print('connect mysql  success!')


    #这个方法一般在爬虫程序中yield调用的时候被触发，其中一个参数item就是yield传过来的，可以在这里处理抓到的数据，比如说进一步格式化，数据保存等。
    def process_item(self, item, spider):
        #print(json.dumps(dict(item)))
        self.mysqlClient.insertOneInfoRecord(item)
        #print('insert  success!')
        return item

    #爬虫结束执行时触发，在这里可以进行文件关闭，数据库关闭等处理。
    def close_spider(self, spider):
        self.mysqlClient.close()


