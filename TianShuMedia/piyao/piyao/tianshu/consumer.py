#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'

import sys, os
import jieba

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from scrapy.utils.project import get_project_settings
from pykafka import KafkaClient
import os, datetime
import time
from loguru import logger
from bs4 import BeautifulSoup

from tianshu.utils import get_project_configs
from tianshu.utils.picture import upload_picture

from tianshu.utils.file import para_isexists_file, write_cnt
from tianshu.utils.record import public_record_wechat

settings = get_project_settings()
dev = settings.get('DEV')
log_json = get_project_configs('log.json')
log_path = log_json[dev]['log_dir']
if os.path.exists(log_path) == False:
    os.makedirs(log_path)
logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
logger.add('{}/{}'.format(log_path, os.path.basename(__file__)[:-3]) + "_{time:%Y-%m-%d}.log", rotation="00:00")

# 配置kafka连接信息
kafka_hosts = settings.get('KAFKA_HOSTS')
kafka_topic = settings.get('KAFKA_TOPIC_ARTICLE')
reset_offset_on_start = settings.get('RESET_OFFSET_ON_START')
search_overview_query = settings.get('SEARCH_OVERVIEW_QUERY')
logger.info('kafka info, hosts:{}, topic:{}'.format(kafka_hosts, kafka_topic))
client = KafkaClient(hosts=kafka_hosts)
topic = client.topics[kafka_topic]


# 配置kafka消费信息


def format_to_record(cnt, cover_url=""):
    """
    格式化页面内容，包括处理标签和图片下载
    :param cnt: 页面内容
    :return: format的图文信息
    """
    record = {}
    soup = BeautifulSoup(cnt, 'lxml')
    span_img_soup_list = soup.find_all(['p', 'img'])
    content = ''
    content_html = ''
    img_i = 0
    images = []
    for p_img_soup in span_img_soup_list:
        if p_img_soup.name != 'img':
            # 处理p便签下放img
            img_tags = p_img_soup.find_all('img')
            if img_tags != []:
                continue
            span_img_str = str(p_img_soup)
            # # 处理 推荐阅读 粉丝福利 等
            # if '推荐阅读' in span_img_str :
            #     break
            content_html += span_img_str
            continue
        try:img_url = p_img_soup['data-src']
        except Exception as e:
            logger.warning('soup: {}, error: {}'.format(e,str(p_img_soup)))
            continue
        # 下载视频定制，并上传，生成自己的封面地址
        pic_url_final = upload_picture(img_url)
        if pic_url_final == None:
            continue
        content_html += '<img src="{}" />'.format(pic_url_final)
        # 只取三张做封面
        if img_i >= 3:
            continue
        images.append(pic_url_final)
        img_i += 1

    if img_i >= 3:
        image_type = 3
    else:
        images = images[:1]
        image_type = 1
    record['content_html'] = content_html
    record['content'] = content
    record['image_type'] = image_type
    record['images'] = images
    return record


def process_msg():
    path_json = get_project_configs('path.json')
    articles_dir = path_json[dev]['articles_dir']
    consumer_json = get_project_configs('consumer.json')
    consumer_group_name = consumer_json[dev]['consumer_group']
    consumer = topic.get_balanced_consumer(
        consumer_group=consumer_group_name,
        managed=True,
        auto_commit_enable=True
    )
    # 获取被消费数据的偏移量和消费内容
    for message in consumer:
        if message is None:
            continue
        # 信息分为message.offset, message.value
        msg_value = message.value.decode()
        try:
            msg_value_dict = eval(msg_value)
        except:
            continue
        news_from = 'xmq_{}'.format(msg_value_dict["spider_name"])
        fake_alias = msg_value_dict["fake_alias"]
        title = msg_value_dict["msg_title"]
        content = msg_value_dict["msg_content"]
        # content title
        fake_appid = msg_value_dict["fake_id"]
        msg_id = msg_value_dict["msg_id"]
        fake_nickname = msg_value_dict["fake_nickname"]
        fake_avatar = msg_value_dict["fake_head_img"]
        msg_cover = msg_value_dict['msg_cover']
        custom_id = 185
        msg_update_time = msg_value_dict['msg_update_time']
        "时间戳转时间"
        msg_update_time_array = time.localtime(msg_update_time)
        msg_update_time_str = time.strftime("%Y-%m-%d %H:%M:%S", msg_update_time_array)
        msg_update_time_fomat = datetime.datetime.strptime(msg_update_time_str, '%Y-%m-%d %H:%M:%S')
        dt_sub_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 判断内容是否已抓取
        path_info = '{}/{}/{}.txt'.format(articles_dir, fake_alias, msg_update_time_str[:10])
        is_para = para_isexists_file(path_info, title, slice_i=1, split_str="|||")
        if is_para:
            continue
        record = format_to_record(content, msg_cover)
        record['news_type'] = 2
        record['weixin_appid'] = fake_alias
        record['title'] = title
        record['origin_author_name'] = fake_nickname
        record['origin_author_avatar'] = fake_avatar
        record['is_draft'] = 1
        record['type'] = 3
        record['is_check_time'] = -1
        record['channel_id'] = 0
        record['news_from'] = news_from
        record['origin_publish_time'] = msg_update_time_str
        # 发布内容
        pubilc_res_json = public_record_wechat(record, custom_id)
        message = pubilc_res_json['message']
        if message != 'SUCCESS':
            logger.info(
                '图文发布失败! nickname: {}, pulish_time: {}, title: {}, massage: {}'.format(fake_nickname,
                                                                                       msg_update_time_str, title,
                                                                                       pubilc_res_json))
            continue
        logger.info('图文发布成功! nickname: {}, pulish_time: {}, title: {}, massage: {}'.format(fake_nickname, title,
                                                                                           msg_update_time_str,
                                                                                           pubilc_res_json))
        write_cnt([msg_id, title, msg_update_time_fomat], path_info, '|||')


if __name__ == '__main__':
    process_msg()
