# -*- coding: utf-8 -*-
import socket


# Scrapy settings for tianshu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'tianshu'

SPIDER_MODULES = ['tianshu.spiders']
NEWSPIDER_MODULE = 'tianshu.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tianshu (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 15
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tianshu.middlewares.TianshuSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'tianshu.middlewares.TianshuDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'tianshu.pipelines.TianshuPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# 获取当前环境
hostname = socket.gethostname()
if 'Rong' in hostname:
    DEV = "beta"
elif 'WEB' in hostname:
    DEV = "web"
elif 'pre' in hostname:
    DEV = "pre"
elif 'Lish' in hostname:
    DEV = "local"
else:
    DEV = "beta"

# cookie
WECHAT_FAKE_TOKEN = 303209255
WECHAT_FAKE_COOKIE = 'annual_review_dialog=1; noticeLoginFlag=1; ua_id=wecIhYgcC0i6D1SGAAAAAEz-qJ5DYdQq6u3jYNgwJ8Q=; pgv_pvi=4703024128; noticeLoginFlag=1; mm_lang=zh_CN; ptui_loginuin=1165098845; RK=V5QtBiWjUx; ptcz=e22545525c72f1a2775556cf41f918853405cc4d42d2d77b250cd3de0e0b243d; openid2ticket_of2_st8KsAFs-M-hJvYxM5jSEBa8=pntxQGd91cs/cJxwhB8oE+R5AUZhgVNbwcoN9gqCTT0=; pgv_si=s7673961472; cert=i8Sn0rZrWREyw9vQ7Dy3lL8QFl_DvnKu; openid2ticket_o5Hant8S0cHBbTqeLCCDelVl83n4=S9UO1+MgVfTY9Mv1hpTclunojUWqhqmwpaHxwPCYfQY=; openid2ticket_oFA2u5s0xhk7q726gwl1xM8W02DE=RXguz21E3/RIo0A2hDhXk5V9bmccxY70CChBc/nmRUA=; openid2ticket_oxceTjoJ4X8uuBevrYSA26WnDgew=EKwQ7bZZzbNMGKnppE+ux4q3oWioXVSyxsM0qb9yDM4=; rewardsn=; wxtokenkey=777; sig=h01a7d1f0d9c02e2b0fc48eda0e48f168898bc121a01b1ddb37b731c212b60cae35c4d931df6a842cb6; uuid=0428ffa9073996f0d71ee92b73f7c76f; bizuin=3258157885; ticket=181f865c31655b4d3cb5d344f47f31fc4d4c987c; ticket_id=gh_7c125c1246e8; data_bizuin=3258157885; data_ticket=ELvXgOdFRtPgocIQ/26Va9f6vpFQSMtLgxYtgA4PI8lcO9ugXuLnYQwQh8LL5JST; slave_sid=QVJYQTdyaGFHQ2RoVUJlaHNXRFl6ekNyTFVkOVFDYWtsMFo1VV9aT0FfU05EOW5xdmJTZVdsQ2ZvSUVQeFROZ01oRk1ZbUdQVDYxUVZsalVhMnNKQkkzYjB3NUgwRFpzRnlWdWJ1dHJ2SEZfRlRPaGt1eUM1d2VvR2lGemZTdEVtU0U1eWkxOWt1QVlHb1hW; slave_user=gh_7c125c1246e8; xid=9d0d87beb0ab0be0db980dbe2c570fd9; openid2ticket_oPYszwvDXjjrv2yqUbLkM-nmjFPc=cX1n3WVCqUMVCjutMOcqpwjwRjrvKvTFH5uYN7VwpQs='
WECHAT_FAKE_STOCKDAYS = 0


# kafka 相关信息及配置
KAFKA_HOSTS = 'zqhd1:9092,zqhd2:9092,zqhd3:9092'
KAFKA_TOPIC_ARTICLE = 'tianshu_article'
KAFKA_TOPIC_PIYAO_ARTICLE = 'tianshu_piyao'
RESET_OFFSET_ON_START = True

# 设置日志
LOG_LEVEL = 'INFO'

HTTPERROR_ALLOWED_CODES = [503, 400]