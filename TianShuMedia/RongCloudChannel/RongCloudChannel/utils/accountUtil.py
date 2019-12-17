# -*- coding: utf-8 -*-
import re
import time
import json
import requests
from RongCloudChannel.conf.configure import *
from RongCloudChannel.utils.mysqlUtil import MysqlClient
from RongCloudChannel.utils.pwdUtil import *


def getAllAccountByChannel(channelName):
    accountDict = {}
    mysqlClient = MysqlClient.from_settings(DB_CONF_DIR)
    channelIdList = mysqlClient.getChannelIdList(channelName)
    for id in channelIdList:
        userAndPwd = mysqlClient.getUserAndPwdByChannelId(TB_AUTH_NAME, id)
        if userAndPwd is not None:
            #accountDict[userAndPwd[0]] = userAndPwd[1]
            accountDict[userAndPwd[0]] = (userAndPwd[1], id)
    mysqlClient.close()
    return accountDict


def isEmailAccount(account):
    return re.match(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", account) is not None


def isPhoneAccount(account):
    return re.match(r"^1\d{10}$", account) is not None


'''def postLoginErrorAccount(channelName, userName):
    mysqlClient = MysqlClient.from_settings(DB_CONF_DIR)
    id = mysqlClient.getChannelIdByUserName(TB_AUTH_NAME, channelName, userName)
    mysqlClient.close()
    if id is None:
        return

    curTimeStamp = str(int(time.time()) * 1000)
    k = md5(APP_ID + curTimeStamp + SECRET)
    postDict = {'appId': APP_ID, 'k': k, 'timestamp': curTimeStamp, 'd':[]}
    idTempDict = {'c': id, 's': -1}
    postDict['d'].append(idTempDict)

    message = json.dumps(postDict)
    print('*****************疑似无效账号，发送post请求:')
    print(message)

    response = requests.post(POST_CONF['login_error_api'], message, headers=POST_CONF['headers'])
    print('*****************收到回复:')
    print(response.text)'''


def postLoginErrorAccount(curId):
    '''mysqlClient = MysqlClient.from_settings(DB_CONF_DIR)
    id = mysqlClient.getChannelIdByUserName(TB_AUTH_NAME, channelName, userName)
    mysqlClient.close()'''

    id = curId

    if id is None:
        return

    curTimeStamp = str(int(time.time()) * 1000)
    k = md5(APP_ID + curTimeStamp + SECRET)
    postDict = {'appId': APP_ID, 'k': k, 'timestamp': curTimeStamp, 'd':[]}
    idTempDict = {'c': id, 's': -1}
    postDict['d'].append(idTempDict)

    message = json.dumps(postDict)
    print('*****************疑似无效账号，发送post请求:')
    print(message)

    response = requests.post(POST_CONF['login_error_api'], message, headers=POST_CONF['headers'])
    print('*****************收到回复:')
    print(response.text)


def isErrorAccount(channelName, text):
    flag = False
    try:
        textJson = json.loads(text)
    except:
        return flag

    if channelName == '美拍':
        if 'meta' in textJson:
            if 'code' in textJson['meta']:
                if textJson['meta']['code'] == 20170:
                    flag = True

    if channelName == '趣头条':
        if 'code' in textJson:
            if textJson['code'] == -105:
                flag = True

    if channelName == '一点资讯':
        if 'errorCode' in textJson:
            if textJson['errorCode'] == 299:
                flag = True

    return flag

