# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KuaishouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class KuaishouUserInfoIterm(scrapy.Item):
    spider_name = scrapy.Field()
    userId = scrapy.Field()
    kwaiId = scrapy.Field()
    principalId = scrapy.Field()
    constellation  = scrapy.Field()
    cityName = scrapy.Field()
    fan = scrapy.Field()
    follow = scrapy.Field()
    photo = scrapy.Field()
    liked = scrapy.Field()
    open = scrapy.Field()
    playback = scrapy.Field()
    nickname = scrapy.Field()
    avatar = scrapy.Field()
    sex = scrapy.Field()
    description = scrapy.Field()

class KuaishouCookieInfoItem(scrapy.Item):
    spider_name = scrapy.Field()
    kuaishou_live_bfb1s = scrapy.Field()
    clientid = scrapy.Field()
    did = scrapy.Field()
    client_key = scrapy.Field()
    didv = scrapy.Field()