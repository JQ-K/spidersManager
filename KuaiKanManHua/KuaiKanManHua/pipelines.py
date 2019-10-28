# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import time
import redis
from KuaiKanManHua.conf.configure import *


class KuaikanmanhuaPipeline(object):
    def process_item(self, item, spider):
        return item


class UserItemPipeline(object):
    def __init__(self):
        # connect redis
        self.pool = redis.ConnectionPool(host=redisHost, port=redisPort, db=redisDb)
        self.r = redis.Redis(connection_pool=self.pool)

        today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        self.filePath = dir + today + ".txt"


    def process_item(self, item, spider):
        isSuccess = True
        isSuccess = self.write_item_file(self.filePath, item) and isSuccess



    def write_item_file(self, filePath, item):
        isSuccess = True
        try:
            f = open(filePath, 'a+', encoding='utf-8')
            f.write(item['user_id'] + '\t' + item['pic_url'] + '\t' + item['nickname'] + item['sign_text'] + '\n')
            f.close()
        except Exception as e:
            isSuccess = False
        return isSuccess





