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
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700,
        'KuaiShou.pipelines.KuaishouScrapyLogsMySQLPipeline': 701,
        'KuaiShou.pipelines.KuaishouUserSeedsMySQLPipeline': 702,
    },
    'CONCURRENT_REQUESTS_PER_DOMAIN' : 16,
    'CONCURRENT_REQUESTS' : 1
    }
    kuaishou_url = 'http://live.kuaishou.com/m_graphql'

    def start_requests(self):
        settings = get_project_settings()
        # 连接redis
        redis_host = settings.get('REDIS_HOST')
        redis_port = settings.get('REDIS_PORT')
        self.redis_did_name = settings.get('REDIS_DID_NAME')
        self.redis_proxyip_name = settings.get('REDIS_PROXYIP_NAME')
        self.conn = Redis(host=redis_host, port=redis_port)

        search_overview_query = settings.get('SEARCH_OVERVIEW_QUERY')
        self.headers = {
            "accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "content-type": "application/json",
            "Origin": "https://live.kuaishou.com",
            "Referer": "https://live.kuaishou.com/search/?keyword=1",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

        # 配置kafka连接信息
        kafka_hosts = settings.get('KAFKA_HOSTS')
        kafka_topic = settings.get('KAFKA_USERINFO_SEEDS_TOPIC')
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
                self.headers['Referer'] = 'https://live.kuaishou.com/search/?keyword={}'.format(user_id)
                search_overview_query['variables']['keyword'] = '{}'.format(user_id)
                # logger.info(json.dumps(self.search_overview_query))
                # self.conn.incr('kwai_userInfo_offSetSize', 1)
                yield scrapy.Request(self.kuaishou_url, headers=self.headers,
                                     body=json.dumps(search_overview_query),
                                     method='POST',
                                     meta={'bodyJson': search_overview_query, 'msg_value_dict': msg_value_dict,
                                           'retry_times': 0},
                                     callback=self.parse_search_overview, dont_filter=True
                                     )
            except Exception as e:
                logger.warning('Kafka message[{}] structure cannot be resolved :{}'.format(str(msg_value_dict), e))

    def parse_search_overview(self, response):
        try:
            rsp_search_overview_json = json.loads(response.text)
        except:
            # 处理在频率过快的时候 response.text = 你想干嘛？等情况
            logger.warning(response.text)
            rsp_search_overview_json = {'data': {'pcSearchOverview': None}}
            time.sleep(10)
        finally:
            logger.info(rsp_search_overview_json)
            pc_search_overview = rsp_search_overview_json['data']['pcSearchOverview']
        msg_value_dict = response.meta['msg_value_dict']
        search_overview_query = response.meta['bodyJson']
        current_retry_times = response.meta['retry_times'] + 1
        user_id = msg_value_dict['userId']
        if pc_search_overview == None:
            # 删掉did库中的失效did
            kuaishou_did_json = response.meta['Cookie']
            logger.info('RedisDid srem invaild did:{}'.format(str(kuaishou_did_json)))
            self.conn.zrem(self.redis_did_name, str(kuaishou_did_json).encode('utf-8'))
            # 再次尝试抓取，尝试3次
            logger.warning('userId: {}, pcSearchOverview authors list is None ! '.format(user_id))
            if current_retry_times > 7:
                yield self.create_fail_items(user_id, -1)
            else:
                logger.warning(
                    'pcSearchOverview failed, result is None, userId: {}, retryTimes: {}'.format(user_id,
                                                                                                 current_retry_times))
                time.sleep(3)
                yield scrapy.Request(self.kuaishou_url, headers=self.headers, body=json.dumps(search_overview_query),
                                     method='POST',
                                     meta={'bodyJson': search_overview_query, 'msg_value_dict': msg_value_dict,
                                           'retry_times': current_retry_times},
                                     callback=self.parse_search_overview, dont_filter=True
                                     )
        else:
            search_overview_list = pc_search_overview['list']
            for search_overview in search_overview_list:
                if search_overview['type'] != 'authors':
                    continue
                search_overview_authors = search_overview['list']
                if search_overview_authors != []:
                    author_info = search_overview_authors[0]
                    yield self.create_sucess_items(user_id, author_info)
                    break
                logger.warning('userId: {}, pcSearchOverview authors list is [] ! '.format(user_id))
                # 删掉did库中的失效did
                invaild_did = response.meta['Cookie']
                logger.info('RedisDid srem invaild did:{}'.format(str(invaild_did)))
                self.conn.zrem(self.redis_did_name, str(invaild_did).encode('utf-8'))
                # 再次尝试抓取，尝试7次
                if current_retry_times > 3:
                    yield self.create_fail_items(user_id, -2)
                    break
                logger.warning(
                    'pcSearchOverview failed, result is None, userId: {}, retryTimes: {}'.format(user_id,
                                                                                                 current_retry_times))
                time.sleep(3)
                yield scrapy.Request(self.kuaishou_url, headers=self.headers, body=json.dumps(search_overview_query),
                                     method='POST',
                                     meta={'bodyJson': search_overview_query, 'msg_value_dict': msg_value_dict,
                                           'retry_times': current_retry_times},
                                     callback=self.parse_search_overview, dont_filter=True
                                     )

    def create_fail_items(self, user_id, fail_type):
        kuaishou_user_info_iterm = KuaishouUserInfoIterm()
        kuaishou_user_info_iterm['spider_name'] = self.name
        kuaishou_user_info_iterm['is_successed'] = fail_type
        kuaishou_user_info_iterm['userId'] = user_id
        return kuaishou_user_info_iterm

    def create_sucess_items(self, user_id, author_info):
        kuaishou_user_info_iterm = KuaishouUserInfoIterm()
        logger.info('Search userinfo reslut: {}'.format(str(author_info)))
        kuaishou_user_info_iterm['spider_name'] = self.name
        kuaishou_user_info_iterm['userId'] = user_id
        kuaishou_user_info_iterm['kwaiId'] = author_info['id']
        kuaishou_user_info_iterm['principalId'] = author_info['id']
        kuaishou_user_info_iterm['nickname'] = author_info['name']
        kuaishou_user_info_iterm['avatar'] = author_info['avatar']
        kuaishou_user_info_iterm['sex'] = author_info['sex']
        kuaishou_user_info_iterm['description'] = author_info['description']
        kuaishou_user_info_iterm['fan'] = author_info['counts']['fan']
        kuaishou_user_info_iterm['follow'] = author_info['counts']['follow']
        kuaishou_user_info_iterm['photo'] = author_info['counts']['photo']
        kuaishou_user_info_iterm['is_successed'] = 1
        return kuaishou_user_info_iterm
