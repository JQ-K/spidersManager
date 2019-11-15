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


    '''def getChannelIdList(self, tableName, channelName):
        sql = "select distinct channel_id from {} where channel_info_name='{}'".format(tableName, channelName)
        rltList = []
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                curId = row[0]
                rltList.append(curId)
        except Exception as e:
            rltList = []
            raise e
        cursor.close()
        return rltList'''


    def getChannelIdList(self, channelName):
        #sql = "select distinct channel_id from {} where channel_info_name='{}'".format(tableName, channelName)
        sql = "SELECT distinct channel_id FROM mcloud_channel c LEFT JOIN mcloud_channel_auth a ON c.id=a.channel_id WHERE c.type = (SELECT id FROM mcloud_channel_info WHERE NAME='{}') AND c.status!=-2 AND a.auth_name='{}账号'".format(channelName, channelName)
        rltList = []
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                curId = row[0]
                rltList.append(curId)
        except Exception as e:
            rltList = []
            raise e
        cursor.close()
        return rltList


    def getUserAndPwdByChannelId(self, tableName, channelId):
        sql = "select auth_value from {} where channel_id={} and auth_name like '%账号'".format(tableName, channelId)
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            userName = cursor.fetchone()[0]
        except:
            cursor.close()
            return None
        cursor.close()

        sql = "select auth_value from {} where channel_id={} and auth_name like '%密码'".format(tableName, channelId)
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            passWord = cursor.fetchone()[0]
        except:
            cursor.close()
            return None
        cursor.close()
        return (userName, passWord)


    def close(self):
        try:
            self.conn.close()
        except:
            print('close connection error')

