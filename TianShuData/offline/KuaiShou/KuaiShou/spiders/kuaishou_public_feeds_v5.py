# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouPhotoInfoItem
from KuaiShou.utils.signatureUtil import signatureUtil
from KuaiShou.utils.signatureArgUtil import signatureArgUtil


class KuaishouPublicFeedsV5Spider(scrapy.Spider):
    name = 'kuaishou_public_feeds_v5'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouTestPipeline': 699,
        # 'KuaiShou.pipelines.KuaishouKafkaPipeline': 700,
        # 'KuaiShou.pipelines.KuaishouScrapyLogsPipeline': 701
    }}
    settings = get_project_settings()

    preUrl = "http://api.gifshow.com/rest/n/feed/profile2?"
    mainUrlDict = {
        'mod': 'Xiaomi%20(Redmi%20Note%204)',
        'lon': '120.174727',
        'lat': '30.270966',
        'country_code': 'CN',
        'language': 'zh-cn',
        'lang': 'zh',
        'app': '0',
        'net': 'WIFI',
        'oc': 'UNKNOWN',
        'ud': '0',
        'c': 'ALI_CPD',
        'sys': 'ANDROID_5.1.1',
        'appver': '5.2.1.4686',
        'ver': '5.2',
        'ftt': '',
        'os': 'android',
        'did': 'ANDROID_982cbccac9d99034',
        'client_key': '3c2cd3f3',
        'privacy': 'public',
        'count': '30',
        'user_id': '252933812',
        'pcursor': '0',
    }
    sigPart = "&sig={}"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    sigUtil = signatureUtil()
    argUtil = signatureArgUtil()


    def __init__(self, partitionIdx='0', useProxy='0', *args, **kwargs):
        super(KuaishouPublicFeedsV5Spider, self).__init__(*args, **kwargs)
        self.partitionIdx = int(partitionIdx)
        self.useProxy = int(useProxy)


    def start_requests(self):
        # pcursor = '0'
        # user_id = '252933812'
        # mainUrl = self.getMainUrl({'user_id': user_id, 'pcursor': pcursor})
        # sig = self.sigUtil.getSig(mainUrl)
        # url = self.preUrl + mainUrl + self.sigPart.format(sig)
        # yield scrapy.Request(url, method='POST', headers=self.headers,
        #                      callback=self.parseFeedList, meta={'user_id': user_id})

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
                # msg_value_dicte) = eval(msg_value)
                msg_value_dict = json.loads(msg_value)
                if msg_value_dict['spider_name'] != 'kuaishou_user_seeds':
                    continue
                user_id = msg_value_dict['userId']
                logger.info('user_id: ' + str(user_id))
                pcursor = '0'
                mainUrl = self.getMainUrl({'user_id': user_id, 'pcursor': pcursor})
                sig = self.sigUtil.getSig(mainUrl)
                url = self.preUrl + mainUrl + self.sigPart.format(sig)
                time.sleep(random.choice(range(30, 60)))
                yield scrapy.Request(url, method='POST', headers=self.headers,
                                     callback=self.parseFeedList, meta={'user_id': user_id})
            except Exception as e:
                logger.warning('Kafka message structure cannot be resolved :{}'.format(e))


    def parseFeedList(self, response):
        # print(response.text)
        rlt_json = json.loads(response.text)
        user_id = response.meta['user_id']
        if 'result' not in rlt_json or rlt_json['result'] != 1:
            logger.info('wrong response: ' + response.text)
            return
        if 'feeds' not in rlt_json:
            logger.info('feeds not in response: ' + response.text)
            return
        for photo in rlt_json['feeds']:
            photoItem = KuaishouPhotoInfoItem()
            photoItem['spider_name'] = self.name
            photoItem['photo_id'] = photo['photo_id']
            photoItem['user_photo_info'] = photo
            logger.info('get one photo: ' + str(photo['photo_id']))
            yield photoItem

        if 'pcursor' in rlt_json:
            pcursor = rlt_json['pcursor']
            logger.info('pcursor: ' + str(pcursor))
            if pcursor is None or pcursor == 'no_more':
                return
            mainUrl = self.getMainUrl({'user_id': user_id, 'pcursor': pcursor})
            sig = self.sigUtil.getSig(mainUrl)
            url = self.preUrl + mainUrl + self.sigPart.format(sig)
            time.sleep(random.choice(range(30, 60)))
            yield scrapy.Request(url, method='POST', headers=self.headers,
                                 callback=self.parseFeedList, meta={'user_id': user_id})


    def getMainUrl(self, varDict):
        curDict = self.mainUrlDict
        curDict['mod'] = self.argUtil.getMod()
        curDict['lon'] = self.argUtil.getLon()
        curDict['lat'] = self.argUtil.getLat()
        curDict['user_id'] = varDict['user_id']
        curDict['pcursor'] = varDict['pcursor']
        curList = []
        for k, v in curDict.items():
            curList.append(str(k) + '=' + str(v))
        return '&'.join(curList)
