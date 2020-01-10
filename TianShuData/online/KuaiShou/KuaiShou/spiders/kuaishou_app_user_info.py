# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random

from scrapy.utils.project import get_project_settings
from pykafka import KafkaClient
from loguru import logger
from redis import Redis

from KuaiShou.items import KuaishouUserInfoIterm
from KuaiShou.utils.signatureUtil import signatureUtil


class KuaishouAppUserInfoSpider(scrapy.Spider):
    name = 'kuaishou_app_user_info'

    custom_settings = {'ITEM_PIPELINES': {
        'KuaiShou.pipelines.KuaishouKafkaPipeline': 700,
        'KuaiShou.pipelines.KuaishouScrapyLogsPipeline': 701
    }}
    settings = get_project_settings()
    # 连接redis
    redis_host = settings.get('REDIS_HOST')
    redis_port = settings.get('REDIS_PORT')
    redis_did_name = settings.get('REDIS_DID_NAME')
    redis_proxyip_name = settings.get('REDIS_PROXYIP_NAME')
    conn = Redis(host=redis_host, port=redis_port)

    # 用户信息的url由：userPreUrl + userMainUrl + sigPart 拼接而成，其中userMainUrl进行签名计算
    userPreUrl = "https://api.gifshow.com/rest/n/user/profile/v2?"
    userMainUrl = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&user={}&client_key=3c2cd3f3&os=android"

    sigPart = "&sig={}"

    headers = {
        'X-REQUESTID': '1328313',
        'User-Agent': 'kwai-android',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '144',
        'Host': 'api.gifshow.com',
        'Accept-Encoding': 'gzip',
    }


    def __init__(self):
        self.sigUtil = signatureUtil()


    def start_requests(self):
        # 配置kafka连接信息
        kafka_hosts = self.settings.get('KAFKA_HOSTS')
        kafka_topic = self.settings.get('KAFKA_USERINFO_SEEDS_TOPIC')
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

                tempUrl = self.userMainUrl.format(user_id)
                sig = self.sigUtil.getSig(tempUrl)
                userUrl = self.userPreUrl + tempUrl + self.sigPart.format(sig)
                time.sleep(random.choice(range(15, 30)))
                yield scrapy.Request(userUrl, method='POST',
                                     callback=self.parseUserInfoUrl)
            except Exception as e:
                logger.warning('Kafka message[{}] structure cannot be resolved :{}'.format(str(msg_value_dict), e))


    def parseUserInfoUrl(self, response):
        if response.status != 200:
            logger.info('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        if rltJson['result'] != 1:
            logger.info('get user interface error: ' + response.text)
            return
        userInfo = rltJson['userProfile']
        self.getUserInfoItem(userInfo)


    def getUserInfoItem(self, userInfo):
        userItem = KuaishouUserInfoIterm()
        userItem['spider_name'] = self.name
        if 'profile' in userInfo:
            userProfile = userInfo['profile']
            if 'kwaiId' in userProfile:
                userItem['kwaiId'] = userProfile['kwaiId']
            if 'user_id' in userProfile:
                #userItem['user_id'] = userProfile['user_id']
                userItem['userId'] = userProfile['user_id']
            if 'user_name' in userProfile:
                #userItem['user_name'] = userProfile['user_name']
                userItem['nickname'] = userProfile['user_name']
            if 'user_sex' in userProfile:
                #userItem['user_sex'] = userProfile['user_sex']
                userItem['sex'] = userProfile['user_sex']
            if 'user_text' in userProfile:
                #userItem['user_text'] = userProfile['user_text']
                userItem['description'] = userProfile['user_text']
            if 'headurl' in userProfile:
                #userItem['head_url'] = userProfile['headurl']
                userItem['avatar'] = userProfile['headurl']

        # if 'cityCode' in userInfo:
        #     userItem['cityCode'] = userInfo['cityCode']
        if 'cityName' in userInfo:
            userItem['cityName'] = userInfo['cityName']
        if 'constellation' in userInfo:
            userItem['constellation'] = userInfo['constellation']

        if 'ownerCount' in userInfo:
            ownerCount = userInfo['ownerCount']
            # if 'article_public' in ownerCount:
            #     userItem['article_public'] = ownerCount['article_public']
            # if 'collect' in ownerCount:
            #     userItem['collect'] = ownerCount['collect']
            if 'fan' in ownerCount:
                userItem['fan'] = ownerCount['fan']
            if 'follow' in ownerCount:
                userItem['follow'] = ownerCount['follow']
            if 'like' in ownerCount:
                #userItem['like'] = ownerCount['like']
                userItem['liked'] = ownerCount['like']
            # if 'moment' in ownerCount:
            #     userInfo['moment'] = ownerCount['moment']
            if 'photo' in ownerCount:
                userInfo['photo'] = ownerCount['photo']
            # if 'photo_private' in ownerCount:
            #     userItem['photo_private'] = ownerCount['photo_private']
            # if 'photo_public' in ownerCount:
            #     userItem['photo_public'] = ownerCount['photo_public']
        #print(userItem)
        yield userItem


    # def getUserInfoItem(self, userInfo):
    #     userItem = KuaishouUserInfoIterm()
    #     userItem['spider_name'] = self.name
    #     if 'profile' in userInfo:
    #         userProfile = userInfo['profile']
    #         if 'kwaiId' in userProfile:
    #             userItem['kwaiId'] = userProfile['kwaiId']
    #         if 'user_id' in userProfile:
    #             userItem['user_id'] = userProfile['user_id']
    #         if 'user_name' in userProfile:
    #             userItem['user_name'] = userProfile['user_name']
    #         if 'user_sex' in userProfile:
    #             userItem['user_sex'] = userProfile['user_sex']
    #         if 'user_text' in userProfile:
    #             userItem['user_text'] = userProfile['user_text']
    #         if 'headurl' in userProfile:
    #             userItem['head_url'] = userProfile['headurl']
    #
    #     if 'cityCode' in userInfo:
    #         userItem['cityCode'] = userInfo['cityCode']
    #     if 'cityName' in userInfo:
    #         userItem['cityName'] = userInfo['cityName']
    #     if 'constellation' in userInfo:
    #         userItem['constellation'] = userInfo['constellation']
    #
    #     if 'ownerCount' in userInfo:
    #         ownerCount = userInfo['ownerCount']
    #         if 'article_public' in ownerCount:
    #             userItem['article_public'] = ownerCount['article_public']
    #         if 'collect' in ownerCount:
    #             userItem['collect'] = ownerCount['collect']
    #         if 'fan' in ownerCount:
    #             userItem['fan'] = ownerCount['fan']
    #         if 'follow' in ownerCount:
    #             userItem['follow'] = ownerCount['follow']
    #         if 'like' in ownerCount:
    #             userItem['like'] = ownerCount['like']
    #         if 'moment' in ownerCount:
    #             userInfo['moment'] = ownerCount['moment']
    #         if 'photo' in ownerCount:
    #             userInfo['photo'] = ownerCount['photo']
    #         if 'photo_private' in ownerCount:
    #             userItem['photo_private'] = ownerCount['photo_private']
    #         if 'photo_public' in ownerCount:
    #             userItem['photo_public'] = ownerCount['photo_public']
    #     print(userItem)
    #     #yield userItem




