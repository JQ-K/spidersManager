# -*- coding: utf-8 -*-

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
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

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

# log
LOG_LEVEL = 'INFO'

# kafka 相关信息及配置
KAFKA_HOSTS = 'zqhd1:9092,zqhd2:9092,zqhd3:9092'
# TOPIC = 'tianshu_kuaishou'
KAFKA_TOPIC = 'tianshu_test'
# 设置TOPIC是否从头消费
RESET_OFFSET_ON_START = True

# spider cookie value num
SPIDER_COOKIE_CNT = 10

# graphql
USER_INFO_QUERY = {
    "operationName": "userInfoQuery",
    "variables": {
        "principalId": "{%s}"
    },
    "query": "query userInfoQuery($principalId: String) {\n  userInfo(principalId: $principalId) {\n    id\n    principalId\n    kwaiId\n    eid\n    userId\n    profile\n    name\n    description\n    sex\n    constellation\n    cityName\n    living\n    watchingCount\n    isNew\n    privacy\n    feeds {\n      eid\n      photoId\n      thumbnailUrl\n      timestamp\n      __typename\n    }\n    verifiedStatus {\n      verified\n      description\n      type\n      new\n      __typename\n    }\n    countsInfo {\n      fan\n      follow\n      photo\n      liked\n      open\n      playback\n      private\n      __typename\n    }\n    bannedStatus {\n      banned\n      defriend\n      isolate\n      socialBanned\n      __typename\n    }\n    __typename\n  }\n}\n"
}
USER_PHOTO_QUERY = {
    "operationName": "publicFeedsQuery",
    "variables": {
        "principalId": "{%s}",
        "pcursor": "0",
        "count": 200
    },
    "query": "query publicFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  publicFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    live {\n      user {\n        id\n        kwaiId\n        eid\n        profile\n        name\n        living\n        __typename\n      }\n      watchingCount\n      src\n      title\n      gameId\n      gameName\n      categoryId\n      liveStreamId\n      playUrls {\n        quality\n        url\n        __typename\n      }\n      followed\n      type\n      living\n      redPack\n      liveGuess\n      anchorPointed\n      latestViewed\n      expTag\n      __typename\n    }\n    list {\n      photoId\n      caption\n      thumbnailUrl\n      poster\n      viewCount\n      likeCount\n      commentCount\n      timestamp\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      width\n      height\n      user {\n        id\n        eid\n        name\n        profile\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"
}
PHOTO_COMMENT_QUERY = {
    "operationName": "commentListQuery",
    "variables": {
        "pcursor": "0",
        "photoId": "3xz7aiwh5tgc3x9",
        "count": 200
    },
    "query": "query commentListQuery($photoId: String, $page: Int, $pcursor: String, $count: Int) {\n  shortVideoCommentList(photoId: $photoId, page: $page, pcursor: $pcursor, count: $count) {\n    commentCount\n    realCommentCount\n    pcursor\n    commentList {\n      commentId\n      authorId\n      authorName\n      content\n      headurl\n      timestamp\n      authorEid\n      status\n      subCommentCount\n      subCommentsPcursor\n      likedCount\n      liked\n      subComments {\n        commentId\n        authorId\n        authorName\n        content\n        headurl\n        timestamp\n        authorEid\n        status\n        replyToUserName\n        replyTo\n        replyToEid\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
}

# REDIS配置信息
REDIS_HOST = 'zqhd5'
REDIS_PORT = 6379
REDIS_DID_NAME = 'tianshu_did'
