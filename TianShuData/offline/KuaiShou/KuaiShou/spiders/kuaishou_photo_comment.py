# -*- coding: utf-8 -*-
import scrapy
import json

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouPhotoCommentInfoIterm


class KuaishouPhotoCommentSpider(scrapy.Spider):
    name = 'kuaishou_photo_comment'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700
    }}
    settings = get_project_settings()
    # allowed_domains = ['live.kuaishou.com/graphql']
    # start_urls = ['http://live.kuaishou.com/graphql/']

    def start_requests(self):
        # 配置kafka连接信息
        kafka_hosts = self.settings.get('KAFKA_HOSTS')
        kafka_topic = self.settings.get('KAFKA_TOPIC')
        reset_offset_on_start = self.settings.get('RESET_OFFSET_ON_START')
        self.photo_comment_query = self.settings.get('PHOTO_COMMENT_QUERY')
        client = KafkaClient(hosts=kafka_hosts)
        topic = client.topics[kafka_topic]
        # 配置kafka消费信息
        consumer = topic.get_balanced_consumer(
            consumer_group='test',
            managed=True,
            auto_commit_enable=True
        )
        # 获取被消费数据的偏移量和消费内容
        for message in consumer:
            try:
                if message is None:
                    continue
                # 信息分为message.offset, message.value
                msg_value = message.value.decode()
                msg_value_dict = eval(msg_value)
                if msg_value_dict['spider_name'] != 'kuaishou_user_photo_info':
                    continue
                photo_id = msg_value_dict['user_photo_info']['photoId']
                self.photo_comment_query['variables']['photoId'] = photo_id
                self.kuaikan_url = 'https://live.kuaishou.com/graphql'
                self.headers = {'content-type': 'application/json'}
                yield scrapy.Request(self.kuaikan_url, headers=self.headers, body=json.dumps(self.photo_comment_query),
                                     method='POST', callback=self.parse_photo_comment,
                                     meta={'bodyJson': self.photo_comment_query}
                                     )
            except Exception as e:
                logger.warning('Kafka message structure cannot be resolved :{}'.format(e))

    def parse_photo_comment(self, response):
        rsp_json = json.loads(response.text)
        body_json = response.meta['bodyJson']
        photo_id = body_json['variables']['photoId']

        short_video_comment_list = rsp_json['data']['shortVideoCommentList']
        if short_video_comment_list == None:
            # 删掉did库中的失效did
            # ...待开发
            logger.warning('UserPhotoQuery failed, principalId:{}'.format(photo_id))
            return

        for photo_comment_info in short_video_comment_list['commentList']:
            kuaishou_photo_comment_info_iterm = KuaishouPhotoCommentInfoIterm()
            kuaishou_photo_comment_info_iterm['spider_name'] = self.name
            kuaishou_photo_comment_info_iterm['photo_id'] = photo_id
            kuaishou_photo_comment_info_iterm['photo_comment_info'] = photo_comment_info
            yield kuaishou_photo_comment_info_iterm
        pcursor = short_video_comment_list['pcursor']
        if pcursor == 'no_more':
            return
        self.photo_comment_query['variables']['pcursor'] = pcursor
        yield scrapy.Request(self.kuaikan_url, headers=self.headers, body=json.dumps(self.photo_comment_query),
                             method='POST', callback=self.parse_photo_comment,
                             meta={'bodyJson': self.photo_comment_query}
                             )
