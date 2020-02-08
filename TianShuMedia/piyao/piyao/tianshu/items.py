# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TianshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class WeChatFakeArticleItem(scrapy.Item):
    spider_name = scrapy.Field()
    fake_alias = scrapy.Field()
    fake_id = scrapy.Field()
    fake_nickname = scrapy.Field()
    fake_head_img =scrapy.Field()
    msg_id = scrapy.Field()
    msg_cover = scrapy.Field()
    msg_digest = scrapy.Field()
    msg_link = scrapy.Field()
    msg_title = scrapy.Field()
    msg_update_time = scrapy.Field()
    msg_create_time = scrapy.Field()
    msg_content = scrapy.Field()
    msg_text = scrapy.Field()