# -*- coding: utf-8 -*-
import scrapy
import json
import time
import requests
import re

from RongCloudChannel.items import *
from RongCloudChannel.utils import dateUtil


class GongzhonghaoappSpider(scrapy.Spider):
    name = 'GongZhongHaoApp'
    channel_id = '公众号'

    ### __biz 和 key 一一对应, 且key的有效时间较短
    __biz = 'test'
    key = 'test'
    uin = 'test'
    firstOffset = 0
    count = 10

    articalListUrl = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz={}&f=json&offset={}&count={}&is_ok=1&uin={}&key={}"

    #param: uin, key, __biz
    articalUrl = "https://mp.weixin.qq.com/mp/getappmsgext?f=json&uin={}&key={}&__biz={}"
    #param: mid, sn, idx, scene
    articalBody = "mid={}&sn={}&idx={}&scene={}&is_only_read=1"
    spaceMark = "&amp;"

    articalHeaders = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1278.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
    }


    def start_requests(self):
        yield scrapy.Request(self.articalListUrl.format(self.__biz, self.firstOffset, self.count, self.uin, self.key),
                             method='GET', callback=self.parseArticalListPage,
                             meta={'biz': self.__biz})


    def parseArticalListPage(self, response):
        rltJson = json.loads(response.text)
        biz = response.meta['biz']
        if 'ret' not in rltJson:
            return
        if rltJson['ret'] != 0:
            print('response error:' + response.text)
            return
        msgListJson = json.loads(rltJson['general_msg_list'])
        msgList = msgListJson['list']
        curTime = dateUtil.getCurDate()
        for msg in msgList:
            contentItem = ContentItem()
            contentItem['channel_id'] = self.channel_id
            contentItem['account_id'] = biz
            contentItem['record_class'] = 'content_info'
            contentItem['crawl_time'] = curTime

            url = msg['app_msg_ext_info']['content_url']
            title = msg['app_msg_ext_info']['title']
            datetime = msg['comm_msg_info']['datetime']
            id = msg['comm_msg_info']['id']

            contentItem['id'] = id
            contentItem['title'] = title
            contentItem['content_link'] = url
            contentItem['publish_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(datetime)))

            time.sleep(5)
            comment_id = self.getCommentId(url)

            curUrl = url.replace("http://mp.weixin.qq.com/s?", "").replace("#wechat_redirect", "")
            paramList = curUrl.split(self.spaceMark)
            mid = ""
            sn = ""
            idx = ""
            scene = ""
            for curParam in paramList:
                if curParam.startswith("mid="):
                    mid = curParam[4:]
                if curParam.startswith("sn="):
                    sn = curParam[3:]
                if curParam.startswith("idx="):
                    idx = curParam[4:]
                if curParam.startswith("scene="):
                    scene = curParam[6:]
            time.sleep(10)
            curBody = self.articalBody.format(mid, sn, idx, scene)
            if comment_id is not None:
                curBody += "&comment_id=" + comment_id
            yield scrapy.Request(self.articalUrl.format(self.uin, self.key, self.__biz),
                                 body=curBody, method='POST',
                                 headers=self.articalHeaders,
                                 callback=self.parseArticalPage,
                                 meta={'contentItem': contentItem})

            break
        '''can_msg_continue = rltJson['can_msg_continue']
        if can_msg_continue == 1:
            next_offset = rltJson['next_offset']
            time.sleep(10)
            yield scrapy.Request(self.articalListUrl.format(self.__biz, next_offset, self.count, self.uin, self.key),
                                 method='GET', callback=self.parseArticalListPage)'''


    def getCommentId(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            return None
        commentIdRlt = re.search(r'var comment_id = "\d+"', response.text)
        if commentIdRlt is not None:
            commentIdStr = commentIdRlt.group(0)
            commentId = commentIdStr.replace('var comment_id = "', '').replace('"', '')
            return commentId
        return None


    def parseArticalPage(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        contentItem = response.meta['contentItem']
        if 'appmsgstat' in rltJson:
            appmsgstat = rltJson['appmsgstat']
            if 'read_num' in appmsgstat:
                contentItem['read_count'] = appmsgstat['read_num']
            if 'like_num' in appmsgstat:
                contentItem['like_count'] = appmsgstat['like_num']
        if 'comment_count' in rltJson:
            contentItem['comment_count'] = rltJson['comment_count']

        print(contentItem)
        #yield contentItem