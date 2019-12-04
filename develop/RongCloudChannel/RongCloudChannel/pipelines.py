# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import time
import requests

from RongCloudChannel.conf.configure import *
from RongCloudChannel.utils.pwdUtil import *

class RongcloudchannelPipeline(object):

    api = POST_CONF['url']
    headers = POST_CONF['headers']

    def __init__(self):
        self.resultDict = {}
        self.listItem = []
        self.accountStaticDict = {}


    def process_item(self, item, spider):
        #print(json.dumps(dict(item)))
        #self.writeItemToTxt(item)

        account = item['account_id']
        if account in self.accountStaticDict:
            self.accountStaticDict[account] += 1
        else:
            self.accountStaticDict[account] = 1

        if item['record_class'] == 'channel_info':
            self.updateChannelInfo(item)

        if item['record_class'] == 'content_info':
            self.updateContentInfo(item)

        if len(self.listItem) == 10:
            self.postItems()

        return item


    def writeItemToTxt(self, item):
        f = open(ITEM_FILE_PATH + '{}.txt'.format(item['channel_id']), "a+", encoding="utf-8")
        f.write(json.dumps(dict(item)) + '\n')
        f.close()


    def updateChannelInfo(self, item):
        if 'channel_id' in item:
            self.resultDict['code'] = item['channel_id']
        if 'new_visit_count' in item:
            self.resultDict['ngc'] = self.getIntValue(item['new_visit_count'])
        if 'total_visit_count' in item:
            self.resultDict['tgc'] = self.getIntValue(item['total_visit_count'])
        if 'new_subscribe_count' in item:
            self.resultDict['nfs'] = self.getIntValue(item['new_subscribe_count'])
        if 'total_subscribe_count' in item:
            self.resultDict['fs'] = self.getIntValue(item['total_subscribe_count'])
        if 'cancel_fans_count' in item:
            self.resultDict['cfs'] = self.getIntValue(item['cancel_fans_count'])


    def updateContentInfo(self, item):
        tempDict = {}
        if 'channel_id' in item:
            tempDict['cn'] = item['channel_id']
        if 'crawl_time' in item:
            tempDict['sa'] = item['crawl_time']
        if 'id' in item:
            tempDict['tid'] = str(item['id'])
        if 'title' in item:
            tempDict['t'] = str(item['title'])
        if 'content_link' in item:
            tempDict['lk'] = str(item['content_link'])
        if 'publish_time' in item:
            tempDict['pt'] = str(item['publish_time'])
        if 'publish_status' in item:
            tempDict['s'] = str(item['publish_status'])
        if 'read_count' in item:
            tempDict['vc'] = self.getIntValue(item['read_count'])
        if 'comment_count' in item:
            tempDict['c'] = self.getIntValue(item['comment_count'])
        if 'share_count' in item:
            tempDict['fwd'] = self.getIntValue(item['share_count'])
        if 'collect_count' in item:
            tempDict['fav'] = self.getIntValue(item['collect_count'])
        if 'recommend_count' in item:
            tempDict['rc'] = self.getIntValue(item['recommend_count'])
        if 'like_count' in item:
            tempDict['dc'] = self.getIntValue(item['like_count'])
        if 'download_count' in item:
            tempDict['dwn'] = self.getIntValue(item['download_count'])

        self.listItem.append(tempDict)


    def getIntValue(self, val):
        try:
            rlt = int(val)
        except:
            rlt = 0
        return rlt


    def postItems(self):
        if len(self.listItem) > 0:
            if "code" not in self.resultDict:
                self.resultDict['code'] = self.listItem[0]['cn']
            curTimeStamp = str(int(time.time())*1000)
            self.resultDict['k'] = md5(APP_ID + curTimeStamp + SECRET)
            self.resultDict['s'] = self.listItem
            self.resultDict['appId'] = APP_ID
            self.resultDict['timestamp'] = curTimeStamp
            message = json.dumps(self.resultDict)
            #print(message)
            response = requests.post(self.api, message, headers=self.headers)
            #print(response.text)
            self.listItem.clear()


    def close_spider(self, spider):
        self.postItems()

        print('此次爬虫抓取统计结果:')
        print(self.accountStaticDict)
