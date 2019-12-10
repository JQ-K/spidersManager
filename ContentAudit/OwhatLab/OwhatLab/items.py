# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OwhatLabItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


#用户，包括发帖和回帖用户
class OwhatLabUserIterm(scrapy.Item):
    user_id = scrapy.Field()  # 用户id
    nick_name = scrapy.Field()  # 昵称
    pic_url = scrapy.Field()  # t头像图片url
    update_time = scrapy.Field()  # 10位时间戳



#商品
class OwhatLabShopProductItem(scrapy.Item):
    shop_id = scrapy.Field()  # 商品id
    publish_time = scrapy.Field()  # 商品发布时间，13位时间戳
    title = scrapy.Field()  # 商品名称
    shop_imgurl = scrapy.Field()  # 商品封面图片url
    column_id = scrapy.Field() #商品所属频道id
    column_name = scrapy.Field() #商品所属频道名称
    shop_max_price = scrapy.Field()  # 商品最大价格，单位：元
    shop_min_price = scrapy.Field()  # 商品最小价格，单位：元
    shop_sale_total = scrapy.Field()  # 商品已销售量

    publisher_id  = scrapy.Field()#商品发布作者id
    publisher_name = scrapy.Field()#商品发布作者昵称
    publisher_pic_url = scrapy.Field() #商品发布作者头像url
    update_time = scrapy.Field()  # 13位时间戳


# 文章
class OwhatLabArticleItem(scrapy.Item):
    article_id = scrapy.Field() #文章id
    publish_time = scrapy.Field()  # 文章发布时间，13位时间戳
    title = scrapy.Field()  # 文章标题
    article_imgurl = scrapy.Field() #文章封面图片url
    column_id =  scrapy.Field() #文章所属频道id
    column_name = scrapy.Field() #文章所属频道名称

    publisher_id = scrapy.Field() #文章发布作者id
    publisher_name = scrapy.Field() #文章发布作者昵称
    publisher_pic_url = scrapy.Field()  # 文章发布作者头像url
    update_time = scrapy.Field() #13位时间戳


