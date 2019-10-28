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


CHANNEL_CONF = {
    "V们": {'feedType': 3, 'targetID': 3},
    "魔道祖师": {'feedType': 8, 'targetID': 14},
}

