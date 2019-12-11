# -*- coding: utf-8 -*-
import scrapy
import json

from pykafka import KafkaClient
from loguru import logger

from KuaiShou.settings import KAFKA_HOSTS, KAFKA_TOPIC, RESET_OFFSET_ON_START, USER_PHOTO_QUERY
from KuaiShou.items import KuaishouUserPhotoInfoIterm


class KuaishouUserPhotoSpider(scrapy.Spider):
    name = 'kuaishou_user_photo_info'
    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700
    }}
    allowed_domains = ['live.kuaishou.com/graphql']

    # start_urls = ['http://live.kuaishou.com/graphql/']

    def start_requests(self):
        # 配置kafka连接信息
        client = KafkaClient(hosts=KAFKA_HOSTS)
        topic = client.topics[KAFKA_TOPIC]
        # 配置kafka消费信息
        consumer = topic.get_simple_consumer(
            consumer_group=self.name,
            reset_offset_on_start=RESET_OFFSET_ON_START
        )
        # 获取被消费数据的偏移量和消费内容
        for message in consumer:
            try:
                if message is None:
                    continue
                # 信息分为message.offset, message.value
                msg_value = message.value.decode()
                msg_value_dict = eval(msg_value)
                if msg_value_dict['name'] != 'kuxuan_kol_user':
                    continue
                self.kwai_id = msg_value_dict['kwaiId']
                self.user_photo_query = USER_PHOTO_QUERY
                self.user_photo_query['variables']['principalId'] = self.kwai_id
                self.kuaikan_url = 'https://live.kuaishou.com/graphql'
                self.headers = {'content-type': 'application/json'}
                yield scrapy.Request(self.kuaikan_url, headers=self.headers, body=json.dumps(self.user_photo_query),
                                     method='POST', callback=self.parse_user_photo,
                                     meta={'bodyJson': self.user_photo_query},
                                     cookies={'did': 'web_d54ea5e1190a41e481809b9cd17f92aa'}
                                     )
            except Exception as e:
                logger.warning('Kafka message structure cannot be resolved :{}'.format(e))

    def parse_user_photo(self, response):
        rsp_json = json.loads(response.text)
        public_feeds = rsp_json['data']['publicFeeds']
        if public_feeds['list'] == []:
            # 删掉did库中的失效did
            # ...待开发
            body_json = response.meta['bodyJson']
            principal_id = body_json['variables']['principalId']
            logger.warning('UserPhotoQuery failed, principalId:{}'.format(principal_id))
            return
        for user_photo_info in public_feeds['list'][1:2]:
            kuaishou_user_photo_info_iterm = KuaishouUserPhotoInfoIterm()
            kuaishou_user_photo_info_iterm['name'] = self.name
            kuaishou_user_photo_info_iterm['user_photo_info'] = user_photo_info
            yield kuaishou_user_photo_info_iterm
        pcursor = public_feeds['pcursor']
        if pcursor == 'no_more':
            return
        self.user_photo_query['variables']['pcursor'] = pcursor
        yield scrapy.Request(self.kuaikan_url, headers=self.headers, body=json.dumps(self.user_photo_query),
                             method='POST', callback=self.parse_user_photo, meta={'bodyJson': self.user_photo_query},
                             cookies={'did': 'web_d54ea5e1190a41e481809b9cd17f92aa'}
                             )
