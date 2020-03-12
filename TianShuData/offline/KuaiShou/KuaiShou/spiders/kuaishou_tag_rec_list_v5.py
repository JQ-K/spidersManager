# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouTagRecItem
from KuaiShou.utils.signatureUtil import signatureUtil
from KuaiShou.utils.signatureArgUtil import signatureArgUtil


class KuaishouTagRecListV5Spider(scrapy.Spider):
    name = 'kuaishou_tag_rec_list_v5'
    custom_settings = {'ITEM_PIPELINES': {
        # 'KuaiShou.pipelines.KuaishouTestPipeline': 699,
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700,
        'KuaiShou.pipelines.KuaishouScrapyLogsPipeline': 701
    }}
    settings = get_project_settings()

    preUrl = "https://api.gifshow.com/rest/n/search/tagRecommend?"
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
        'pcursor': '0'
    }
    sigPart = "&sig={}"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    sigUtil = signatureUtil()
    argUtil = signatureArgUtil()


    def __init__(self, partitionIdx='0', useProxy='0', *args, **kwargs):
        super(KuaishouTagRecListV5Spider, self).__init__(*args, **kwargs)
        self.partitionIdx = int(partitionIdx)
        self.useProxy = int(useProxy)


    def start_requests(self):
        mainUrl = self.getMainUrl({'pcursor': '0'})
        sig = self.sigUtil.getSig(mainUrl)
        url = self.preUrl + mainUrl + self.sigPart.format(sig)
        yield scrapy.Request(url, method='POST', headers=self.headers,
                             callback=self.parseRecList)


    def parseRecList(self, response):
        # print(response.text)
        rlt_json = json.loads(response.text)
        if 'result' not in rlt_json or rlt_json['result'] != 1:
            logger.info('wrong response: ' + response.text)
            return
        if 'tags' not in rlt_json:
            logger.info('tags not in response: ' + response.text)
            return
        for tagInfo in rlt_json['tags']:
            if 'tag' not in tagInfo:
                logger.info('tag not in tagInfo')
                continue
            curTag = tagInfo['tag']
            tagItem = KuaishouTagRecItem()
            tagItem['spider_name'] = self.name
            tagItem['tagId'] = curTag['id']
            tagItem['tagName'] = curTag['name']
            tagItem['tagRecInfo'] = tagInfo
            logger.info('get one tag: ' + str(tagItem['tagId']))
            yield tagItem

        if 'pcursor' in rlt_json:
            pcursor = rlt_json['pcursor']
            logger.info('pcursor: ' + str(pcursor))
            if pcursor is None or pcursor == 'no_more':
                return
            mainUrl = self.getMainUrl({'pcursor': pcursor})
            sig = self.sigUtil.getSig(mainUrl)
            url = self.preUrl + mainUrl + self.sigPart.format(sig)
            time.sleep(random.choice(range(30, 60)))
            yield scrapy.Request(url, method='POST', headers=self.headers,
                                 callback=self.parseRecList)


    def getMainUrl(self, varDict):
        curDict = self.mainUrlDict
        curDict['mod'] = self.argUtil.getMod()
        curDict['lon'] = self.argUtil.getLon()
        curDict['lat'] = self.argUtil.getLat()
        curDict['pcursor'] = varDict['pcursor']
        curList = []
        for k, v in curDict.items():
            curList.append(str(k) + '=' + str(v))
        return '&'.join(curList)

