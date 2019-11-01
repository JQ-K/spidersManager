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
    channel_id = scrapy.Field() #百家号、企鹅号:cn
    account_id = scrapy.Field() #账号
    record_class = scrapy.Field() #content_info
    crawl_time = scrapy.Field() #采集时间:sa
    id = scrapy.Field() #tid
    title = scrapy.Field() #标题:t
    content_link = scrapy.Field() #内容链接:lk
    publish_time = scrapy.Field() #发布时间:pt
    publish_status = scrapy.Field() #发布状态:s
    audit_result = scrapy.Field() #审核结果:0- 草稿 1- 审核中 2- 未通过 3- 已发布 4- 处理中 5- 处理失败 6- 管理员下线 7- 作者下线 8 待发布 9- 已删除 10- 作者删除 11-MCN 主账号下线
    read_count = scrapy.Field() #阅读数:vc
    comment_count = scrapy.Field() #评论数:c
    share_count = scrapy.Field() #分享数:fwd
    collect_count = scrapy.Field() #收藏数:fav
    recommend_count = scrapy.Field() #推荐数:rc
    like_count = scrapy.Field() #点赞数:dc
    download_count = scrapy.Field() #下载数:dwn
    finish_rate = scrapy.Field() #阅读/播放完成率，不抓


class AccountItem(scrapy.Item):
    channel_id = scrapy.Field() #百家号、企鹅号:code
    account_id = scrapy.Field() #账号
    record_class = scrapy.Field() #channel_info
    crawl_time = scrapy.Field() #采集时间
    new_visit_count = scrapy.Field() #新增访问人数:ngc
    total_visit_count = scrapy.Field() #累计访问人数:tgc
    new_subscribe_count = scrapy.Field() #新增订阅人数:nfs
    total_subscribe_count = scrapy.Field() #总订阅人数:fs
    new_fans_count = scrapy.Field() #新增粉丝人数
    cancel_fans_count = scrapy.Field() #取消订阅/关注人数:cfs