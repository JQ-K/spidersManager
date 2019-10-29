# -*- coding: UTF-8 -*-
#import json
#import redis


import sys
import os

from utils.myredis import RedisClient


import  configparser
conf = configparser.ConfigParser()

sys.path.append(os.path.abspath('..'))

current_path = os.path.dirname(os.path.realpath(__file__))
parent_path =  os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
conf_path = os.path.join(parent_path, 'conf\dbconf.ini')
print(current_path)
print(parent_path)
print(conf_path)

conf.read(conf_path)
print(conf.sections())
host = conf.get('redis', 'host')
port = conf.get('redis','port')
db = conf.get('redis', 'db')
#redisClient = RedisClient(host, port, db)
redisClient = RedisClient.from_settings()

print(redisClient.host)




