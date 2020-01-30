# -*- coding: utf-8 -*-
import scrapy
import random, time, datetime
import json
import os,sys

from loguru import logger
from bs4 import BeautifulSoup
from scrapy.utils.project import get_project_settings

from tianshu.items import WeChatFakeArticleItem
from tianshu.utils import get_project_configs, str_to_bool
from tianshu.utils.dt import compute_time_interval
from tianshu.utils.notice import DingDingMsg


class WechatFakeSpider(scrapy.Spider):
    name = 'wechatfake'
    # allowed_domains = ['mp.weixin.qq.com']
    # start_urls = ['http://mp.weixin.qq.com/']
    custom_settings = {'ITEM_PIPELINES': {
        # 'tianshu.pipelines.TianShuKafkaPipeline': 700,
        'tianshu.pipelines.TianShuPiYaoKafkaPipeline': 701
    }}
    settings = get_project_settings()
    token = settings.get('WECHAT_FAKE_TOKEN')
    cookie = settings.get('WECHAT_FAKE_COOKIE')
    stockdays = settings.get('WECHAT_FAKE_STOCKDAYS')

    dev = settings.get('DEV')
    notice_json = get_project_configs('notice.json')[dev]
    at_mobiles = notice_json["at_mobiles"]
    ddmsg_notify = str_to_bool(notice_json["ddmsg_notify"])
    is_at_all = str_to_bool(notice_json["is_at_all"])
    notice_app = DingDingMsg(at_mobiles, is_at_all, ddmsg_notify)

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    def start_requests(self):
        fakes_json = get_project_configs('account.json')
        for fake_nickname, fake_alias in fakes_json.items():
            start_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={token}&lang=zh_CN&f=json&ajax=1&random={random}&query={query}&begin={begin}&count={count}'.format(
                random=random.random(), token=self.token, query=fake_alias, begin=0, count=5)
            yield scrapy.Request(start_url, headers=self.headers, callback=self.search_fake_biz, method='GET',
                                 dont_filter=True, meta={'fake_nickname':fake_nickname,'fake_alias':fake_alias})
            # time.sleep(random.randint(25,30))

    def search_fake_biz(self, response):
        time.sleep(random.randint(30, 60))
        rep_json = json.loads(response.text)
        fake_nickname = response.meta['fake_nickname']
        fake_alias = response.meta['fake_alias']
        if rep_json['base_resp']['ret'] != 0:
            logger.error(rep_json)
            self.notice_app.send(
                "Project:{}-{}-{},Error:{}".format(self.name, fake_nickname, fake_alias, str(rep_json)))
            time.sleep(3600)
            return
        if rep_json['list'] == []:
            logger.warning('Project:{}-{}-{},list is null!'.format(self.name, fake_nickname, fake_alias))
            return
        fake_info = rep_json['list'][0]
        alias = fake_info['alias']
        if fake_alias.lower() != alias.lower():
            return
        fake_id = fake_info['fakeid']
        nickname = fake_info['nickname']
        count = 5
        pagenum = 1
        begin = (pagenum - 1) * 5
        logger.info('Fake:{}-{}, Page:{}'.format(nickname, alias, pagenum))
        appmsg_list_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token={token}&lang=zh_CN&f=json&%E2%80%A65&action=list_ex&begin={begin}&count={count}&query={query}&fakeid={fakeid}&type=9'.format(
            token=self.token, fakeid=fake_id, begin=begin, count=count, query='')
        yield scrapy.Request(appmsg_list_url, headers=self.headers, callback=self.fake_page_down, method='GET',
                             dont_filter=True, meta={'fake_info': fake_info,'pagenum':pagenum,'count':count})


    def fake_page_down(self,response):
        time.sleep(random.randint(10, 15))
        count = response.meta['count']
        pagenum = response.meta['pagenum']
        fake_info = response.meta['fake_info']
        fake_id = fake_info['fakeid']
        nickname = fake_info['nickname']
        alias = fake_info['alias']
        round_head_img = fake_info['round_head_img']
        fake_articles_url_json = json.loads(response.text)
        if fake_articles_url_json['base_resp']['ret'] != 0:
            logger.error(fake_articles_url_json)
            self.notice_app.send("Project:{}-{}-{},Error:{}".format(self.name, nickname, alias,
                                                                    str(fake_articles_url_json)))
            return
        fake_msg_cnt = fake_articles_url_json['app_msg_cnt']
        fake_msg_list = fake_articles_url_json['app_msg_list']
        for fake_msg in fake_msg_list:
            msg_link = fake_msg['link']
            msg_update_time = fake_msg['update_time']
            msg_create_time = fake_msg['create_time']
            # 判断时间是否在指定时间后
            today = datetime.datetime.now()
            oneday = datetime.timedelta(days=self.stockdays)
            dtBefore = today - oneday
            dtBefore_str = dtBefore.strftime("%Y-%m-%d")
            dt_time_limit = "{} 00:00:00".format(dtBefore_str)
            time_interval, dt_sub_str, dt_sub_end_str = compute_time_interval(msg_update_time,
                                                                              dt_time_limit)
            # 超出时间，结束遍历，结束翻页
            if time_interval < 0:
                return
            fake_msg['fake_id'] = fake_id
            fake_msg['nickname'] = nickname
            fake_msg['round_head_img'] = round_head_img
            fake_msg['alias'] = alias
            yield scrapy.Request(msg_link, callback=self.wechat_article, meta={"fake_msg": fake_msg})

        # 翻页
        pagenum += 1
        begin = (pagenum - 1) * count
        # 超出总数，结束翻页
        if begin > int(fake_msg_cnt):
            return
        logger.info('Fake:{}-{}, Page:{}'.format(nickname, alias, pagenum))
        appmsg_list_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token={token}&lang=zh_CN&f=json&%E2%80%A65&action=list_ex&begin={begin}&count={count}&query={query}&fakeid={fakeid}&type=9'.format(
            token=self.token, fakeid=fake_id, begin=begin, count=count, query='')
        yield scrapy.Request(appmsg_list_url, headers=self.headers, callback=self.fake_page_down, method='GET',
                             dont_filter=True, meta={'fake_info': fake_info,'pagenum':pagenum,'count':count})



    def wechat_article(self, response):
        wechat_fake_article_item = WeChatFakeArticleItem()
        fake_msg = response.meta['fake_msg']
        resp_txt = response.text
        soup = BeautifulSoup(resp_txt, 'lxml')
        # 获取文本内容
        soup_div_list = soup.find_all('div', {'id': 'js_content'})
        if soup_div_list == []:
            soup_div_list = soup.find_all('div', {'class': 'rich_media_content'})
        if soup_div_list == []:
            logger.warning('Soup div list is null! nickname:{}, title:{}'.format(fake_msg['nickname'], fake_msg['title']))
            self.notice_app.send("Project:{}-{}-{},Error:Soup div list is null!".format(self.name, fake_msg['nickname'], fake_msg['title']))
            time.sleep(random.randint(3, 5))
            return
        rich_media_content = soup_div_list[0]
        wechat_fake_article_item['spider_name'] = self.name
        wechat_fake_article_item['fake_nickname'] = fake_msg['nickname']
        wechat_fake_article_item['fake_alias'] = fake_msg['alias']
        wechat_fake_article_item['fake_id'] = fake_msg['fake_id']
        wechat_fake_article_item['fake_head_img'] = fake_msg['round_head_img']
        wechat_fake_article_item['msg_id'] = fake_msg['appmsgid']
        wechat_fake_article_item['msg_cover'] = fake_msg['cover']
        wechat_fake_article_item['msg_digest'] = fake_msg['digest']
        wechat_fake_article_item['msg_link'] = fake_msg['link']
        wechat_fake_article_item['msg_title'] = fake_msg['title']
        wechat_fake_article_item['msg_update_time'] = fake_msg['update_time']
        wechat_fake_article_item['msg_create_time'] = fake_msg['create_time']
        wechat_fake_article_item['msg_content'] = str(rich_media_content)
        yield wechat_fake_article_item
