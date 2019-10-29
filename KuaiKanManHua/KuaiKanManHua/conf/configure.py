# -*- coding: utf-8 -*-

# Redis配置
redisHost = '10.8.26.26'
redisPort = 6379
redisDb = 1

#
redis_id_set_name = "KuaiKanManHuaBbsID"

# user info save dir
dir = "/data/code/crawlab-master/data/0_kuaikanmanhua/bbs_user_info/"


REDIS_CONF = {
    "host": "10.8.26.26",
    "port": 6379,
    "db": 1,
    #"expire": 60 * 60 * 24 * 5,
}

REDIS_KEY = {
    "channel_conf": "KuaiKanManHua_CHANNEL_CONF_JSON_STR",
    "user_id": "KuaiKanManHua_USER_ID_SET",
}

CHANNEL_CONF = {
    "V们": {'feedType': 3, 'targetID': 3},
    "魔道祖师": {'feedType': 8, 'targetID': 14},
    "同人": {'feedType': 8, 'targetID': 32},
    "影视": {'feedType': 8, 'targetID': 33},
    "手作": {'feedType': 8, 'targetID': 37},
    "游戏": {'feedType': 8, 'targetID': 34},
    "声控": {'feedType': 7, 'targetID': 9},
    "时尚": {'feedType': 8, 'targetID': 36},
    "推荐": {'feedType': 2, 'targetID': 2},
}

