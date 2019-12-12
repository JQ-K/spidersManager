# -*- coding: utf-8 -*-
import scrapy
import json
import re

from RongCloudChannel.utils.targetIdUtil import *
from RongCloudChannel.items import *
from RongCloudChannel.utils import dateUtil


class GongzhonghaoSpider(scrapy.Spider):
    name = 'GongZhongHao'
    channel_id = '公众号'

    articleUrl = "https://mp.weixin.qq.com/s/{}"


    def start_requests(self):
        targetId = "oZd8wfgltezqaZJAgJWHxQ"
        yield scrapy.Request(self.articleUrl.format(targetId), method='GET',
                             callback=self.parseArticalPage, meta={'targetId': targetId})


    def parseArticalPage(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        targetId = response.meta['targetId']

        contentItem = ContentItem()
        contentItem['channel_id'] = self.channel_id
        contentItem['record_class'] = 'content_info'

        link = response.url
        curTime = dateUtil.getCurDate()
        contentItem['crawl_time'] = curTime
        contentItem['id'] = targetId
        contentItem['content_link'] = link

        titleList = response.xpath('//h2[@class="rich_media_title"]/text()').extract()
        if len(titleList) == 1:
            title = titleList[0].strip()
            contentItem['title'] = title

        authorNameList = response.xpath('//a[@id="js_name"]/text()').extract()
        if len(authorNameList) == 1:
            authorName = authorNameList[0].strip()
            contentItem['account_id'] = authorName

        pubDateResult = re.search(r'",o="\d{4}-\d{2}-\d{2}', response.text)
        if pubDateResult is not None:
            pubDate = pubDateResult.group(0).strip().replace('",o="', "")
            pubDate += " 00:00:00"
            contentItem['publish_time'] = pubDate

        #print(contentItem)
        yield contentItem

