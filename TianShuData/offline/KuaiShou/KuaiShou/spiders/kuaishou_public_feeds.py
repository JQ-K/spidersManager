# -*- coding: utf-8 -*-
import scrapy
import json

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouUserPhotoInfoIterm


class KuaishouUserPhotoSpider(scrapy.Spider):
    name = 'kuaishou_public_feeds'
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
        self.public_feeds_query = self.settings.get('PUBLIC_FEEDS_QUERY')
        client = KafkaClient(hosts=kafka_hosts)
        topic = client.topics[kafka_topic]
        # 配置kafka消费信息
        consumer = topic.get_balanced_consumer(
            consumer_group=self.name,
            managed=True,
            auto_commit_enable=True
        )
        self.kuaikan_url = 'https://live.kuaishou.com/graphql'
        self.headers = {'content-type': 'application/json'}
        # 获取被消费数据的偏移量和消费内容
        for message in consumer:
            try:
                if message is None:
                    continue
                # 信息分为message.offset, message.value
                msg_value = message.value.decode()
                msg_value_dict = eval(msg_value)
                if msg_value_dict['spider_name'] != 'kuanshou_kol_seeds':
                    continue
                principal_id = msg_value_dict['principalId']
                self.public_feeds_query['variables']['principalId'] = principal_id
                yield scrapy.Request(self.kuaikan_url, headers=self.headers, body=json.dumps(self.public_feeds_query),
                                     method='POST', callback=self.parse_user_photo,
                                     meta={'bodyJson': self.public_feeds_query}
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
        for user_photo_info in public_feeds['list']:
            kuaishou_user_photo_info_iterm = KuaishouUserPhotoInfoIterm()
            kuaishou_user_photo_info_iterm['spider_name'] = self.name
            kuaishou_user_photo_info_iterm['user_photo_info'] = user_photo_info
            yield kuaishou_user_photo_info_iterm
        pcursor = public_feeds['pcursor']
        if pcursor == 'no_more':
            return
        self.public_feeds_query['variables']['pcursor'] = pcursor
        yield scrapy.Request(self.kuaikan_url, headers=self.headers, body=json.dumps(self.public_feeds_query),
                             method='POST', callback=self.parse_user_photo, meta={'bodyJson': self.public_feeds_query}
                             )
