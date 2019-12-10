# -*- coding: utf-8 -*-
import scrapy
import json

import time

from OwhatLab.conf.configure import *
from OwhatLab.utils.myredis import RedisClient
from OwhatLab.items import OwhatLabArticleItem, OwhatLabUserIterm


class SpiderCommentUsersInfoSpider(scrapy.Spider):
    name = 'spider_comment_users_info'
    allowed_domains = ['appo4.owhat.cn']
    start_urls = ['http://appo4.owhat.cn/']

    # 首页url：PreUrl + listMainUrl
    PreUrl = "https://appo4.owhat.cn/api?"
    # jalouse频道首页--该频道只有一个用户user_id=8244418,s所以无需遍历整个list直接赋值user_id即可

    flag1 = 0

    # 用户详情页--文章类信息url,各个频道相同：
    #ArticleMainUrl = "apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m=home&cmd_s=userindex&data=%7B%22userid%22%3A{}%2C%22tabtype%22%3A2%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575256658.578629&v=1.0"

    # "apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m=home&cmd_s=userindex&data=%7B%22userid%22%3A%228244418%22%2C%22tabtype%22%3A2%2C%22pagenum%22%3A%221%22%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575283078.534425&v=1.0"


    #思路1: 爬虫步骤： 先对具体某个频道的主页url进入找到内容list，每页显示20条，可以翻页展示-----再对list中的每一项找到对应的user_id-------然后在ArticleMainUrl中传入user_id参数，抓取该用户的全部文章信息
    #思路2：爬虫步骤： 先对具体某个频道的主页url进入找到内容list，对list中的每一项分别抓取其用户信息，文章信息，商品信息，评论用户信息需通过文章id进一步去请求url解析


def __init__(self):
    # connect redis
    self.redisClient = RedisClient.from_settings(DB_CONF_DIR)
    new_CHANNEL_CONF = json.dumps(CHANNEL_CONF)
    self.redisClient.put("CHANNEL_CONF", new_CHANNEL_CONF, None, False)

    self.user_set_key = REDIS_KEY['user_id']

    channelJsonStr = self.redisClient.get("CHANNEL_CONF", -1)
    self.channelDict = json.loads(channelJsonStr)
    # print(self.channelDict)
    print('Owhat评论用户信息爬虫开始...')


def start_requests(self):
    for value in self.channelDict.values():
        if value['itemIndex'] in ['1', '2', '9', '10', '11', '12']:
            self.flag1 = 1
            curPage = 1
            cmd_m = value['cmd_m']
            cmd_s = value['cmd_s']
            itemIndex = value['itemIndex']
            columnid = str(value['columnid'])
            apiv = value['apiv']

            while curPage > 0 and self.flag1 == 1 and curPage < 81:
                # print('curPage:', curPage)
                print('文章信息抓取：正在抓取itemIndex={}，频道={}，第{}页内容...'.format(itemIndex, columnid, curPage))
                if itemIndex == 2:
                    tempUrl = apiv.format(cmd_m, cmd_s, itemIndex, columnid, curPage)
                else:
                    tempUrl = apiv.format(cmd_m, cmd_s, columnid, itemIndex, curPage)
                curPage += 1
                listUrl = self.PreUrl + tempUrl
                # print('文章信息抓取listUrl：', listUrl)
                time.sleep(5)
                yield scrapy.Request(listUrl, method='POST',  # headers=self.headers,
                                     callback=self.parseListUrl)
        else:
            continue


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
    # print('videoList内容：', videoList)
    if len(videoList) > 0:
        for videoInfo in videoList:
            if 'articlestatus' in videoInfo:
                article_id = videoInfo['entityid']
                # print(article_id)
                # 此处不能加判断article_id是否已经在redis key中，因为文章爬虫和评论用户爬虫可能独立运行
                comment_apiv = "apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m=findcommentsbyarticleid&cmd_s=community.comment&data=%7B%22childcommentlimit%22%3A%2220%22%2C%22articleid%22%3A%22{}%22%2C%22pagesize%22%3A%2220%22%2C%22sortby%22%3A%22newest%22%7D&requesttimestap=1575614795.023966&v=1.0"
                commentUrl = self.PreUrl + comment_apiv.format(article_id)
                print('评论用户信息抓取listUrl：', commentUrl)
                time.sleep(5)
                yield scrapy.Request(commentUrl, method='POST',  # headers=self.headers,
                                     callback=self.parseCommentListUrl)

            else:
                continue
    else:
        # print('该频道主页内容的文章爬虫已完毕！')
        self.flag1 = 0
        return


def parseCommentListUrl(self, response):
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
            if 'creatordto' in videoInfo:
                userItem = OwhatLabUserIterm()
                creatorInfo = videoInfo['creatordto']
                if 'userid' in creatorInfo:
                    user_id = creatorInfo['userid']
                    if self.redisClient.sismember(self.user_set_key, user_id) == 1:
                        continue
                    else:
                        self.redisClient.sadd(self.user_set_key, user_id)
                        userItem['user_id'] = creatorInfo['userid']
                        if 'nickname' in creatorInfo:
                            userItem['nick_name'] = creatorInfo['nickname']
                        if 'avatarimg' in creatorInfo:
                            userItem['pic_url'] = creatorInfo['avatarimg']

                        userItem['update_time'] = time.time()

                        print('userItem：', userItem)
                        return userItem
                else:
                    continue

    else:
        return