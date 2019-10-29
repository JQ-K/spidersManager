# -*- coding: UTF-8 -*-

import json
#import redis

import sys
import os
import configparser
from KuaiKanManHua.utils.myredis import RedisClient

from KuaiKanManHua.conf.configure import *
from KuaiKanManHua.items import UserItem

redisClient = RedisClient.from_settings(DB_CONF_DIR)
print(redisClient.host)
print(redisClient.port)
print(redisClient.db)
'''redisClient = RedisClient('10.8.26.26', 6379, 1)

print(redisClient.host)
print(redisClient.port)
print(redisClient.db)'''
print(REDIS_KEY['channel_conf'])
channelJsonStr = redisClient.get(REDIS_KEY['channel_conf'], -1)
channelJson = json.loads(channelJsonStr)
for value in channelJson.values():
    print(value)
    feedType = value['feedType']
    targetID = value['targetID']
    print(feedType)
    print(targetID)


'''import json
import sys,os
sys.path.append(os.path.abspath('..'))

from conf.configure import *
from utils.myredis import RedisClient
import sys
import os

from utils.myredis import RedisClient

import  configparser
conf = configparser.ConfigParser()


redisClient = RedisClient.from_settings()

print(redisClient.host)

print(CHANNEL_CONF)

redisClient = RedisClient(REDIS_CONF['host'], REDIS_CONF['port'], REDIS_CONF['db'])
#redisClient.put(REDIS_KEY['channel_conf'], json.dumps(CHANNEL_CONF), -1)

channelJsonStr = redisClient.get(REDIS_KEY['channel_conf'], -1)
print(channelJsonStr)
channelJson = json.loads(channelJsonStr)
print(channelJson)
print(type(channelJson))
for channel_name, value in channelJson.items():
    print(channel_name)
    print(value)
    feedType = value['feedType']
    targetID = value['targetID']
    print(feedType)
    print(targetID)'''



