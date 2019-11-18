# -*- coding: utf-8 -*-
import re
from RongCloudChannel.conf.configure import *
from RongCloudChannel.utils.mysqlUtil import MysqlClient

def getAllAccountByChannel(channelName):
    accountDict = {}
    mysqlClient = MysqlClient.from_settings(DB_CONF_DIR)
    channelIdList = mysqlClient.getChannelIdList(channelName)
    for id in channelIdList:
        userAndPwd = mysqlClient.getUserAndPwdByChannelId(TB_AUTH_NAME, id)
        if userAndPwd is not None:
            accountDict[userAndPwd[0]] = userAndPwd[1]
    mysqlClient.close()
    return accountDict


def isEmailAccount(account):
    return re.match(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", account)
    #pass

def isPhoneAccount(account):
    return re.match(r"^1\d{10}$", account)
    #return re.match(r"^1[35678]\d{9}$", account)



