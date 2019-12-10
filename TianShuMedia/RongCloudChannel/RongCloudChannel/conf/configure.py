# -*- coding: utf-8 -*-

###beta
POST_CONF = {
    'url': 'http://beta.rongcloud.zhanqi.tv/api/mcloud/stat/partner/sync_statistics', #beta
    'headers': {
        'content-type': 'application/json',
    },
    'login_error_api': 'http://beta.rongcloud.zhanqi.tv/api/mcloud/stat/partner/change_login', #beta
}
DB_CONF_DIR = "/data/code/crawlab-master/spiders/conf" #beta



###正式
'''POST_CONF = {
    'url': 'https://www.tianshucloud.cn/api/mcloud/stat/partner/sync_statistics', #正式
    'headers': {
        'content-type': 'application/json',
    },
    'login_error_api': 'https://www.tianshucloud.cn/api/mcloud/stat/partner/change_login', #正式
}
DB_CONF_DIR = "/data/code/crawlab/spiders/conf" #正式'''




TB_AUTH_NAME = "mcloud_channel_auth"

ITEM_FILE_PATH = 'D:/py_workspace/spidersManager/RongCloudChannel/RongCloudChannel/test/'

APP_ID = '1001'
SECRET = '7PRxo8QvOV4ebTPygPtQ'
