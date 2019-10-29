# -*- coding: UTF-8 -*-
import sys
import os

from utils.myredis import RedisClient


import  configparser


redisClient = RedisClient.from_settings()

print(redisClient.host)



