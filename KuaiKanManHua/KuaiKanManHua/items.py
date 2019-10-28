# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KuaikanmanhuaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class UserItem(scrapy.Item):
    user_id = scrapy.Field()
    pic_url = scrapy.Field()
    nickname = scrapy.Field()
    sign_text = scrapy.Field()


