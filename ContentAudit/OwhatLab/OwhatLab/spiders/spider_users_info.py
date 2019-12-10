# -*- coding: utf-8 -*-

import time
import json
import scrapy

# import sys
# sys.path.append(" D:\gitPython\spidersManager\develop\OwhatLab")
from OwhatLab.conf.configure import *
from  OwhatLab.items import OwhatLabUserIterm
from OwhatLab.utils.myredis import RedisClient


class SpiderUsersInfoSpider(scrapy.Spider):
    name = 'spider_users_info'
    allowed_domains = ['appo4.owhat.cn']
    start_urls = ['http://appo4.owhat.cn/']

    headers = {
        'User-Agent': 'Owhat/1.2.2 (iPhone; iOS 9.3.5; Scale/3.00)',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9, zh-Hant-CN;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '369',
        'Host': 'appo4.owhat.cn',
        'Accept-Encoding': 'gzip, deflate',
        'Proxy - Connection': 'keep - alive',
        'Accept': '*/*',
    }

    flag1 = 0

    # 首页url：PreUrl + listMainUrl
    PreUrl = "https://appo4.owhat.cn/api?"

    # listMainUrl = "apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m=iconlist&cmd_s=index&data=%7B%22type%22%3A%221%22%2C%22parentid%22%3A%220%22%7D&requesttimestap=1575258094.277788&v=1.0"

    # jalouse频道首页--该频道只有一个用户user_id=8244418,s所以无需遍历整个list直接赋值user_id即可

    # 其他频道
    # 公益

    # 明星商品
    # 美妆
    # 零食
    # 运功潮牌
    # 生活方式
    # 偶像志
    # 活动社
    # 星闻社
    # 星生活


    # listMainUrl = "apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m={}&cmd_s={}&data=%7B%22columnid%22%3A%22{}%22%2C%22itemIndex%22%3A{}%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575266544.774394&v=1.0"

    def __init__(self):
        # connect redis
        self.redisClient = RedisClient.from_settings(DB_CONF_DIR)

        new_CHANNEL_CONF = json.dumps(CHANNEL_CONF)
        self.redisClient.put("CHANNEL_CONF", new_CHANNEL_CONF, None, False)

        self.user_set_key = REDIS_KEY['user_id']

        channelJsonStr = self.redisClient.get("CHANNEL_CONF", -1)
        self.channelDict = json.loads(channelJsonStr)
        # print(self.channelDict)

        print('Owhat用户信息爬虫开始...')

    def start_requests(self):
        for value in self.channelDict.values():
            self.flag1 = 1
            curPage = 1
            cmd_m = value['cmd_m']
            cmd_s = value['cmd_s']
            itemIndex = value['itemIndex']
            columnid = str(value['columnid'])
            apiv = value['apiv']

            while curPage > 0 and self.flag1 == 1 and curPage < 81:
                # print('curPage:', curPage)
                print('用户信息抓取：正在抓取itemIndex={}，频道={}，第{}页内容...'.format(itemIndex, columnid, curPage))
                if itemIndex == 2:
                    tempUrl = apiv.format(cmd_m, cmd_s, itemIndex, columnid, curPage)
                else:
                    tempUrl = apiv.format(cmd_m, cmd_s, columnid, itemIndex, curPage)
                curPage += 1
                listUrl = self.PreUrl + tempUrl
                print('用户信息抓取listUrl：', listUrl)
                time.sleep(5)
                yield scrapy.Request(listUrl, method='POST',  # headers=self.headers,
                                     callback=self.parseListUrl)

    def parseListUrl(self, response):
        # print(response.text)
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        content = rltJson['data']
        if content == "":
            print('get list interface error: ' + response.text)
            return
        videoList = content['list']
        # print('videoList内容：',videoList)
        if len(videoList) > 0:
            for videoInfo in videoList:
                user_id = videoInfo['publisherid']
                # print(user_id)
                flag = self.redisClient.sismember(self.user_set_key, user_id)
                if flag == 1:
                    # print('该用户信息已爬虫，不再重复爬取')
                    continue
                else:
                    self.redisClient.sadd(self.user_set_key, user_id)
                    yield self.getUserInfoItem(videoInfo)  # 此处yield函数不可少
        else:
            # print('该频道主页内容的用户信息爬虫已完毕！')
            self.flag1 = 0
            return

    def getUserInfoItem(self, userInfo):
        userItem = OwhatLabUserIterm()

        if 'publisherid' in userInfo:
            userItem['user_id'] = userInfo['publisherid']
        if 'publishername' in userInfo:
            userItem['nick_name'] = userInfo['publishername']
        if 'publisheravatarimg' in userInfo:
            userItem['pic_url'] = userInfo['publisheravatarimg']
        userItem['update_time'] = time.time()

        print('userItem内容：', userItem)

        return userItem  # 此处必须用return返回