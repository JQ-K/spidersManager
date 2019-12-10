# -*- coding: utf-8 -*-

import pymysql
import configparser
import os

class MysqlClient(object):

    def __init__(self, host, user, password, database):
        self.conn = pymysql.connect(host=host, user=user, password=password, database=database)
        #print('success')

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


    def insertOneInfoRecord(self, Item):
        #print('insert beginning...')
        if 'user_id' in Item:
            sql = "insert into user_info " \
              "(user_id, nick_name,pic_url,update_time) " \
              "values ({}, '{}', '{}', {}) " \
                .format(int(Item['user_id']),
                    Item['nick_name'],
                    Item['pic_url'],
                    int(Item['update_time']))
        elif  'article_id' in Item  :
            sql = "insert into article_info " \
              "(article_id, publish_time, title,article_imgurl, column_id, column_name, publisher_id,publisher_name,publisher_pic_url,update_time) " \
              "values ({}, {}, '{}', '{}', '{}', '{}', {},'{}','{}',{}) " \
                .format(int(Item['article_id']),
                        int(Item['publish_time']),
                        Item['title'],
                        Item['article_imgurl'],
                        Item['column_id'],
                        Item['column_name'],
                        int(Item['publisher_id']),
                        Item['publisher_name'],
                        Item['publisher_pic_url'],
                        int(Item['update_time']))
        elif 'shop_id' in Item:
            sql = "insert into shop_info " \
                  "(shop_id, publish_time, title,shop_imgurl, column_id, column_name,shop_max_price,shop_min_price,shop_sale_total, publisher_id,publisher_name,publisher_pic_url,update_time) " \
                  "values ({}, {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', {},'{}','{}',{}) " \
                    .format(int(Item['shop_id']),
                        int(Item['publish_time']),
                        Item['title'],
                        Item['shop_imgurl'],
                        Item['column_id'],
                        Item['column_name'],
                        Item['shop_max_price'],
                        Item['shop_min_price'],
                        Item['shop_sale_total'],
                        int(Item['publisher_id']),
                        Item['publisher_name'],
                        Item['publisher_pic_url'],
                        int(Item['update_time']))
        else:
            sql = ""

        #print(sql)
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
