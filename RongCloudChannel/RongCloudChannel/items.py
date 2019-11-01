# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RongcloudchannelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ContentItem(scrapy.Item):
    channel_id = scrapy.Field() #百家号、企鹅号。。。
    account_id = scrapy.Field() #账号
    record_class = scrapy.Field() #content_info
    crawl_time = scrapy.Field() #采集时间
    id = scrapy.Field()
    content_link = scrapy.Field() #内容链接
    publish_time = scrapy.Field() #发布时间
    publish_status = scrapy.Field() #发布状态
    audit_result = scrapy.Field() #审核结果
    read_count = scrapy.Field() #阅读数
    #play_count = scrapy.Field() #播放数
    comment_count = scrapy.Field() #评论数
    share_count = scrapy.Field() #分享数
    collect_count = scrapy.Field() #收藏数
    recommend_count = scrapy.Field() #推荐数
    like_count = scrapy.Field() #点赞数
    download_count = scrapy.Field() #下载数
    finish_rate = scrapy.Field() #阅读/播放完成率，不抓


class AccountItem(scrapy.Item):
    channel_id = scrapy.Field() #百家号、企鹅号
    account_id = scrapy.Field() #账号
    record_class = scrapy.Field() #channel_info
    crawl_time = scrapy.Field() #采集时间
    new_visit_count = scrapy.Field() #新增访问人数
    total_visit_count = scrapy.Field() #累计访问人数
    new_subscribe_count = scrapy.Field() #新增订阅人数
    total_subscribe_count = scrapy.Field() #总订阅人数
    new_fans_count = scrapy.Field() #新增粉丝人数
    cancel_fans_count = scrapy.Field() #取消订阅/关注人数