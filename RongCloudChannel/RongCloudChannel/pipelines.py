# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import requests

class RongcloudchannelPipeline(object):

    api = "http://beta.rongcloud.zhanqi.tv/api/mcloud/stat/partner/sync_statistics"
    headers = {
        'content-type': 'application/json'
    }

    def __init__(self):
        self.resultDict = {}
        self.listItem = []


    def process_item(self, item, spider):
        print(json.dumps(dict(item)))
        self.writeItemToTxt(item)

        if item['record_class'] == 'channel_info':
            self.updateChannelInfo(item)

        if item['record_class'] == 'content_info':
            self.updateContentInfo(item)

        if len(self.listItem) == 10:
            self.postItems()

        return item


    def writeItemToTxt(self, item):
        f = open('D:/py_workspace/spidersManager/RongCloudChannel/RongCloudChannel/test/{}.txt'.format(item['channel_id']),
                 "a+", encoding="utf-8")
        f.write(json.dumps(dict(item)) + '\n')
        f.close()


    def updateChannelInfo(self, item):
        if item['channel_id'] == "百家号":
            self.resultDict['code'] = item['channel_id']
            self.resultDict['nfs'] = item['new_subscribe_count']
            self.resultDict['cfs'] = item['cancel_fans_count']
        if item['channel_id'] == "企鹅号":
            self.resultDict['code'] = item['channel_id']


    def updateContentInfo(self, item):
        tempDict = {}

        if item['channel_id'] == "百家号":
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

        if item['channel_id'] == "企鹅号":
            tempDict['cn'] = item['channel_id']
            tempDict['sa'] = item['crawl_time']
            tempDict['tid'] = item['id']
            tempDict['t'] = item['title']
            tempDict['lk'] = item['content_link']
            tempDict['pt'] = item['publish_time']
            tempDict['vc'] = item['read_count']
            tempDict['c'] = item['comment_count']

        if item['channel_id'] == "趣头条":
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

        self.listItem.append(tempDict)


    def postItems(self):
        if len(self.listItem) > 0:
            if "code" not in self.resultDict:
                self.resultDict['code'] = self.listItem[0]['cn']
            self.resultDict['s'] = self.listItem
            message = json.dumps(self.resultDict)
            print(message)
            requests.post(self.api, message, headers=self.headers)
            self.listItem.clear()


    def close_spider(self, spider):
        self.postItems()
