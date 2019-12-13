#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'

import pymysql
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
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password)
            self.conn.autocommit(True)
            self.conn.set_charset(self.charset)
            self.cur = self.conn.cursor()
            if (dbname):
                try:
                    self.conn.select_db(dbname)
                except pymysql.Error as e:
                    print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    # def __del__(self):
    #     self.close()

    def selectDb(self, db):
        try:
            self.conn.select_db(db)
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def query(self, sql):
        try:
            n = self.cur.execute(sql)
            return n
        except pymysql.Error as e:
            print("Mysql Error:%s\nSQL:%s" % (e, sql))
            return 0

    def queryMany(self, sql, args):
        try:
            n = self.cur.executemany(sql, args)
            return n
        except pymysql.Error as e:
            print("Mysql Error:%s\nSQL:%s" % (e, sql))
            return 0

    def fetchRow(self):
        result = self.cur.fetchone()
        return result

    def fetchAll(self):
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
        columns = data.keys()
        _prefix = "".join(['INSERT INTO `', table_name, '`'])
        _fields = ",".join(["".join(['`', column, '`']) for column in columns])
        _values = ",".join(["%s" for i in range(len(columns))])
        _sql = "".join([_prefix, "(", _fields, ") VALUES (", _values, ")"])
        _params = [data[key] for key in columns]
        return self.cur.execute(_sql, tuple(_params))

    def update(self, tbname, data, condition):
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
        condition_str = ''
        for key, value in condition.items():
            condition_str += ' {} = {} AND '.format(key, value)
        condition_str = condition_str[:-5]
        _prefix = "".join(['DELETE FROM  `', tbname, '`', ' WHERE '])
        _sql = "".join([_prefix, condition_str])
        return self.cur.execute(_sql)

    def select(self, tbname, condition):
        condition_str = ''
        for key, value in condition.items():
            condition_str += ' {} = "{}" AND '.format(key, value)
        condition_str = condition_str[:-5]
        _prefix = "".join(['SELECT * FROM  `', tbname, '`', ' WHERE '])
        _sql = "".join([_prefix, condition_str])
        return self.cur.execute(_sql)

    def getLastInsertId(self):
        return self.cur.lastrowid

    def rowcount(self):
        return self.cur.rowcount

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cur.close()
        self.conn.close()
