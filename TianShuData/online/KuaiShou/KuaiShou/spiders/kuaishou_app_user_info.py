# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random

from scrapy.utils.project import get_project_settings
from pykafka import KafkaClient
from loguru import logger
from redis import Redis
from urllib.parse import urlencode

from KuaiShou.items import KuaishouUserInfoIterm
from KuaiShou.utils.signatureUtil import signatureUtil


class KuaishouAppUserInfoSpider(scrapy.Spider):
    name = 'kuaishou_app_user_info'
    custom_settings = {
        'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700,
        'KuaiShou.pipelines.KuaishouScrapyLogsPipeline': 701
        },
        'CONCURRENT_REQUESTS_PER_DOMAIN': '1',
    }
    settings = get_project_settings()
    # 连接redis
    redis_host = settings.get('REDIS_HOST')
    redis_port = settings.get('REDIS_PORT')
    redis_did_name = settings.get('REDIS_DID_NAME')
    redis_proxyip_name = settings.get('REDIS_PROXYIP_NAME')
    conn = Redis(host=redis_host, port=redis_port)

    # 用户信息的url由：userPreUrl + userMainUrl + sigPart 拼接而成，其中userMainUrl进行签名计算
    userPreUrl = "https://api.gifshow.com/rest/n/user/profile/v2?"
    params = {
        "mod": "OPPO(OPPO%20R11)",
        "lon": "120.174975",
        "country_code": "CN",
        "did": "ANDROID_ff30ff78e0b7b86b",
        "app": "0",
        "net": "WIFI",
        "oc": "UNKNOWN",
        "ud": "0",
        "c": "ALI_CPD",
        "sys": "ANDROID_5.1.1",
        "appver": "5.2.1.4686",
        "ftt": "",
        "language": "zh-cn",
        "lat": "30.370968",
        "ver": "5.2",
        "user": "40300005",
        "client_key": "3c2cd3f3",
        "os": "android"
    }


    headers = {
        'User-Agent': 'kwai-android',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'api.gifshow.com',
        'Accept-Encoding': 'gzip',
    }
    sigUtil = signatureUtil()

    def start_requests(self):

        msg_value_dict = {'userId': 40300005, 'kwaiId': 'SS19908888', 'principalId': 'SS19908888', 'spider_name': 'kuaishou_user_seeds'}
        tempUrl = urlencode(self.params)
        sig = self.sigUtil.getSig(tempUrl)
        sigPart = "&sig={}".format(sig)
        userUrl = self.userPreUrl + tempUrl + sigPart
        time.sleep(random.choice(range(5, 10)))
        yield scrapy.Request(userUrl, method='POST', meta={'msg_value_dict': msg_value_dict},
                             callback=self.parseUserInfoUrl)

        # # 配置kafka连接信息
        # kafka_hosts = self.settings.get('KAFKA_HOSTS')
        # kafka_topic = self.settings.get('KAFKA_USERINFO_SEEDS_TOPIC')
        # logger.info('kafka info, hosts:{}, topic:{}'.format(kafka_hosts, kafka_topic))
        # client = KafkaClient(hosts=kafka_hosts)
        # topic = client.topics[kafka_topic]
        # # 配置kafka消费信息
        # consumer = topic.get_balanced_consumer(
        #     consumer_group=self.name,
        #     managed=True,
        #     auto_commit_enable=True
        # )
        # # 获取被消费数据的偏移量和消费内容
        # for message in consumer:
        #     try:
        #         if message is None:
        #             continue
        #         # 信息分为message.offset, message.value
        #         msg_value = message.value.decode()
        #         msg_value_dict = eval(msg_value)
        #         if 'spider_name' not in list(msg_value_dict.keys()):
        #             logger.warning('Excloude key: spider_name, msg: {}'.format(msg_value))
        #             continue
        #         if msg_value_dict['spider_name'] != 'kuaishou_user_seeds':
        #             continue
        #         user_id = msg_value_dict['userId']
        #         self.params['user'] = user_id
        #         tempUrl = urlencode(self.params)
        #         sig = self.sigUtil.getSig(tempUrl)
        #         sigPart = "&sig={}".format(sig)
        #         userUrl = self.userPreUrl + tempUrl + sigPart
        #         time.sleep(random.choice(range(15, 30)))
        #         yield scrapy.Request(userUrl, method='POST', meta={'msg_value_dict': msg_value_dict},
        #                              callback=self.parseUserInfoUrl)
        #     except Exception as e:
        #         logger.warning('Kafka message[{}] structure cannot be resolved :{}'.format(str(msg_value_dict), e))


    def parseUserInfoUrl(self, response):
        logger.info(response.text)
        # kuaishou_user_info_iterm = KuaishouUserInfoIterm()
        # kuaishou_user_info_iterm['spider_name'] = self.name
        # msg_value_dict = response.meta['msg_value_dict']
        # user_id = msg_value_dict['userId']
        # kuaishou_user_info_iterm['userId'] = user_id
        # if response.status != 200:
        #     kuaishou_user_info_iterm['is_successed'] = response.status
        #     logger.warning(
        #         'userId: {user_id}, Failed! response status: {status}'.format(user_id=user_id, status=response.status))
        #     return kuaishou_user_info_iterm
        # rltJson = json.loads(response.text)
        # if rltJson['result'] != 1:
        #     kuaishou_user_info_iterm['is_successed'] = -3
        #     logger.info('userId: {user_id}, interface error: {error}'.format(user_id=user_id, error=response.text))
        #     return kuaishou_user_info_iterm
        # logger.info(rltJson)
        # userInfo = rltJson['userProfile']
        # if 'profile' in userInfo:
        #     userProfile = userInfo['profile']
        #     if 'kwaiId' in userProfile:
        #         kuaishou_user_info_iterm['kwaiId'] = userProfile['kwaiId']
        #     if 'user_id' in userProfile:
        #         kuaishou_user_info_iterm['userId'] = userProfile['user_id']
        #     if 'user_name' in userProfile:
        #         kuaishou_user_info_iterm['nickname'] = userProfile['user_name']
        #     if 'user_sex' in userProfile:
        #         kuaishou_user_info_iterm['sex'] = userProfile['user_sex']
        #     if 'user_text' in userProfile:
        #         kuaishou_user_info_iterm['description'] = userProfile['user_text']
        #     if 'headurl' in userProfile:
        #         kuaishou_user_info_iterm['avatar'] = userProfile['headurl']
        # if 'cityName' in userInfo:
        #     kuaishou_user_info_iterm['cityName'] = userInfo['cityName']
        # if 'constellation' in userInfo:
        #     kuaishou_user_info_iterm['constellation'] = userInfo['constellation']
        #
        # if 'ownerCount' in userInfo:
        #     ownerCount = userInfo['ownerCount']
        #     if 'fan' in ownerCount:
        #         kuaishou_user_info_iterm['fan'] = ownerCount['fan']
        #     if 'follow' in ownerCount:
        #         kuaishou_user_info_iterm['follow'] = ownerCount['follow']
        #     if 'like' in ownerCount:
        #         kuaishou_user_info_iterm['liked'] = ownerCount['like']
        #     if 'photo' in ownerCount:
        #         userInfo['photo'] = ownerCount['photo']
        #     # if 'moment' in ownerCount:
        #     #     userInfo['moment'] = ownerCount['moment']
        #     # if 'photo_private' in ownerCount:
        #     #     userItem['photo_private'] = ownerCount['photo_private']
        #     # if 'photo_public' in ownerCount:
        #     #     userItem['photo_public'] = ownerCount['photo_public']
        # return kuaishou_user_info_iterm
