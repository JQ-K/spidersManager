# -*- coding: utf-8 -*-

import pymysql
import configparser
import os

class MysqlClient(object):

    def __init__(self, host, user, password, database):
        self.conn = pymysql.connect(host=host, user=user, password=password, database=database)


    @classmethod
    def from_settings(cls, conf_dir):
        conf_path = os.path.join(conf_dir, 'dbconf.ini')
        conf = configparser.ConfigParser()
        conf.read(conf_path)
        host = conf.get('mysql', 'host')
        user = conf.get('mysql', 'user')
        password = conf.get('mysql', 'password')
        database = conf.get('mysql', 'database')
        return cls(host, user, password, database)


    def insertOneUserInfoRecord(self, tableName, userDict):
        pass


    def close(self):
        try:
            self.conn.close()
        except:
            print('close connection error')
