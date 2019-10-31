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
        return item
