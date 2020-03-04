# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouTagNewPhotoItem
from KuaiShou.utils.signatureUtil import signatureUtil
from KuaiShou.utils.signatureArgUtil import signatureArgUtil


class KuaishouTagFeedNewV5Spider(scrapy.Spider):
    name = 'kuaishou_tag_feed_new_v5'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouTestPipeline': 699,
        # 'KuaiShou.pipelines.KuaishouKafkaPipeline': 700,
        # 'KuaiShou.pipelines.KuaishouScrapyLogsPipeline': 701
    }}
    settings = get_project_settings()

    preUrl = "https://api.gifshow.com/rest/n/tag/text/feed/recent?"
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
        'pcursor': '0',
    }
    sigPart = "&sig={}"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    sigUtil = signatureUtil()
    argUtil = signatureArgUtil()

    def __init__(self, partitionIdx='0', useProxy='0', *args, **kwargs):
        super(KuaishouTagFeedNewV5Spider, self).__init__(*args, **kwargs)
        self.partitionIdx = int(partitionIdx)
        self.useProxy = int(useProxy)


    def start_requests(self):
        tagId = 17842124
        tagName = '我的快手影集'
        mainUrl = self.getMainUrl({'pcursor': '0', 'tagName': tagName})
        sig = self.sigUtil.getSig(mainUrl)
        url = self.preUrl + mainUrl + self.sigPart.format(sig)
        yield scrapy.Request(url, method='POST', headers=self.headers,
                             callback=self.parseTagPhotoInfo,
                             meta={'tagId': tagId, 'tagName': tagName})


    def parseTagPhotoInfo(self, response):
        # print(response.text)
        rlt_json = json.loads(response.text)
        if 'result' not in rlt_json or rlt_json['result'] != 1:
            logger.info('wrong response: ' + response.text)
            return
        if 'feeds' not in response.text:
            logger.info('feeds not in response: ' + response.text)

        tagId = response.meta['tagId']
        tagName = response.meta['tagName']

        for photoInfo in rlt_json['feeds']:
            if 'photo_id' not in photoInfo:
                continue
            photoItem = KuaishouTagNewPhotoItem()
            photoItem['spider_name'] = self.name
            photoItem['tagId'] = tagId
            photoItem['tagName'] = tagName
            photoItem['photo_id'] = photoInfo['photo_id']
            photoItem['photoInfo'] = photoInfo
            yield photoItem

        if 'pcursor' in rlt_json:
            pcursor = rlt_json['pcursor']
            logger.info('pcursor: ' + str(pcursor))
            if pcursor == 'no_more':
                return
            mainUrl = self.getMainUrl({'pcursor': pcursor, 'tagName': tagName})
            sig = self.sigUtil.getSig(mainUrl)
            url = self.preUrl + mainUrl + self.sigPart.format(sig)
            time.sleep(random.choice(range(30, 60)))
            yield scrapy.Request(url, method='POST', headers=self.headers,
                                 callback=self.parseTagPhotoInfo,
                                 meta={'tagId': tagId, 'tagName': tagName})


    def getMainUrl(self, varDict):
        curDict = self.mainUrlDict
        curDict['mod'] = self.argUtil.getMod()
        curDict['lon'] = self.argUtil.getLon()
        curDict['lat'] = self.argUtil.getLat()
        curDict['pcursor'] = varDict['pcursor']
        curDict['tagName'] = varDict['tagName']
        curList = []
        for k, v in curDict.items():
            curList.append(str(k) + '=' + str(v))
        return '&'.join(curList)
