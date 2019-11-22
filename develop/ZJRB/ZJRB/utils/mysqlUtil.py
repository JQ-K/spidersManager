# -*- coding: utf-8 -*-

import pymysql
import configparser
import os

class MysqlClient(object):

    def __init__(self, host, user, password, database):
        self.conn = pymysql.connect(host=host, user=user, password=password, database=database)


    def getUrlListByHost(self, host):
        sql = "select id, source_title, title, url from transmit_content where host = '{}' and content_type = '图文'".format(host)

        rltList = []
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                id = row[0]
                source_title = row[1]
                title = row[2]
                url = row[3]
                rltList.append((id, source_title, title, url))
        except Exception as e:
            rltList = []
            raise e
        cursor.close()
        return rltList

    def close(self):
        try:
            self.conn.close()
        except:
            print('close connection error')

