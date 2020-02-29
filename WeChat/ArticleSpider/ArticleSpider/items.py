# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KuaishoucomplementsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class WechatParamsItem(scrapy.Item):
    params_str=scrapy.Field()




class ArticalItem(scrapy.Item):
    # weChat_name =scrapy.Field()  #账号名称：新榜、央视新闻等
    # weChat_account=scrapy.Field()#微信账号：作为微信公众号自定义的字符组合唯一标识
    biz=scrapy.Field()  #公众号唯一标识，后面可与账号表关联，获得账号名称和微信账号
    title=scrapy.Field()         #标题
    SN=scrapy.Field()            #可唯一确定一篇文章
    type=scrapy.Field()             #文章类型
    publish_time=scrapy.Field()      #发布时间
    read_cnt_1day=scrapy.Field()   #一日阅读数
    read_cnt_3day=scrapy.Field() #三日阅读数
    read_cnt_7day=scrapy.Field()  #七日阅读数
    inWatching_cnt_1day=scrapy.Field()#一日在看数
    inWatching_cnt_3day=scrapy.Field()#三日在看数
    inWatching_cnt_7day=scrapy.Field() #七日在看数
    isOrigin_flag=scrapy.Field()         #是否原创，1表示原创，在文章内容页可以看到
    rank=scrapy.Field()                  #公众号文章列表排序字段
    author=scrapy.Field()                #作者
    summary=scrapy.Field()               #摘要，新榜给过来的excel中都为空
    article_url=scrapy.Field()          #文章url
    update_time=scrapy.Field()          #记录更新时间


# class ArticalUpdateItem(scrapy.Item):   #三日后文章更新
#     weChat_name =scrapy.Field()  #账号名称：新榜、央视新闻等
#     weChat_account=scrapy.Field()#微信账号：作为微信公众号自定义的字符组合唯一标识
#     SN=scrapy.Field()
#     three_day_read_cnt=scrapy.Field() #三日阅读数
#     three_day_inWatching_cnt=scrapy.Field()#三日在看数









class ContentItem(scrapy.Item):
    channel_id = scrapy.Field() #企鹅号、百家号
    account_id = scrapy.Field() #账号
    record_class = scrapy.Field() #content_info
    crawl_time = scrapy.Field() #采集时间:sa
    id = scrapy.Field() #tid
    title = scrapy.Field() #标题:t
    content_link = scrapy.Field() #内容链接:lk
    publish_time = scrapy.Field() #发布时间:pt
    publish_status = scrapy.Field() #发布状态:s #审核结果:0- 草稿 1- 审核中 2- 未通过 3- 已发布 4- 处理中 5- 处理失败 6- 管理员下线 7- 作者下线 8 待发布 9- 已删除 10- 作者删除 11-MCN 主账号下线
    audit_result = scrapy.Field() #审核结果
    read_count = scrapy.Field() #阅读数:vc
    comment_count = scrapy.Field() #评论数:c
    share_count = scrapy.Field() #分享数:fwd
    collect_count = scrapy.Field() #收藏数:fav
    recommend_count = scrapy.Field() #推荐数:rc
    like_count = scrapy.Field() #点赞数:dc
    download_count = scrapy.Field() #下载数:dwn
    finish_rate = scrapy.Field() #阅读/播放完成率，不抓


class UserInfoItem(scrapy.Item):
    userId = scrapy.Field()
    kwaiId = scrapy.Field()
    principalId = scrapy.Field()
    nickname = scrapy.Field()
    avatar = scrapy.Field()
    sex = scrapy.Field()
    description = scrapy.Field()
    constellation = scrapy.Field()
    cityName = scrapy.Field()
    fan = scrapy.Field()
    follow = scrapy.Field()
    photo = scrapy.Field()
    liked = scrapy.Field()
    open = scrapy.Field()
    playback = scrapy.Field()
    jsonStr = scrapy.Field()





