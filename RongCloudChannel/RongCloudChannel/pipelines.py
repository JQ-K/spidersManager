# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

class RongcloudchannelPipeline(object):
    def __init__(self):
        pass
    def process_item(self, item, spider):
        print(json.dumps(dict(item)))
        '''if item['channel_id'] == "百家号":
            f = open('D:/py_workspace/spidersManager/RongCloudChannel/RongCloudChannel/test/baijiahao.txt', "a+", encoding="utf-8")
            f.write(json.dumps(dict(item)) + '\n')
            f.close()'''
        return item
