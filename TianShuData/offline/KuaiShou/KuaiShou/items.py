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


class KuxuanKolUserItem(scrapy.Item):
    # define the fields for your item here like:
    spider_name = scrapy.Field()
    id = scrapy.Field()
    userId = scrapy.Field()
    kwaiId = scrapy.Field()
    principalId = scrapy.Field()
    cityName = scrapy.Field()
    fan = scrapy.Field()
    headurl = scrapy.Field()
    ku_value = scrapy.Field()
    photo = scrapy.Field()
    user_name = scrapy.Field()
    user_sex = scrapy.Field()
    user_text = scrapy.Field()
    avg_view_count = scrapy.Field()
    avg_like_count = scrapy.Field()
    avg_comment_count = scrapy.Field()
    categorys = scrapy.Field()


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


class KuaishouUserPhotoInfoIterm(scrapy.Item):
    spider_name = scrapy.Field()
    spider_datetime = scrapy.Field()
    photo_id = scrapy.Field()
    user_photo_info = scrapy.Field()


class KuaishouPhotoCommentInfoIterm(scrapy.Item):
    spider_name = scrapy.Field()
    spider_datetime = scrapy.Field()
    photo_id = scrapy.Field()
    photo_comment_info = scrapy.Field()


class KuaishouShopInfoIterm(scrapy.Item):
    spider_name = scrapy.Field()
    spider_datetime = scrapy.Field()
    userId = scrapy.Field()
    shopInfo = scrapy.Field()


class KuaishouShopProductItem(scrapy.Item):
    spider_name = scrapy.Field()
    spider_datetime = scrapy.Field()
    userId = scrapy.Field()
    productId = scrapy.Field()
    productInfo = scrapy.Field()


class KuaishouShopProductDetailItem(scrapy.Item):
    spider_name = scrapy.Field()
    spider_datetime = scrapy.Field()
    productId = scrapy.Field()
    productDetail = scrapy.Field()


class KuaishouShopProductCommentItem(scrapy.Item):
    spider_name = scrapy.Field()
    spider_datetime = scrapy.Field()
    productId = scrapy.Field()
    commentId = scrapy.Field()
    productComment = scrapy.Field()

