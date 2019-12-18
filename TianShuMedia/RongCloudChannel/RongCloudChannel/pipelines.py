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
        self.totalDict = {}
        self.accountStaticDict = {}


    def process_item(self, item, spider):
        #print(json.dumps(dict(item)))
        #self.writeItemToTxt(item)
        if 'account_id' in item:
            if item['record_class'] == 'content_info':
                account = item['account_id']
                if account in self.accountStaticDict:
                    self.accountStaticDict[account] += 1
                else:
                    self.accountStaticDict[account] = 1

        if item['record_class'] == 'channel_info':
            self.updateChannelInfo(item)

        if item['record_class'] == 'content_info':
            self.updateContentInfo(item)

        return item


    def writeItemToTxt(self, item):
        f = open(ITEM_FILE_PATH + '{}.txt'.format(item['channel_id']), "a+", encoding="utf-8")
        f.write(json.dumps(dict(item)) + '\n')
        f.close()


    def updateChannelInfo(self, item):
        account = item['account_id']
        if account not in self.totalDict:
            self.totalDict[account] = {}
            self.totalDict[account]['s'] = []

        if 'channel_id' in item:
            self.totalDict[account]['code'] = item['channel_id']
        if 'new_visit_count' in item:
            self.totalDict[account]['ngc'] = self.getIntValue(item['new_visit_count'])
        if 'total_visit_count' in item:
            self.totalDict[account]['tgc'] = self.getIntValue(item['total_visit_count'])
        if 'new_subscribe_count' in item:
            self.totalDict[account]['nfs'] = self.getIntValue(item['new_subscribe_count'])
        if 'total_subscribe_count' in item:
            self.totalDict[account]['fs'] = self.getIntValue(item['total_subscribe_count'])
        if 'cancel_fans_count' in item:
            self.totalDict[account]['cfs'] = self.getIntValue(item['cancel_fans_count'])


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

        account = item['account_id']
        if account not in self.totalDict:
            self.totalDict[account] = {}
            self.totalDict[account]['s'] = []
            tempChannelId = item['channel_id']
            self.totalDict[account]['code'] = tempChannelId
        self.totalDict[account]['s'].append(tempDict)

        if len(self.totalDict[account]['s']) == 10:
            self.postItems(account)


    def postItems(self, account):
        curTimeStamp = str(int(time.time()) * 1000)
        self.totalDict[account]['k'] = md5(APP_ID + curTimeStamp + SECRET)
        self.totalDict[account]['appId'] = APP_ID
        self.totalDict[account]['timestamp'] = curTimeStamp
        message = json.dumps(self.totalDict[account])
        #print(message)
        response = requests.post(self.api, message, headers=self.headers)
        #print(response.text)
        if self.isRightResponse(response):
            self.totalDict[account]['s'].clear()
        else:
            print('bad post:' + message)
            print('bad resp:' + response.text)


    def getIntValue(self, val):
        try:
            rlt = int(val)
        except:
            rlt = 0
        return rlt


    def isRightResponse(self, response):
        rltJson = json.loads(response.text)
        if 'code' in rltJson:
            if rltJson['code'] == 0:
                return True
            else:
                return False
        return False


    def writeItemToMysql(self, item):
        pass


    def close_spider(self, spider):
        for account in self.totalDict.keys():
            self.postItems(account)

        print('此次爬虫抓取统计结果:')
        print(self.accountStaticDict)
