# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import json
import datetime
import redis
from loguru import logger
from scrapy.utils.project import get_project_settings
from pykafka import KafkaClient
from NewsCheck.util.EmailClass import EmailClass


class NewscheckPipeline(object):
    def __init__(self):
        self.settings = get_project_settings()
        self.redis_host = self.settings.get('REDIS_HOST')
        self.redis_port = self.settings.get('REDIS_PORT')
        self.red = redis.Redis(host=self.redis_host, port=self.redis_port)

        self.today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        self.totalNum = 0

    def process_item(self, item, spider):
        #item['crawl_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['crawl_time'] = int(time.time())
        #isSuccess = self.writeItemToTxt(item)
        isSuccess = self.writeNewsIdToRedis(spider.name, item['id'])
        if not isSuccess:
            logger.info('write id to redis failed: ' + str(item['id']))
        else:
            logger.info('get one news: ' + str(item['id']))
            self.totalNum += 1
        return item

    def writeItemToTxt(self, item):
        settings = get_project_settings()
        try:
            f = open(settings.get('NEWS_INFO_ITEM_FILE_PATH') + '{}.txt'.format(self.today), "a+", encoding="utf-8")
            f.write(json.dumps(dict(item)) + '\n')
            f.close()
            return True
        except:
            return False

    def writeNewsIdToRedis(self, key_name, id):
        try:
            self.red.sadd(key_name, id)
            return True
        except:
            return False

    def close_spider(self, spider):
        #self.red.close()
        print('此次爬虫抓取统计结果:')
        print(self.totalNum)



class KuaishouKafkaPipeline(object):
    def open_spider(self, spider):
        settings = get_project_settings()
        self.kafka_hosts = settings.get('KAFKA_HOSTS')
        self.kafka_topic = settings.get('KAFKA_TOPIC')
        client = KafkaClient(hosts=self.kafka_hosts)
        topic = client.topics[self.kafka_topic]
        self.producer = topic.get_producer()
        self.producer.start()
        spider.logger.info('KafkaClient:hosts = %s,topic = %s' % (self.kafka_hosts, self.kafka_topic))
        self.fakeNum = 0


    def process_item(self, item, spider):
        if self.isNewsFake(item):
            if spider.name in ['PiYaoPlatform',]:
                tempDict = self.getDict(item, spider.name)
                msg = bytes(json.dumps(tempDict), encoding='utf-8')
            else:
                msg = bytes(json.dumps(dict(item)), encoding='utf-8')
            self.producer.produce(msg)
            spider.logger.info('Msg Produced kafka[%s]: %s' % (self.kafka_topic, msg))
            logger.info('--add one fake news--: ' + str(item['id']))
            self.fakeNum += 1
        return item


    def isNewsFake(self, item):
        # wordList = ['肺炎','疫情','野味','武汉','病例','浙一','疾控','发热','口罩','N95','蝙蝠',
        #             '果子狸','钟南山','重大卫生事件','冠状病毒','卫健委','发烧','咳嗽','隔离','传染']
        wordList = ['肺炎', '疫情', '野味', '武汉', '病例', '浙一', '疾控', '发热', '口罩',
                    'N95', '蝙蝠', '果子狸', '钟南山', '重大卫生事件', '冠状病毒', '卫健委',
                    '发烧', '咳嗽', '隔离', '传染', '感染', '2019-nCov', '确诊', '突发公共卫生事件',
                    '驰援', '雷神山', '火神山', '小汤山', '封城', '钟南山', 'SARS', '消毒']
        cont = ''
        if 'title' in item:
            cont += item['title']
        if 'content' in item:
            cont += item['content']
        if 'text' in item:
            cont += item['text']

        for word in wordList:
            if cont.find(word) >= 0:
                return True
        return False


    def getDict(self, item, spider_name):
        rltDict = {}
        if 'channel' in item:
            rltDict['spider_name'] = spider_name
        else:
            rltDict['spider_name'] = None

        if 'id' in item:
            rltDict['msg_id'] = item['id']
        else:
            rltDict['msg_id'] = None

        if 'url' in item:
            rltDict['msg_link'] = item['url']
        else:
            rltDict['msg_link'] = None

        if 'title' in item:
            rltDict['msg_title'] = item['title']
        else:
            rltDict['msg_title'] = None

        if 'content' in item:
            rltDict['msg_content'] = item['content']
        else:
            rltDict['msg_content'] = None

        if 'text' in item:
            rltDict['msg_text'] = item['text']
        else:
            rltDict['msg_text'] = None

        if 'publish_time' in item:
            rltDict['msg_update_time'] = item['publish_time']
        else:
            rltDict['msg_update_time'] = None

        if 'crawl_time' in item:
            rltDict['msg_create_time'] = item['crawl_time']
        else:
            rltDict['msg_create_time'] = None

        rltDict['fake_alias'] = None
        rltDict['fake_id'] = None
        rltDict['fake_nickname'] = None
        rltDict['fake_head_img'] = None
        rltDict['msg_cover'] = None
        rltDict['msg_digest'] = None

        return rltDict


    def close_spider(self, spider):
        self.producer.stop()
        spider.logger.info('kafka[%s] Producer stoped!' % (self.kafka_topic))
        print('疑似新闻数量:')
        print(self.fakeNum)



class KuaiShouPipeline(object):
    def __init__(self):
        self.today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        #self.path = '/Users/macbookpro/PycharmProjects/spidersManager/TianShuMedia/NewsCheck/'
        self.path = '/data/code/crawlab-master/data/kuaishou/ZJRB/'
        #self.path = 'D:/ZJRB/'
        self.filepath = self.path + '{}.txt'.format(self.today)
        self.totalNum = 0

        f = open(self.filepath, "a+", encoding="utf-8")
        msg = 'id' + '\t' + '链接' + '\t' + \
              '标题' + '\t' + '发布时间' + '\t' + \
              '原始阅读数' + '\t' + '原始点赞数' + '\t' + '原始评论数' + '\t' + \
              '阅读数' + '\t' + '点赞数' + '\t' + '评论数'
        f.write(msg + '\n')
        f.close()

    def process_item(self, item, spider):
        isSuccess = self.writeItemToTxt(item)
        if not isSuccess:
            logger.info('write item txt failed: ' + str(item['id']))
        else:
            logger.info('get one news: ' + str(item['id']))
            self.totalNum += 1
        return item

    def writeItemToTxt(self, item):
        try:
            f = open(self.filepath, "a+", encoding="utf-8")
            msg = item['id'] + '\t' + item['url'] + '\t' + \
                  item['title'] + '\t' + item['publish_time'] + '\t' + \
                  item['read_count'] + '\t' + item['like_count'] + '\t' + item['comment_count'] + '\t' + \
                  self.getCountStr(item['read_count']) + '\t' + self.getCountStr(item['like_count']) + '\t' + self.getCountStr(item['comment_count'])
            f.write(msg + '\n')
            f.close()
            return True
        except:
            return False

    def getCountStr(self, cnt):
        if cnt.find('w') < 0:
            return cnt
        d = float(cnt.strip().replace('w', '')) * 10000
        return str(int(d))

    def close_spider(self, spider):
        email = EmailClass()
        email.send(self.filepath)
        print('此次爬虫抓取统计结果: ' + str(self.totalNum))


