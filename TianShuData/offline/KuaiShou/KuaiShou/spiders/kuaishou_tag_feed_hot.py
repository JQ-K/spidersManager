# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouTagHotPhotoItem


class KuaishouTagFeedHotSpider(scrapy.Spider):
    name = 'kuaishou_tag_feed_hot'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouTestPipeline': 699,
        # 'KuaiShou.pipelines.KuaishouKafkaPipeline': 700,
        # 'KuaiShou.pipelines.KuaishouScrapyLogsPipeline': 701
    }}
    settings = get_project_settings()


    def __init__(self, partitionIdx='0', useProxy='0', *args, **kwargs):
        super(KuaishouTagFeedHotSpider, self).__init__(*args, **kwargs)
        self.partitionIdx = int(partitionIdx)
        self.useProxy = int(useProxy)


    def start_requests(self):
        tagId = 17842124
        tagName = '我的快手影集'
        url = 'https://apis2.ksapisrv.com/rest/n/tag/text/feed/hot?lon=120.2925583040106&kpf=IPHONE&net=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8_5&appver=6.10.1.1242&isp=&c=a&mod=iPhone8%2C1&sys=ios10.3.3&sh=1334&ver=6.10&lat=30.36317252037759&did=F125510A-A382-4D14-A2C4-F3DC7B50EB9C&kpn=KUAISHOU&ud=1577168521&sw=750&browseType=1&egid=DFP91F44D054C8155496C8B8CCCA555249D51D7260F5055719A25373287920E1'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        bodyText = '__NS_sig3=2207127078c641580fb18797c843f6eaa728cd92dd&__NStokensig=0febaf40efa0e43775a69a10c23f6be8a6ed16168098b481ecea6f948880d24a&client_key=56c3713c&country_code=cn&kuaishou.api_st=Cg9rdWFpc2hvdS5hcGkuc3QSoAGqw2YICmh95HWZ2sM02WjD47ZnK8INJ6w1qkKm-7rmxyAWMU1MYhOFyN-SzPVLhVr-shuV1gvbMy31ImIycB7JvRBKjyvgz6GrRrHAZt8dmHUcDvj5rE6ZwRB2N0vkPn_juX4Q363mANNh-xCmGfz4hQszffqFIEy8Jeoe6EgMgm8kF1bmWMV3S5ScbOJPDRT7a2Au6DtbIGzbveEX4--8GhIgH75JxRxHRbwpYsUawhz3w5UiIGIRxJAIjYpXUqDPAdqSJMKXqCbWJMan2w6FeOmV00A6KAUwAQ&language=zh-Hans-CN%3Bq%3D1&sig=f2aec0d3f2159aab16a1da657c6bf2f4&tagName={}&tagSource=1&token=4193f61b40a44724aab42f483a5b4a0d-1577168521'

        yield scrapy.Request(url, method='POST', headers=headers, body=bodyText.format(tagName),
                             callback=self.parseTagPhotoInfo, meta={'tagId': tagId, 'tagName': tagName})


    def parseTagPhotoInfo(self, response):
        print(response.text)
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
            photoItem = KuaishouTagHotPhotoItem()
            photoItem['spider_name'] = self.name
            photoItem['tagId'] = tagId
            photoItem['tagName'] = tagName
            photoItem['photo_id'] = photoInfo['photo_id']
            photoItem['photoInfo'] = photoInfo
            yield photoItem

        if 'pcursor' in rlt_json:
            pcursor = rlt_json['pcursor']
            logger.info('pcursor: ' + str(pcursor))
            # yield scrapy.Request...


