# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import sys



class SinanewsItem(scrapy.Item):
    parentTitle = scrapy.Field()
    parentUrls = scrapy.Field()

    subTitle = scrapy.Field()
    subUrls = scrapy.Field()

    subFilename = scrapy.Field()


    sonUrls = scrapy.Field()
    head = scrapy.Field()

    content = scrapy.Field()
