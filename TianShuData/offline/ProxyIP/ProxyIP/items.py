# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxyipItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class FreeProxyIPItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    url_name = scrapy.Field()
    proxy = scrapy.Field()