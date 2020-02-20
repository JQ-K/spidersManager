# -*- coding: utf-8 -*-
import scrapy
import time
import random
import re
import json

from loguru import logger
from NewsCheck.items import NewsInfo


class DazhechengshiSpider(scrapy.Spider):
    name = 'DaZheChengShi'
    channel = '大浙网-城事板块'

    urlList = ['http://zj.qq.com/l/news/list20130328165910.htm',
               'http://zj.qq.com/l/news/list20130328165910_2.htm']

    custom_settings = {'ITEM_PIPELINES': {
        'NewsCheck.pipelines.NewscheckPipeline': 700,
        'NewsCheck.pipelines.KuaishouKafkaPipeline': 701
    }}


    def start_requests(self):
        for curUrl in self.urlList:
            time.sleep(random.choice(range(3,6)))
            yield scrapy.Request(curUrl, callback=self.parseList)


    def parseList(self, response):
        href_list = response.xpath('//a[@target="_blank"]/@href').extract()
        rlt_href_list = []
        for href in href_list:
            idx = href.find('http://zj.qq.com/a/')
            if 0 == idx:
                rlt_href_list.append(href)

        # 获得单篇文本的标题和正文
        for useful_href in rlt_href_list:
            time.sleep(random.choice(range(2,4)))
            yield scrapy.Request(useful_href, callback=self.parseNews, meta={'url': useful_href})

        next_page_list = response.xpath('//a[@class="f12"]/@href').extract()

        if len(next_page_list) == 4:
            time.sleep(random.choice(range(3,6)))
            yield scrapy.Request(next_page_list[1], callback=self.parseList)


    def parseNews(self, response):
        url = response.meta['url']
        title = ''
        try:
            title_list = response.xpath('//title/text()').extract()
            title += title_list[0]
        except:
            logger.info('获取标题出错：' + url)

        p_list = response.xpath('//p/text()').extract()
        if len(p_list) == 0:
            p_list = response.xpath('//P/text()').extract()

        if len(p_list) == 0:
            logger.info('正文为空：' + url)
        else:
            for i, txt in enumerate(p_list):
                pure_txt = re.sub(r'\r\n|\n|\t', "", txt)
                p_list[i] = pure_txt

        vid = url.split('/')[-1].split('.')[0]

        pubTime = ''
        pubTime_list = response.xpath('//span[@class="a_time"]/text()').extract()
        if len(pubTime_list) == 0:
            pubTime_list = response.xpath('//span[@class="article-time"]/text()').extract()
        if len(pubTime_list) > 0:
            pubTime += pubTime_list[0]

        newsInfo = NewsInfo()
        newsInfo['channel'] = self.channel
        newsInfo['id'] = str(vid)
        newsInfo['url'] = url
        newsInfo['title'] = title
        newsInfo['content'] = ''.join(p_list)
        newsInfo['publish_time'] = pubTime

        cmtList = re.findall(r"cmt_id = \d+;", response.text)
        if len(cmtList) == 1:
            cmtId = cmtList[0].replace('cmt_id = ', '').replace(';', '')
            time.sleep(random.choice(range(1,3)))
            yield scrapy.Request('https://coral.qq.com/article/{}/commentnum'.format(cmtId),
                                 callback=self.parseCmt, meta={'item': newsInfo})


    def parseCmt(self, response):
        newsInfo = response.meta['item']
        rltJson = json.loads(response.text)
        if rltJson['errCode'] == 0:
            if 'data' in rltJson:
                if 'commentnum' in rltJson['data']:
                    newsInfo['comment_count'] = self.getIntValue(rltJson['data']['commentnum'])
        yield newsInfo


    def getIntValue(self, val):
        try:
            rlt = int(val)
        except:
            rlt = 0
        return rlt

