# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import requests

class RongcloudchannelPipeline(object):
    api = "http://beta.rongcloud.zhanqi.tv/api/mcloud/stat/partner/sync_statistics"
    def __init__(self):
        self.resultDict = {}
        self.listItem = []
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

        if item['record_class'] == 'channel_info':
            if item['channel_id'] == "百家号":
                self.resultDict['code'] = item['channel_id']
                self.resultDict['nfs'] = item['new_subscribe_count']
                self.resultDict['cfs'] = item['cancel_fans_count']
            if item['channel_id'] == "企鹅号":
                self.resultDict['code'] = item['channel_id']
        if item['record_class'] == 'content_info':
            if item['channel_id'] == "百家号":
                tempDict = {}
                tempDict['cn'] = item['channel_id']
                tempDict['sa'] = item['crawl_time']
                tempDict['tid'] = item['id']
                tempDict['t'] = item['title']
                tempDict['lk'] = item['content_link']
                tempDict['pt'] = item['publish_time']
                tempDict['s'] = str(item['publish_status'])
                tempDict['vc'] = item['read_count']
                tempDict['c'] = item['comment_count']
                tempDict['fwd'] = item['share_count']
                tempDict['fav'] = item['collect_count']
                tempDict['rc'] = item['recommend_count']
                tempDict['dc'] = item['like_count']
                self.listItem.append(tempDict)
            if item['channel_id'] == "企鹅号":
                tempDict = {}
                tempDict['cn'] = item['channel_id']
                tempDict['sa'] = item['crawl_time']
                tempDict['tid'] = item['id']
                tempDict['t'] = item['title']
                tempDict['lk'] = item['content_link']
                tempDict['pt'] = item['publish_time']
                tempDict['vc'] = item['read_count']
                tempDict['c'] = item['comment_count']
        return item

    def close_spider(self, spider):
        '''self.resultDict['s'] = self.listItem
        message = json.dumps(self.resultDict)
        print(message)
        requests.post(self.api, message)'''
