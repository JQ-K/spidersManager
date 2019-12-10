# -*- coding: utf-8 -*-

# db conf file path
#DB_CONF_DIR = "D:/gitPython/spidersManager/conf"
DB_CONF_DIR = "/data/code/crawlab-master/spiders/conf"

# user info save dir
#dir = "/data/code/crawlab-master/data/0_kuaikanmanhua/bbs_user_info/"

REDIS_KEY = {
    "channel_conf": "OwhatLab_CHANNEL_CONF_JSON_STR",
    "user_id": "OwhatLab_USER_ID_SET",
    "shop_id": "OwhatLab_SHOP_ID_SET",
    "article_id": "OwhatLab_ARTICLE_ID_SET"
}


#    "Model": {'cmd_m': 'findarticlelist', 'cmd_s': 'community.article','itemIndex':'9','columnid':'22,23,24,25',"apiv":"apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m={}&cmd_s={}&data=%7B%22columnid%22%3A%22{}%22%2C%22itemIndex%22%3A{}%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575362381.760970&v=1.0"},

CHANNEL_CONF = {
    "Model": {'cmd_m': 'findarticlelist', 'cmd_s': 'community.article','itemIndex':'9','columnid':'22,23,24,25',"apiv":"apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m={}&cmd_s={}&data=%7B%22columnid%22%3A%22{}%22%2C%22itemIndex%22%3A{}%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575362381.760970&v=1.0"},
    "Activity": {'cmd_m': 'findarticlelist', 'cmd_s': 'community.article','itemIndex':'10','columnid':'29',"apiv":"apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m={}&cmd_s={}&data=%7B%22columnid%22%3A%22{}%22%2C%22itemIndex%22%3A{}%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575362495.286659&v=1.0"},
    "News": {'cmd_m': 'findarticlelist', 'cmd_s': 'community.article','itemIndex':'11','columnid':'32,12',"apiv":"apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m={}&cmd_s={}&data=%7B%22columnid%22%3A%22{}%22%2C%22itemIndex%22%3A{}%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575362549.542109&v=1.0"},
    "NewsLife": {'cmd_m': 'findarticlelist', 'cmd_s': 'community.article', 'itemIndex': '12', 'columnid': '27',"apiv":"apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m={}&cmd_s={}&data=%7B%22columnid%22%3A%22{}%22%2C%22itemIndex%22%3A{}%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575362597.893096&v=1.0"},

    "Star": {'cmd_m': 'findshoplistv6', 'cmd_s': 'shop.goods', 'itemIndex': '3', 'columnid': '4,5,12,13',"apiv":"apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m={}&cmd_s={}&data=%7B%22pinpaiidstr%22%3A%22%22%2C%22columnidstr%22%3A%22{}%22%2C%22itemIndex%22%3A{}%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575362065.485564&v=1.0"},
    "MZ": {'cmd_m': 'findshoplistv6', 'cmd_s': 'shop.goods', 'itemIndex': '4', 'columnid': '28',"apiv":"apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m={}&cmd_s={}&data=%7B%22pinpaiidstr%22%3A%22%22%2C%22columnidstr%22%3A%22{}%22%2C%22itemIndex%22%3A{}%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575362128.461141&v=1.0"},
    "Eat": {'cmd_m': 'findshoplistv6', 'cmd_s': 'shop.goods', 'itemIndex': '6', 'columnid': '63',"apiv":"apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m={}&cmd_s={}&data=%7B%22pinpaiidstr%22%3A%22%22%2C%22columnidstr%22%3A%22{}%22%2C%22itemIndex%22%3A{}%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575362174.399443&v=1.0"},
    "Sport": {'cmd_m': 'findshoplistv6', 'cmd_s': 'shop.goods', 'itemIndex': '7', 'columnid': '204，208,255,256,257,295,296,297,52',"apiv":"apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m={}&cmd_s={}&data=%7B%22pinpaiidstr%22%3A%22%22%2C%22columnidstr%22%3A%22{}%22%2C%22itemIndex%22%3A{}%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575362300.834321&v=1.0"},
    "Life": {'cmd_m': 'findshoplistv6', 'cmd_s': 'shop.goods', 'itemIndex': '8', 'columnid': '47',"apiv":"apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m={}&cmd_s={}&data=%7B%22pinpaiidstr%22%3A%22%22%2C%22columnidstr%22%3A%22{}%22%2C%22itemIndex%22%3A{}%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575362338.905392&v=1.0"},
    "GyShop":{'cmd_m': 'findcharitypagelist6', 'cmd_s': 'index', 'itemIndex': '2', 'columnid': '4',"apiv":"apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m={}&cmd_s={}&data=%7B%22itemIndex%22%3A{}%2C%22charitytype%22%3A{}%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575601181.215219&v=1.0"},
    "GyArticle": {'cmd_m': 'findcharitypagelist6', 'cmd_s': 'index', 'itemIndex': '2', 'columnid': '5',"apiv": "apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m={}&cmd_s={}&data=%7B%22itemIndex%22%3A{}%2C%22charitytype%22%3A{}%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575601181.215219&v=1.0"},
    "JA": {'cmd_m': 'findarticlelist','cmd_s': 'community.article','itemIndex':'1','columnid':'42',"apiv":"apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m={}&cmd_s={}&data=%7B%22columnid%22%3A%22{}%22%2C%22itemIndex%22%3A{}%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575361934.786107&v=1.0"}
}

