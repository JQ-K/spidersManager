# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import request

class RongcloudchannelPipeline(object):
    api = "http://beta.rongcloud.zhanqi.tv/api/mcloud/stat/partner/sync_statistics"
    def __init__(self):
        pass
    def process_item(self, item, spider):
        print(json.dumps(dict(item)))
        '''if item['channel_id'] == "百家号":
            f = open('D:/py_workspace/spidersManager/RongCloudChannel/RongCloudChannel/test/baijiahao.txt', "a+", encoding="utf-8")
            f.write(json.dumps(dict(item)) + '\n')
            f.close()'''

        '''if item['channel_id'] == "企鹅号":
                    f = open('D:/py_workspace/spidersManager/RongCloudChannel/RongCloudChannel/test/qierhao.txt', "a+", encoding="utf-8")
                    f.write(json.dumps(dict(item)) + '\n')
                    f.close()'''

        #request.post(self.api, json=)
        return item
