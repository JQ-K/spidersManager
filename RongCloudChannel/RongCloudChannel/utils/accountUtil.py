# -*- coding: utf-8 -*-
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
    return accountDict

