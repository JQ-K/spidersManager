# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouTagInfoItem
from KuaiShou.utils.signatureUtil import signatureUtil
from KuaiShou.utils.signatureArgUtil import signatureArgUtil


class KuaishouTagInfoV5Spider(scrapy.Spider):
    name = 'kuaishou_tag_info_v5'
    custom_settings = {'ITEM_PIPELINES': {
        # 'KuaiShou.pipelines.KuaishouTestPipeline': 699,
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700,
        'KuaiShou.pipelines.KuaishouScrapyLogsPipeline': 701
    }}
    settings = get_project_settings()

    preUrl = "https://api.gifshow.com/rest/n/tag/text/info?"
    mainUrlDict = {
        'mod': 'OPPO(OPPO%20R11)',
        'lon': '120.174975',
        'lat': '30.270968',
        'country_code': 'CN',
        'language': 'zh-cn',
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
        'tagName': '快影片场',
    }
    sigPart = "&sig={}"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    sigUtil = signatureUtil()
    argUtil = signatureArgUtil()


    def __init__(self, partitionIdx='0', useProxy='0', *args, **kwargs):
        super(KuaishouTagInfoV5Spider, self).__init__(*args, **kwargs)
        self.partitionIdx = int(partitionIdx)
        self.useProxy = int(useProxy)


    def start_requests(self):
        # tagId = 17842124
        # tagName = '我的快手影集'
        # mainUrl = self.getMainUrl({'tagName': tagName})
        # sig = self.sigUtil.getSig(mainUrl)
        # url = self.preUrl + mainUrl + self.sigPart.format(sig)
        # yield scrapy.Request(url, method='POST', headers=self.headers,
        #                      callback=self.parseTagInfo,
        #                      meta={'tagId': tagId, 'tagName': tagName})

        # 配置kafka连接信息
        kafka_hosts = self.settings.get('KAFKA_HOSTS')
        zookeeper_hosts = self.settings.get('ZOOKEEPER_HOSTS')
        # kafka_topic = self.settings.get('KAFKA_TOPIC_DATA')
        kafka_topic = self.settings.get('KAFKA_TOPIC_DATA_TAG')   #该topic用于话题相关爬虫测试
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
                if msg_value_dict['spider_name'] != 'kuaishou_tag_rec_list_v5':
                    continue
                tagId = msg_value_dict['tagId']
                tagName = msg_value_dict['tagName']
                logger.info('tag_id: ' + str(tagId))
                time.sleep(random.choice(range(30, 60)))

                mainUrl = self.getMainUrl({'tagName': tagName})
                sig = self.sigUtil.getSig(mainUrl)
                url = self.preUrl + mainUrl + self.sigPart.format(sig)
                yield scrapy.Request(url, method='POST', headers=self.headers,
                                     callback=self.parseTagInfo,
                                     meta={'tagId': tagId, 'tagName': tagName})
            except Exception as e:
                logger.warning('Kafka message structure cannot be resolved :{}'.format(e))


    def parseTagInfo(self, response):
        # print(response.text)
        rlt_json = json.loads(response.text)
        if 'result' not in rlt_json or rlt_json['result'] != 1:
            logger.info('wrong response: ' + response.text)
            return
        if 'tagInfo' not in rlt_json:
            logger.info('tagInfo not in response: ' + response.text)
            return
        tagId = response.meta['tagId']
        tagName = response.meta['tagName']
        tagItem = KuaishouTagInfoItem()
        tagItem['spider_name'] = self.name
        tagItem['tagId'] = tagId
        tagItem['tagName'] = tagName
        tagItem['tagInfo'] = rlt_json['tagInfo']
        logger.info('get one tag: ' + str(tagItem['tagId']))
        yield tagItem


    def getMainUrl(self, varDict):
        curDict = self.mainUrlDict
        curDict['mod'] = self.argUtil.getMod()
        curDict['lon'] = self.argUtil.getLon()
        curDict['lat'] = self.argUtil.getLat()
        curDict['tagName'] = varDict['tagName']
        curList = []
        for k, v in curDict.items():
            curList.append(str(k) + '=' + str(v))
        return '&'.join(curList)
