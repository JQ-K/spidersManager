# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouPhotoSubCommentItem
from KuaiShou.utils.mysql import MySQLClient


class KuaishouPhotoSubCommentSpider(scrapy.Spider):
    name = 'kuaishou_photo_sub_comment'
    custom_settings = {'ITEM_PIPELINES': {
        # 'KuaiShou.pipelines.KuaishouTestPipeline': 699,
        'KuaiShou.pipelines.KuaishouFilePipeline': 700,
        'KuaiShou.pipelines.KuaishouScrapyLogsPipeline': 701,
    }}
    settings = get_project_settings()

    url = 'https://live.kuaishou.com/graphql'
    query = {
        "operationName": "subCommentListQuery",
        "variables": {
            "photoId": "3x7qgrnnavc5tja",
            "rootCommentId": "158878958708",
            "pcursor": "0",
            "count": 20
        },
        "query": "query subCommentListQuery($photoId: String, $rootCommentId: String, $pcursor: String, $count: Int) {\n  subCommentList(photoId: $photoId, rootCommentId: $rootCommentId, pcursor: $pcursor, count: $count) {\n    pcursor\n    subCommentsList {\n      commentId\n      authorId\n      authorName\n      content\n      headurl\n      timestamp\n      authorEid\n      status\n      replyToUserName\n      replyTo\n      replyToEid\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
    headers = {
        'Content-Type': 'application/json'
    }


    def __init__(self, partitionIdx='0', useProxy='0', cookieManual='0', cookieIdx='0', *args, **kwargs):
        super(KuaishouPhotoSubCommentSpider, self).__init__(*args, **kwargs)
        self.partitionIdx = int(partitionIdx)
        self.useProxy = int(useProxy)
        self.cookieManual = int(cookieManual)
        self.cookieIdx = int(cookieIdx)

        self.saveFilePath = self.settings.get('FILE_PATH_PHOTO_SUB_COMMENT')

        self.mysql_host = self.settings.get('MYSQL_HOST')
        self.mysql_user = self.settings.get('MYSQL_USER')
        self.mysql_password = self.settings.get('MYSQL_PASSWORD')
        self.mysql_database = self.settings.get('MYSQL_DATABASE')
        self.mysql_kuaishou_scrapy_logs_tablename = self.settings.get('MYSQL_KUAISHOU_SCRAPY_LOGS_TABLENAME')
        logger.info('MySQLConn:host = %s,user = %s,db = %s' % (self.mysql_host, self.mysql_user, self.mysql_database))
        self.mysql_client = MySQLClient(host=self.mysql_host, user=self.mysql_user, password=self.mysql_password,
                                        dbname=self.mysql_database)


    def start_requests(self):
        # pcursor = "0"
        # photoId = "3x7qgrnnavc5tja"
        # rootCommentId = "158878958708"
        # curQuery = self.query
        # curQuery['variables']['pcursor'] = pcursor
        # curQuery['variables']['photoId'] = photoId
        # curQuery['variables']['rootCommentId'] = rootCommentId
        # yield scrapy.Request(self.url, headers=self.headers, body=json.dumps(curQuery), method='POST',
        #                      callback=self.parseSubCommentList,
        #                      meta={'photoId': photoId, 'rootCommentId': rootCommentId})

        # 配置kafka连接信息
        kafka_hosts = self.settings.get('KAFKA_HOSTS')
        zookeeper_hosts = self.settings.get('ZOOKEEPER_HOSTS')
        kafka_topic = self.settings.get('KAFKA_TOPIC_DATA')
        reset_offset_on_start = self.settings.get('RESET_OFFSET_ON_START')
        logger.info('kafka info, hosts:{}, topic:{}'.format(kafka_hosts, kafka_topic) + '\n')
        client = KafkaClient(hosts=kafka_hosts, zookeeper_hosts=zookeeper_hosts, broker_version='0.10.1.0')
        topic = client.topics[kafka_topic]
        partitions = topic.partitions
        # 配置kafka消费信息
        consumer = topic.get_simple_consumer(
            consumer_group=self.name,
            reset_offset_on_start=reset_offset_on_start,
            auto_commit_enable=True,
            partitions=[partitions[self.partitionIdx]]
        )

        # 获取被消费数据的偏移量和消费内容
        for message in consumer:
            try:
                if message is None:
                    continue
                # 信息分为message.offset, message.value
                msg_value = message.value.decode()
                # msg_value_dict = eval(msg_value)
                msg_value_dict = json.loads(msg_value)
                if msg_value_dict['spider_name'] != 'kuaishou_photo_comment':
                    continue
                pcursor = "0"
                photoId = msg_value_dict['photo_id']
                logger.info('photoId: ' + str(photoId))
                rootCommentId = msg_value_dict['commentId']
                curQuery = self.query
                curQuery['variables']['pcursor'] = pcursor
                curQuery['variables']['photoId'] = photoId
                curQuery['variables']['rootCommentId'] = rootCommentId
                time.sleep(random.choice(range(30, 50)))
                yield scrapy.Request(self.url, headers=self.headers, body=json.dumps(curQuery), method='POST',
                                     callback=self.parseSubCommentList,
                                     meta={'photoId': photoId, 'rootCommentId': rootCommentId})
            except Exception as e:
                logger.warning('Kafka message structure cannot be resolved :{}'.format(e))


    def parseSubCommentList(self, response):
        rlt_json = json.loads(response.text)
        photoId = response.meta['photoId']
        rootCommentId = response.meta['rootCommentId']

        if 'data' not in rlt_json:
            logger.info('data not in response, photoId: ' + str(photoId))
            return

        if rlt_json['data'] is None:
            logger.info('data is None, photoId: ' + str(photoId))
            return

        if 'subCommentList' not in rlt_json['data']:
            logger.info('subCommentList not in response data, photoId: ' + str(photoId))
            return

        if rlt_json['data']['subCommentList'] is None:
            logger.info('subCommentList is None, photoId: ' + str(photoId))
            return

        subCommentList = rlt_json['data']['subCommentList']
        if 'subCommentsList' not in subCommentList:
            logger.info('subCommentsList not in subCommentList, photoId: ' + str(photoId))
            return
        if subCommentList['subCommentsList'] is None:
            logger.info('subCommentsList is None, photoId: ' + str(photoId))
            return

        commentList = subCommentList['subCommentsList']
        for comment in commentList:
            commentInfo = KuaishouPhotoSubCommentItem()
            commentInfo['spider_name'] = self.name
            commentInfo['photo_id'] = photoId
            commentInfo['rootCommentId'] = rootCommentId
            commentInfo['commentId'] = comment['commentId']
            commentInfo['commentInfo'] = comment
            if self.isCommentIdExistTable(comment['commentId']):
                logger.info('comment id exist: ' + comment['commentId'])
            else:
                logger.info('add one comment record, photoId: ' + str(photoId))
                yield commentInfo

        pcursor = subCommentList['pcursor']
        logger.info('pcursor: ' + str(pcursor))
        if pcursor == 'no_more':
            return

        time.sleep(random.choice(range(30, 50)))
        curQuery = self.query
        curQuery['variables']['pcursor'] = pcursor
        curQuery['variables']['photoId'] = photoId
        curQuery['variables']['rootCommentId'] = rootCommentId
        yield scrapy.Request(self.url, headers=self.headers, body=json.dumps(curQuery), method='POST',
                             callback=self.parseSubCommentList,
                             meta={'photoId': photoId, 'rootCommentId': rootCommentId})


    def isCommentIdExistTable(self, commentId):
        sql = "select count(*) from kuaishou_scrapy_logs where item_id = '{}' and is_successed = 1 and item_type = '{}'".format(commentId, self.name)
        self.mysql_client.query(sql)
        d = self.mysql_client.fetchRow()
        rowCount = d[0]
        if rowCount > 0:
            return True
        else:
            return False


    def close(self):
        self.mysql_client.close()

