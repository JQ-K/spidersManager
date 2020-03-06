__author__ = 'zlx'
# -*- coding: utf-8 -*-
import scrapy
import json
import time
import requests
import re
from redis import  Redis
from loguru import logger
from ArticleSpider.items import *
from ArticleSpider.utils.mysqlUtil import *
from ArticleSpider.utils.toKafka import *
from ArticleSpider.utils.readConfig import *
from ArticleSpider.utils.writeConfig import  *
from scrapy.utils.project import get_project_settings
import configparser
import datetime

class WeChatOfficalAccountsSpider(scrapy.Spider):
    name = 'WeChatOffical'
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1278.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat" ,
   }
    settings = get_project_settings()

    def __init__(self, partitionIdx='0',offset=0):

        self.partitionIdx=int(partitionIdx)
        self.offset = offset
        self.headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132'
        }
        self.articalListUrl = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz={0}&f=json&offset={1}&is_ok=1&uin={2}&key={3}"
        self.spaceMark = "&amp;"
         #param: uin, key, __biz
        self.articalUrl = "https://mp.weixin.qq.com/mp/getappmsgext?f=json&uin={}&key={}&__biz={}"
        #param: mid, sn, idx, scene
        self.articalBody = "mid={}&sn={}&idx={}&scene={}&is_only_read=1"

        #初始化redis
        self.redis_host = self.settings.get('REDIS_HOST')
        self.redis_port = self.settings.get('REDIS_PORT')
        self.red = Redis(host=self.redis_host, port=self.redis_port)
        self.redis_wechat_params = self.settings.get('REDIS_WECHAT_PARAMS')
        self.redis_wechat_crawlInfo=self.settings.get('REDIS_WECHAT_CRAWLINFO')
        self.redis_wechat_crawlInfo_expire_time = settings.get('REDIS_WECHAT_CRAWLINFO_EXPIRE_TIME')
        self.red.expire(self.redis_wechat_crawlInfo, self.redis_wechat_crawlInfo_expire_time)

        self.filePath = self.settings.get('FILE_PATH')  #需要在服务器上创建该路径，待做
        self.OtherTypeMsgfile = open(self.filePath+"OtherTypeMsgfile.txt",mode='a',  encoding='UTF-8')



        # 配置kafka连接信息
        self.kafka_hosts = self.settings.get('KAFKA_HOSTS')
        self.zookeeper_hosts=self.settings.get('ZOOKEEPER_HOSTS')
        self.kafka_topic = settings.get('KAFKA_TOPIC_WECHAT')
        self.reset_offset_on_start = self.settings.get('RESET_OFFSET_ON_START')
        logger.info('reset_offset_on_start:%d,1表示true,0表示false' % self.reset_offset_on_start)
        self.kafkaClient = KafkaClient(hosts=self.kafka_hosts,zookeeper_hosts=self.zookeeper_hosts, broker_version='0.10.1.0')
        logger.info('kafka info, hosts:{},zookeeper_hosts:{}, topic:{}'.format(self.kafka_hosts,self.zookeeper_hosts, self.kafka_topic))


    def start_requests(self):
        cnt=0

        try:
            key='798e72fc742f8bb5a6184de2e839269ac2f0285e274f2f7d6be5d4f2812ed337921d93a22f69951062ffbb3b43dc61adf7dfae8539c1db7d7eafa121fd3bf3faf9b8b29ae9fe9fc0281ddf6331ced605'
            __biz='MzAxMDI3NzA1OA=='
            uin='MzkyOTAwMjQw'
            # key='c1a1a95c556e51454f9c831f2db8efba8ee1cff98063eab70817ea201a52df7cb382ee018a10b192c3d3ca8b214d346ed02ccd89283cf451781b76de3e91a7f76a9cc84be51a30bc8c6d178a7fed5f7e'
            # logger.info('uin:{}，key :{}'.format(uin,key))

            yield scrapy.Request(self.articalListUrl.format(__biz, self.offset, uin, key),
                     method='GET', callback=self.parseArticalListPage,
                     dont_filter=True,meta={'__biz': __biz,'uin':uin,'key':key})


        except Exception as e:
            logger.warning('Kafka message structure cannot be resolved :{}'.format(str(e)))

        logger.info('共处理了{}个biz: %d' % cnt)


    def parseArticalListPage(self, response):
        logger.info("start to parseArticalList")
        #爬虫日期
        crawl_time=datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d")+" 23:59:59", "%Y-%m-%d %H:%M:%S")
        rltJson = json.loads(response.text)
        __biz = response.meta.get("__biz", "")
        uin=response.meta.get("uin", "")
        key=response.meta.get("key", "")
        paramsDict={"__biz":__biz,"uin":uin,"key":key}
        ret, status = rltJson.get('ret'), rltJson.get('errmsg')  # 状态信息
        now_unix_time=0   #爬虫失败为0，那么redis中now_unix_time=0

        if 0 == ret or 'ok' == status:
            general_msg_list = rltJson['general_msg_list']
            msg_list= json.loads(general_msg_list)['list']  # 获取文章列表
            logger.info(msg_list)
            ArticalNumList=[]
            for msg in msg_list:   #从时间最早的开始爬取，依次爬到第7天，msg_list中有10天的量,但是日期范围可能是覆盖15天的
                comm_msg_info = msg['comm_msg_info']  # 该数据是本次推送多篇文章公共的
                #没有单篇文章的发布时间，这一天的文章有一个统一的时间，存在于一天的list中
                now_unix_time = int(comm_msg_info['datetime'])
                publish_time = datetime.datetime.fromtimestamp(now_unix_time)  # 发布时间<class 'datetime.datetime'>
                diff_days=(crawl_time-publish_time).days
                logger.info('当前解析{}天前的文章列表'.format(diff_days))
                # logger.info('{},{}'.format(str(now_unix_time), publish_time.strftime('%Y-%m-%d %H:%M:%S')))
                if diff_days >3:
                    logger.info("近7天数据已经爬完啦，当前日期是{}，相差{}天，退出循环"\
                                .format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_unix_time)),str(diff_days)))
                    break
                msg_type = comm_msg_info['type']  # 文章类型
                '''#至此 得到了这篇文章的发布时间
                #判断，是否需要继续爬虫
                #文章表中一日阅读数，即publish_time-crawl_time=1day，将该条记录插入数据库
                #文章表中三日阅读数，即publish_time-crawl_time=3day，将该值更新到数据库中，微信名称、微信账号、SN是唯一标识
               #文章表中七日阅读数，即publish_time-crawl_time=7day，将该值更新到数据库中，微信名称、微信账号、SN是唯一标识
               #假如这7天内的数据还没有爬完，key就失效的情况，如何继续上一次爬虫，根据文件的id
               '''
                # if diff_days not in [1,3]:  #一个公众号下，只抓取符合时间的文章
                #     continue
                #保存0，1，2，3天文章的数量
                if msg_type==49:  #需要爬取全部内容
                    # 49：图文消息：，1：文字消息，3：图片消息
                    logger.info("start to deal type 49")
                    # self.parse_detail(diff_days, paramsDict,msg,publish_time)
                    app_msg_ext_info = msg.get('app_msg_ext_info')  # article原数据
                    logger.info(app_msg_ext_info)
                    oneDayArticalList=[]
                    if app_msg_ext_info:   #
                        # 本次推送的首条文章,
                        logger.info("first artical")
                        oneDayArticalList.append(app_msg_ext_info)

                        logger.info('other artical')
                        multi_app_msg_item_list = app_msg_ext_info.get('multi_app_msg_item_list')
                        if multi_app_msg_item_list:
                            # for item in multi_app_msg_item_list:
                            oneDayArticalList+= multi_app_msg_item_list
                    self.writeToConfig(diff_days,len(oneDayArticalList))


                    #按键精灵脚本2读取参数，进行点击
                    #fiddler捕获每一篇文章的参数传给kafka，再逐一进行解析

                    curBody = ''
                                                                                                                     # MzAxMDI3NzA1OA==
                    yield scrapy.Request(self.articalUrl.format(paramsDict.get('uin',''), paramsDict.get('key',''), 'MzAxMDI3NzA1OA%3D%3D'),
                         body=curBody, method='POST',
                         headers=self.headers,
                         callback=self.parseArticalNum,
                         dont_filter=True,
                         meta={'diff_days':diff_days})
                else:
                    logger.info("msg_type!=49 时list msg ={} ,可查看除type 49以外的其他类型" .format(str(msg)) )
                    #保存到服务器，写入文本文件
                    self.OtherTypeMsgfile.write(str(msg)+'\n\n')


            # 0：结束；1：继续： 一次返回10天的数据，所以这一步目前不需要
            '''
            can_msg_continue = rltJson.get('can_msg_continue')

            if can_msg_continue==1 :
                offset = rltJson.get('next_offset')  # 下一次请求偏移量
                logger.info('Next offset : %d' % offset)
                yield scrapy.Request(self.articalListUrl.format(__biz, offset, uin, key),
                                 method='GET', callback=self.parseArticalListPage,
                                 meta={'biz': __biz,'uin':uin,'key':key})
            else:
                print('Break , Current offset : %d' % self.offset)
            '''
        else:
            logger.info('ret:{}, status:{},表明cookie失效'.format(ret, status))
            '''
            #cookie失效，需要等待下一个cookie，那么redis中now_unix_time=0
            #如果在7天数据未全部爬完的时候，key失效，则返回当前爬取的时间，并保存至redis中,且该key失效时间为12小时
            #同时将biz传给kafka
           '''
            logger.info('失效时，该公众号{}，目前正在爬取该天{}的数据：'.format(__biz,now_unix_time))
            self.red.hmset(self.redis_wechat_crawlInfo,{__biz:now_unix_time})   #
            # bizsToKafka(self.kafkaClient,self.kafka_topic,[__biz])

    def writeToConfig(self,diff_days,num):
        sectionName='wechatArtical_'+str(diff_days)
        rConifg=ReadConifg(self.filePath,"config.ini")
        sectionList=rConifg.read_sections()
        #将这个list传给windows，写入Config.ini中
        wConfig=WriteConfig(self.filePath,"config.ini")
        if sectionName in sectionList:# 如果分组存在则先删除
            wConfig.remove_section(sectionName)
        wConfig.set_options(sectionName, 'num', num)

    def parseArticalNum(self, response):
        #cookie半途失效，可能会导致response.status == 200
        #如何记录半途失效的情况
        logger.info('start to parseArticalNum')
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        logger.info(response.text)
        articalItem = response.meta.get('articalItem','')
        diff_days=response.meta.get('diff_days','')
        if 'appmsgstat' in rltJson:
            appmsgstat = rltJson['appmsgstat']
            if 'read_num' in appmsgstat:
                articalItem['read_cnt_'+str(diff_days)+'day'] = appmsgstat['read_num']
            if 'like_num' in appmsgstat:
                articalItem['inWatching_cnt_'+str(diff_days)+'day'] = appmsgstat['like_num']
        # if 'comment_count' in rltJson:   #猜测：这个评论是总的评论数，而微信界面显示的是精选评论，精选评论在另一个接口
        #     articalItem['_'+diff_days+'_day_comment_count'] = rltJson['comment_count']
        yield articalItem



