#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'

import pymysql
import time

from loguru import logger

OperationalError = pymysql.OperationalError


# 连接MySQL数据库
class MySQLClient:
    def __init__(self, host, user, password, dbname, port=3306, charset="utf8"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.charset = charset
        self.dbname = dbname
        self.conn = None
        self._conn()


    def _conn(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password)
            self.conn.autocommit(True)
            self.conn.set_charset(self.charset)
            self.cur = self.conn.cursor()
            if (self.dbname):
                try:
                    self.conn.select_db(self.dbname)
                except pymysql.Error as e:
                    logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))
                    return False
            return True
        except pymysql.Error as e:
            logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            return False

    def _reConn(self, num=28800, stime=3):  # 重试连接总次数为1天,这里根据实际情况自己设置,如果服务器宕机1天都没发现就......
        _number = 0
        _status = True
        while _status and _number <= num:
            try:
                self.conn.ping()  # cping 校验连接是否异常
                _status = False
            except:
                if self._conn() == True:  # 重新连接,成功退出
                    break
                _number += 1
                time.sleep(stime)  # 连接不成功,休眠3秒钟,继续循环，知道成功或重试次数结束

    # def __del__(self):
    #     self.close()

    def selectDb(self, db):
        self._reConn()
        try:
            self.conn.select_db(db)
        except pymysql.Error as e:
            logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def query(self, sql):
        self._reConn()
        try:
            n = self.cur.execute(sql)
            return n
        except pymysql.Error as e:
            logger.error("Mysql Error:%s\nSQL:%s" % (e, sql))
            return 0

    def queryMany(self, sql, args):
        self._reConn()
        try:
            n = self.cur.executemany(sql, args)
            return n
        except pymysql.Error as e:
            logger.error("Mysql Error:%s\nSQL:%s" % (e, sql))
            return 0

    def fetchRow(self):
        self._reConn()
        result = self.cur.fetchone()
        return result

    def fetchAll(self):
        self._reConn()
        result = self.cur.fetchall()
        desc = self.cur.description
        d = []
        for inv in result:
            _d = {}
            for i in range(0, len(inv)):
                _d[desc[i][0]] = str(inv[i])
            d.append(_d)
        return d

    def insert(self, table_name, data):
        self._reConn()
        columns = data.keys()
        _prefix = "".join(['INSERT INTO `', table_name, '`'])
        _fields = ",".join(["".join(['`', column, '`']) for column in columns])
        _values = ",".join(["%s" for i in range(len(columns))])
        _sql = "".join([_prefix, "(", _fields, ") VALUES (", _values, ")"])
        _params = [data[key] for key in columns]
        return self.cur.execute(_sql, tuple(_params))

    def update(self, tbname, data, condition):
        self._reConn()
        condition_str = ''
        for key, value in condition.items():
            condition_str += ' {} = {} AND '.format(key, value)
        condition_str = condition_str[:-5]
        _fields = []
        _prefix = "".join(['UPDATE `', tbname, '`', 'SET'])
        for key in data.keys():
            _fields.append("`%s` = '%s'" % (key, data[key]))
        _sql = " ".join([_prefix, ','.join(_fields), 'WHERE', condition_str])
        return self.cur.execute(_sql)

    def delete(self, tbname, condition):
        self._reConn()
        condition_str = ''
        for key, value in condition.items():
            condition_str += ' {} = {} AND '.format(key, value)
        condition_str = condition_str[:-5]
        _prefix = "".join(['DELETE FROM  `', tbname, '`', ' WHERE '])
        _sql = "".join([_prefix, condition_str])
        return self.cur.execute(_sql)

    def select(self, tbname, condition):
        self._reConn()
        condition_str = ''
        for key, value in condition.items():
            condition_str += ' {} = {} AND '.format(key, value)
        condition_str = condition_str[:-5]
        _prefix = "".join(['SELECT * FROM  `', tbname, '`', ' WHERE '])
        _sql = "".join([_prefix, condition_str])
        return self.cur.execute(_sql)

    def getLastInsertId(self):
        self._reConn()
        return self.cur.lastrowid

    def rowcount(self):
        self._reConn()
        return self.cur.rowcount

    def commit(self):
        self._reConn()
        self.conn.commit()

    def rollback(self):
        self._reConn()
        self.conn.rollback()

    def close(self):
        self.cur.close()
        self.conn.close()
