# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KolItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class KuaiShouUserIterm(scrapy.Item):
    kwaiId = scrapy.Field() #快手号，需要用户自己设置，如果用户没设置，就没有这个字段
    user_id = scrapy.Field() #快手id，原始数据为int
    userId = scrapy.Field() #字符串，用于用户信息web页面定位
    user_name = scrapy.Field() #昵称
    user_sex = scrapy.Field() #性别，F-女,M-男
    user_text = scrapy.Field() #简介
    head_url = scrapy.Field() #头像地址
    cityCode = scrapy.Field() #邮编
    cityName = scrapy.Field() #城市
    constellation = scrapy.Field() #星座

    article_public = scrapy.Field() #int
    collect = scrapy.Field() #int
    fan = scrapy.Field() #int 粉丝数
    follow = scrapy.Field() #int 关注数
    like = scrapy.Field() #int
    moment = scrapy.Field() #int 动态数
    photo = scrapy.Field() #int 作品数
    photo_private = scrapy.Field() #int
    photo_public = scrapy.Field() #int

    update_time = scrapy.Field() #10位时间戳
    user_info_json = scrapy.Field()


class KuaiShouShopProductItem(scrapy.Item):
    user_id = scrapy.Field() #快手id
    itemId = scrapy.Field() #商品id
    addType = scrapy.Field() #int
    imageUrl = scrapy.Field() #商品图片url
    itemLinkUrl = scrapy.Field() #商品url
    itemTagList = scrapy.Field() #商品标签
    productPrice = scrapy.Field() #商品价格，单位：分
    productTitle = scrapy.Field() #商品标题
    showCoupon = scrapy.Field() #boolean
    sourceType = scrapy.Field() #int
    stock = scrapy.Field() #int
    updatetime = scrapy.Field() #13位时间戳
    volume = scrapy.Field() #int


class KuaiShouShopInfoItem(scrapy.Item):
    user_id = scrapy.Field()  #快手id
    #product_count = scrapy.Field()  #int 快手小店商品数量
    containTaoBao = scrapy.Field() #bool
    shopLogisticsScore = scrapy.Field() #double
    shopLogisticsScoreLevel = scrapy.Field() #double
    shopQualityScore = scrapy.Field() #double 商品质量
    shopQualityScoreLevel = scrapy.Field() #double
    shopServiceScore = scrapy.Field() #double 服务态度
    shopServiceScoreLevel = scrapy.Field() #double
    totalOrderPayCount = scrapy.Field() #int
    validCommentCount = scrapy.Field() #int


class TestCommentUserItem(scrapy.Item):
    authorId = scrapy.Field()
    authorName = scrapy.Field()
    headurl = scrapy.Field()
    authorEid = scrapy.Field()
