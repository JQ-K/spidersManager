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


    def insertOneUserInfoRecord(self, userItem):
        sql = "insert into user_info (kwaiId, user_id, userId, user_name, user_sex, user_text, head_url, cityName, constellation, fan, follow, liked, photo, update_time) " \
              "values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"\
            .format((str(userItem['kwaiId']), int(userItem['user_id']), str(userItem['userId']), userItem['user_name'], userItem['user_sex'], userItem['user_text'], userItem['head_url'], userItem['cityName'], userItem['constellation'], str(userItem['fan']), str(userItem['follow']), str(userItem['like']), str(userItem['photo']), userItem['update_time']))
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            raise e
        cursor.close()


    def close(self):
        try:
            self.conn.close()
        except:
            print('close connection error')
