# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import time
import redis
from redis import Redis
from scrapy.utils.project import get_project_settings
from ArticleSpider.utils.mysql import MySQLClient
# from twisted.enterprise import adbapi
import pymysql


class WechatArticalPipeline(object):
    def open_spider(self, spider):
        settings = get_project_settings()
        self.mysql_host = settings.get('MYSQL_HOST')
        self.mysql_user = settings.get('MYSQL_USER')
        self.mysql_password = settings.get('MYSQL_PASSWORD')
        self.mysql_database = settings.get('MYSQL_DATABASE')
        self.mysql_wechat_artical_info_tablename=settings.get('MYSQL_WECHAT_ARTICAL_INFO_TABLENAME')

        spider.logger.info(
            'MySQLConn:host = %s,user = %s,db = %s' % (self.mysql_host, self.mysql_user, self.mysql_database))
        self.mysql_client = MySQLClient(host=self.mysql_host, user=self.mysql_user, password=self.mysql_password,
                                        dbname=self.mysql_database)

    def process_item(self, item, spider):
        #需要执行insert和update操作
        #查看有没有这个sn,biz
        select_res = self.mysql_client.select(self.mysql_wechat_artical_info_tablename, {"SN": item['SN'],"biz": item['biz']})
        if select_res == 0:
            self.mysql_client.insert(self.mysql_wechat_artical_info_tablename,item)
            self.mysql_client.commit()
            spider.logger.info('item insert mysql[%s]: %s' % (self.mysql_host, str(item)))
            return item
        self.mysql_client.update(self.mysql_wechat_artical_info_tablename,item, {"SN": item['SN'],"biz": item['biz']})

        return item

    def close_spider(self, spider):
        self.mysql_client.close()
        spider.logger.info('Mysql[%s] Conn closed!' % (self.mysql_host))





# class MysqlTwistedPipline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):
#         dbparms = dict(
#             host = settings["MYSQL_HOST"],
#             db = settings["MYSQL_DBNAME"],
#             user = settings["MYSQL_USER"],
#             passwd = settings["MYSQL_PASSWORD"],
#             charset='utf8',
#             # cursorclass=MySQLdb.cursors.DictCursor,
#             cursorclass=pymysql.cursors.DictCursor,  #将取回值以字典形式显示
#             use_unicode=True,
#         )
#         # dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
#         dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         #使用twisted将mysql插入变成异步执行
#         query = self.dbpool.runInteraction(self.do_insert, item)
#         query.addErrback(self.handle_error, item, spider) #处理异常
#
#     def handle_error(self, failure, item, spider):
#         #处理异步插入的异常
#         print (failure)
#
#     def do_insert(self, cursor, item):
#         #执行具体的插入
#         #根据不同的item 构建不同的sql语句并插入到mysql中
#         insert_sql, params = item.get_insert_sql()
#         cursor.execute(insert_sql, params)
#
