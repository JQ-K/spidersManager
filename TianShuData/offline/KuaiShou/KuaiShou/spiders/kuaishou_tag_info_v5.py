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
        'KuaiShou.pipelines.KuaishouTestPipeline': 699,
        # 'KuaiShou.pipelines.KuaishouKafkaPipeline': 700,
        # 'KuaiShou.pipelines.KuaishouScrapyLogsPipeline': 701
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
        tagId = 17842124
        tagName = '我的快手影集'
        mainUrl = self.getMainUrl({'tagName': tagName})
        sig = self.sigUtil.getSig(mainUrl)
        url = self.preUrl + mainUrl + self.sigPart.format(sig)
        yield scrapy.Request(url, method='POST', headers=self.headers,
                             callback=self.parseTagInfo,
                             meta={'tagId': tagId, 'tagName': tagName})


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

