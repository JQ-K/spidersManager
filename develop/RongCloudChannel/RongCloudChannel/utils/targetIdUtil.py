# -*- coding: utf-8 -*-

from RongCloudChannel.utils.mysqlUtil import MysqlClient


def getAllTargetIdByChannel(channelName):
    mysqlClient = MysqlClient.from_settings(DB_CONF_DIR)
    targetDict = mysqlClient.getTargetIdDictByChannelName(channelName)
    mysqlClient.close()
    return targetDict


