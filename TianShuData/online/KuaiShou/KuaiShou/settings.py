# -*- coding: utf-8 -*-
from KuaiShou.utils.useragent import UAPOOL
import random

# Scrapy settings for KuaiShou project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'KuaiShou'

SPIDER_MODULES = ['KuaiShou.spiders']
NEWSPIDER_MODULE = 'KuaiShou.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'KuaiShou (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = random.randint(2, 5)
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'KuaiShou.middlewares.KuaishouSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'KuaiShou.middlewares.KuaishouDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     'KuaiShou.pipelines.KuaishouPipeline': 300,
#     'KuaiShou.pipelines.KuxuanKolUserPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

HTTPERROR_ALLOWED_CODES = [500, 400]
# log
# LOG_LEVEL = 'INFO'
LOG_LEVEL = 'WARNING'

# 超时时间,超时尝试时间
RETRY_ENABLED = True
RETRY_TIMES = 3
DOWNLOAD_TIMEOUT = 7

SEARCH_OVERVIEW_QUERY = {
    "operationName": "SearchOverviewQuery",
    "variables": {
        "keyword": "500730148",
        "ussid": ""
    },
    "query": "query SearchOverviewQuery($keyword: String, $ussid: String) {\n  pcSearchOverview(keyword: $keyword, ussid: $ussid) {\n    list {\n      ... on SearchCategoryList {\n        type\n        list {\n          categoryId\n          categoryAbbr\n          title\n          src\n          __typename\n        }\n        __typename\n      }\n      ... on SearchUserList {\n        type\n        ussid\n        list {\n          id\n          name\n          living\n          avatar\n          sex\n          description\n          counts {\n            fan\n            follow\n            photo\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on SearchLivestreamList {\n        type\n        lssid\n        list {\n          user {\n            id\n            avatar\n            name\n            __typename\n          }\n          poster\n          coverUrl\n          caption\n          id\n          playUrls {\n            quality\n            url\n            __typename\n          }\n          quality\n          gameInfo {\n            category\n            name\n            pubgSurvival\n            type\n            kingHero\n            __typename\n          }\n          hasRedPack\n          liveGuess\n          expTag\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
}

# REDIS配置信息
# REDIS_HOST = 'zqhd5'
REDIS_HOST = '10.8.26.105'
REDIS_PORT = 6379
REDIS_DID_NAME = 'tianshu_did'
REDIS_PROXYIP_NAME = 'tianshu_proxyip_kuaishou'
REDIS_DID_EXPIRE_TIME = 900

# MySQL配置信息
# MYSQL_HOST = 'zqhd3'
# MYSQL_USER = 'tianshu'
# MYSQL_PASSWORD = 'Tianshu_123'
# MYSQL_DATABASE = 'tianshuData'
MYSQL_HOST = '10.8.26.106'
MYSQL_USER = 'scrapy'
MYSQL_PASSWORD = 'Scrapy_123'
MYSQL_DATABASE = 'tianshuData'
MYSQL_KUAISHOU_USER_SEEDS_TABLENAME = 'kuaishou_user_seeds'
MYSQL_KUAISHOU_SCRAPY_LOGS_TABLENAME = 'kuaishou_scrapy_logs'

# kafka 相关信息及配置
# KAFKA_HOSTS = 'zqhd1:9092,zqhd2:9092,zqhd3:9092'
KAFKA_HOSTS = 'zb2627:9092,zb2628:9092,zb2629:9092'
ZOOKEEPER_HOSTS = 'zb2627:2181,zb2628:2181,zb2629:2181'
KAFKA_USERINFO_SEEDS_TOPIC = 'kuaishou_userInfo_seeds'
KAFKA_ONLINE_DAILY_TOPIC = 'kuaishou_online_daily'

# spider did pool
SPIDER_DID_SUPPLEMENTS_QUANTITY_PER_TIME = 6
SPIDER_DID_POOL_WARNING_LINE = 60
