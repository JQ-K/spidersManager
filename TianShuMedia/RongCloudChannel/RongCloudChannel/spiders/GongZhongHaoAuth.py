# -*- coding: utf-8 -*-
import scrapy


class GongzhonghaoauthSpider(scrapy.Spider):
    name = 'GongZhongHaoAuth'

    apiDict = {
        "wechat_auth_list_api": "https://tianshucloud.cn/api/platform/weixin/internalAuthList?",
        "wechat_refresh_taken_api": "https://tianshucloud.cn/api/platform/weixin/refreshToken?",
    }

    secret = 'be9eb337beb1cfefed645084f605838d'
    #auth_list_json = get_json(wechat_auth_list_api, data={'secret': 'be9eb337beb1cfefed645084f605838d'})
    #auth_list_json = get_json(wechat_refresh_taken_api, data={"id": id, 'secret': 'be9eb337beb1cfefed645084f605838d'})

