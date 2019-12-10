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
    name = scrapy.Field()
    id = scrapy.Field()
    user_id = scrapy.Field()
    kwaiId = scrapy.Field()
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

class KuaishouCookieInfoItem(scrapy.Item):
    name = scrapy.Field()
    kuaishou_live_bfb1s = scrapy.Field()
    clientid = scrapy.Field()
    did = scrapy.Field()
    client_key = scrapy.Field()
    didv = scrapy.Field()

class KuaishouUserInfoIterm(scrapy.Item):
    name = scrapy.Field()
    user_info = scrapy.Field()

class KuaishouUserPhotoInfoIterm(scrapy.Item):
    name = scrapy.Field()
    user_photo_info = scrapy.Field()

class KuaishouPhotoCommentInfoIterm(scrapy.Item):
    name = scrapy.Field()
    photo_id = scrapy.Field()
    photo_comment_info = scrapy.Field()

### old
# class KuaiShouUserIterm(scrapy.Item):
#     kwaiId = scrapy.Field() #快手号，需要用户自己设置，如果用户没设置，就没有这个字段
#     user_id = scrapy.Field() #快手id，原始数据为int
#     userId = scrapy.Field() #字符串，用于用户信息web页面定位
#     user_name = scrapy.Field() #昵称
#     user_sex = scrapy.Field() #性别，F-女,M-男
#     user_text = scrapy.Field() #简介
#     head_url = scrapy.Field() #头像地址
#     cityCode = scrapy.Field() #邮编
#     cityName = scrapy.Field() #城市
#     constellation = scrapy.Field() #星座
#
#     article_public = scrapy.Field() #int，改成str
#     collect = scrapy.Field() #int，改成str
#     fan = scrapy.Field() #int 粉丝数，改成str
#     follow = scrapy.Field() #int 关注数，改成str
#     like = scrapy.Field() #int，改成str
#     moment = scrapy.Field() #int 动态数，改成str
#     photo = scrapy.Field() #int 作品数，改成str
#     photo_private = scrapy.Field() #int，改成str
#     photo_public = scrapy.Field() #int，改成str
#
#     update_time = scrapy.Field() #10位时间戳
#     user_info_json = scrapy.Field()
#
#
# class KuaiShouShopProductItem(scrapy.Item):
#     user_id = scrapy.Field() #快手id
#     itemId = scrapy.Field() #商品id
#     addType = scrapy.Field() #int
#     imageUrl = scrapy.Field() #商品图片url
#     itemLinkUrl = scrapy.Field() #商品url
#     itemTagList = scrapy.Field() #商品标签
#     productPrice = scrapy.Field() #商品价格，单位：分
#     productTitle = scrapy.Field() #商品标题
#     showCoupon = scrapy.Field() #boolean
#     sourceType = scrapy.Field() #int
#     stock = scrapy.Field() #int
#     updatetime = scrapy.Field() #13位时间戳
#     volume = scrapy.Field() #int
#
#     itemFrom = scrapy.Field() #商品来源，如淘宝等
#     saleCount = scrapy.Field() #卖出数量
#
#
#
# class KuaiShouShopInfoItem(scrapy.Item):
#     user_id = scrapy.Field()  #快手id
#     #product_count = scrapy.Field()  #int 快手小店商品数量
#     containTaoBao = scrapy.Field() #bool
#     shopLogisticsScore = scrapy.Field() #double
#     shopLogisticsScoreLevel = scrapy.Field() #double
#     shopQualityScore = scrapy.Field() #double 商品质量
#     shopQualityScoreLevel = scrapy.Field() #double
#     shopServiceScore = scrapy.Field() #double 服务态度
#     shopServiceScoreLevel = scrapy.Field() #double
#     totalOrderPayCount = scrapy.Field() #int
#     validCommentCount = scrapy.Field() #int
