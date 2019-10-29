# -*- coding: UTF-8 -*-
import json
import sys,os
sys.path.append(os.path.abspath('..'))

from conf.configure import *
from utils.myredis import RedisClient

#redisClient = RedisClient(REDIS_CONF['host'], REDIS_CONF['port'], REDIS_CONF['db'])

#print(redisClient.host)
print(CHANNEL_CONF)

'''for channel_name, value in CHANNEL_CONF.items():
    print(channel_name)
    print(value)
    feedType = value['feedType']
    targetID = value['targetID']
    print(feedType)
    print(targetID)'''

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
    print(targetID)




