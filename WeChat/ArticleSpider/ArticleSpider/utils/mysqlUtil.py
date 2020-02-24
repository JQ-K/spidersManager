__author__ = 'zlx'
# -*- coding: utf-8 -*-

import pymysql
import configparser
import os
import datetime
import json

from loguru import logger
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class mysqlInfo(object):


    # def __init__(self, host='127.0.0.1', user='root', password='root_123', database='weChat'):
    #初始化mysql 和kafka
    def __init__(self):

        self.mysql_host = settings.get('MYSQL_HOST')
        self.mysql_user = settings.get('MYSQL_USER')
        self.mysql_password = settings.get('MYSQL_PASSWORD')
        self.mysql_database = settings.get('MYSQL_DATABASE_WECHAT')
        self.table_name=settings.get('MYSQL_WECHAT_ACCOUNT_INFO_TABLENAME')
        logger.info(
            'MySQLConn:host = %s,user = %s,db = %s' % (self.mysql_host, self.mysql_user, self.mysql_database))
        self.conn = pymysql.connect(host=self.mysql_host, user=self.mysql_user, password=self.mysql_password,
                                        database=self.mysql_database, port=3306, charset="utf8")



    #从数据库中找出biz，并把biz传送给kafka
    def getAllAccountFromMySQL(self,col):
        bizList=[]
        sql="select {} from {}".format(col,self.table_name)
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                # print("row")
                # print(row)
                curId = row[0]
                # click_rank=row[1]
                bizList.append(curId)
        except Exception as e:
            bizList = []
            raise e
        cursor.close()

        return bizList


    def close(self):
        try:
            self.conn.close()
        except:
            print('close connection error')


if __name__ == '__main__':

    mysql_info = mysqlInfo()
    biz_list=mysql_info.getAllAccountFromMySQL('biz')
    # #对biz_list进行排序
    print(biz_list)
    # logger.info('biz_list:{}'.format(''.join(biz_list)))
    mysql_info.close()
