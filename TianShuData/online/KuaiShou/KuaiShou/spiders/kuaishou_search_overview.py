# -*- coding: utf-8 -*-
import scrapy
import json
import time

from scrapy.utils.project import get_project_settings
from pykafka import KafkaClient
from loguru import logger
from redis import Redis

from KuaiShou.items import KuaishouUserInfoIterm

class KuaishouUserCountsSpider(scrapy.Spider):
    name = 'kuaishou_search_overview'
    # allowed_domains = ['live.kuaishou.com/m_graphql']
    # start_urls = ['http://live.kuaishou.com/m_graphql/']

    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700
    }}
    settings = get_project_settings()
    # 连接redis
    redis_host = settings.get('REDIS_HOST')
    redis_port = settings.get('REDIS_PORT')
    redis_did_name = settings.get('REDIS_DID_NAME')
    conn = Redis(host=redis_host, port=redis_port)

    kuaishou_url = 'http://live.kuaishou.com/m_graphql'
    search_overview_query = settings.get('SEARCH_OVERVIEW_QUERY')
    headers = {'content-type': 'application/json'}

    def start_requests(self):
        # 配置kafka连接信息
        kafka_hosts = self.settings.get('KAFKA_HOSTS')
        kafka_topic = self.settings.get('KAFKA_TOPIC')
        logger.info('kafka info, hosts:{}, topic:{}'.format(kafka_hosts, kafka_topic))
        client = KafkaClient(hosts=kafka_hosts)
        topic = client.topics[kafka_topic]
        # 配置kafka消费信息
        consumer = topic.get_balanced_consumer(
            consumer_group=self.name,
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
                if 'spider_name' not in list(msg_value_dict.keys()):
                    logger.warning('Excloude key: spider_name, msg: {}'.format(msg_value))
                    continue
                if msg_value_dict['spider_name'] != 'kuaishou_user_seeds':
                    continue
                user_id = msg_value_dict['userId']
                self.search_overview_query['variables']['keyword'] = '{}'.format(user_id)
                yield scrapy.Request(self.kuaishou_url, headers=self.headers, body=json.dumps(self.search_overview_query),
                                     method='POST',
                                     meta={'bodyJson': self.search_overview_query, 'msg_value_dict': msg_value_dict, 'retry_times':0},
                                     callback=self.parse_search_overview, dont_filter=True
                                     )
            except Exception as e:
                logger.warning('Kafka message[{}] structure cannot be resolved :{}'.format(str(msg_value_dict),e))


    def parse_search_overview(self, response):
        try:
            rsp_search_overview_json = json.loads(response.text)
        except:
            # 处理在频率过快的时候 response.text = 你想干嘛？等情况
            rsp_search_overview_json = {'data':{'pcSearchOverview':None}}
            time.sleep(3)
        finally:
            logger.info(rsp_search_overview_json)
            pc_search_overview = rsp_search_overview_json['data']['pcSearchOverview']
        if pc_search_overview == None:
            # 删掉did库中的失效did
            kuaishou_did_json = response.meta['didJson']
            logger.info('RedisDid srem invaild did:{}'.format(str(kuaishou_did_json)))
            self.conn.srem(self.redis_did_name, str(kuaishou_did_json).encode('utf-8'))
            # 再次尝试抓取，尝试7次
            retry_times = response.meta['retry_times'] + 1
            if retry_times>7:
                return
            search_overview_query = response.meta['bodyJson']
            msg_value_dict = response.meta['msg_value_dict']
            user_id = msg_value_dict['userId']
            logger.warning('pcSearchOverview failed, result is None, userId: {}, retryTimes: {}'.format(user_id, retry_times))
            time.sleep(3)
            return scrapy.Request(self.kuaishou_url, headers=self.headers, body=json.dumps(search_overview_query),
                                 method='POST',
                                 meta={'bodyJson': search_overview_query, 'msg_value_dict': msg_value_dict, 'retry_times':retry_times},
                                 callback=self.parse_search_overview, dont_filter=True
                                 )
        search_overview_list = pc_search_overview['list']
        for search_overview in search_overview_list:
            if search_overview['type'] != 'authors':
                continue
            for  author_info in search_overview['list']:
                logger.info('Search userinfo reslut: {}'.format(str(author_info)))
                kuaishou_user_info_iterm = KuaishouUserInfoIterm()
                kuaishou_user_info_iterm['spider_name'] = self.name
                kuaishou_user_info_iterm['principalId'] = author_info['id']
                kuaishou_user_info_iterm['nickname'] = author_info['name']
                kuaishou_user_info_iterm['avatar'] = author_info['avatar']
                kuaishou_user_info_iterm['sex'] = author_info['sex']
                kuaishou_user_info_iterm['description'] = author_info['description']
                kuaishou_user_info_iterm['fan'] = author_info['counts']['fan']
                kuaishou_user_info_iterm['follow'] = author_info['counts']['follow']
                kuaishou_user_info_iterm['photo'] = author_info['counts']['photo']
                yield kuaishou_user_info_iterm
