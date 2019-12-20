# -*- coding: utf-8 -*-

import pymysql
import configparser
import os

class MysqlClient(object):

    def __init__(self, host, user, password, database):
        self.conn = pymysql.connect(host=host, user=user, password=password, database=database)

    @classmethod
    def from_settings(cls, conf_dir, session_name='mysql'):
        conf_path = os.path.join(conf_dir, 'dbconf.ini')
        conf = configparser.ConfigParser()
        conf.read(conf_path)
        host = conf.get(session_name, 'host')
        user = conf.get(session_name, 'user')
        password = conf.get(session_name, 'password')
        database = conf.get(session_name, 'database')
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
        #sql = "SELECT distinct channel_id FROM mcloud_channel c LEFT JOIN mcloud_channel_auth a ON c.id=a.channel_id WHERE c.type = (SELECT id FROM mcloud_channel_info WHERE NAME='{}') AND c.status!=-2 AND a.auth_name='{}账号'".format(channelName, channelName)
        #####test
        sql = "SELECT distinct channel_id FROM mcloud_channel c LEFT JOIN mcloud_channel_auth a ON c.id=a.channel_id WHERE c.type = (SELECT id FROM mcloud_channel_info WHERE NAME='{}') AND c.status!=-2 AND c.login_status!=-1 AND a.auth_name='{}账号'".format(channelName, channelName)

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


    '''def getChannelIdByUserName(self, tableName, channelName, userName):
        sql = "select distinct channel_id from {} where channel_info_name = '{}' and auth_name = '{}账号' and auth_value = '{}'".format(tableName, channelName, channelName, userName)
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            id = cursor.fetchone()[0]
        except:
            cursor.close()
            return None
        cursor.close()
        return id'''


    def getTargetIdDictByChannelName(self, channelName):
        sql = "select target_id, type from mcloud_dispatch_task WHERE channel_info_name='{}' AND STATUS=8 and target_id is not null".format(channelName)
        rltDict = {}
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                target_id = row[0]
                type = row[1]
                rltDict[target_id] = type
        except Exception as e:
            rltDict = {}
            raise e
        cursor.close()
        return rltDict


    def insertOneRecord(self, saveDict, tbName):
        keyList = list(saveDict.keys())
        decorateKeyList = ["%(" + elem + ")s" for elem in keyList]
        sql = "replace into {} ({}) values ({})".format(tbName, ",".join(keyList), ",".join(decorateKeyList))
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, saveDict)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        cursor.close()


    def close(self):
        try:
            self.conn.close()
        except:
            print('close connection error')

