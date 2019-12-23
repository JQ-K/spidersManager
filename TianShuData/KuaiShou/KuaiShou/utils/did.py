#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'

import requests
import json
import time
import random
from loguru import logger

def ProduceRandomStr(bits):
    """
    获取指定个数的包含大小写字母和数字的字符串
    :param bits:
    :return:
    """
    num_set = [chr(i) for i in range(48,58)]
    b_char_set = [chr(i) for i in range(65,90)]
    s_char_set = [chr(i) for i in range(97,122)]
    total_set = num_set + s_char_set + b_char_set
    value_set = "".join(random.sample(total_set, bits))
    return value_set

def RegisterCookie(cookies):
    payloadHeader = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Length": "1425",
        "Content-Type": "text/plain;charset=UTF-8",
        "Cookie": cookies,
        "Host": "live.kuaishou.com",
        "kpf": "PC_WEB",
        "kpn": "GAME_ZONE",
        "Origin": "https://live.kuaishou.com",
        "Referer": "https://live.kuaishou.com/v/hot/",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"
    }
    time_int = int(time.time() * 1000)
    payloadData = {
        "base": {
            "session_id": ProduceRandomStr(16),
            "page_id": "{}_{}".format(ProduceRandomStr(16),time_int-77777),
            "refer_page_id": "{}_{}".format(ProduceRandomStr(16),time_int-777777),
            "refer_show_id": "",
            "refer_url": "https://live.kuaishou.com/profile/3xbyt4rb5kwkh9w",
            "page_live_stream_id": "",
            "url": "https://live.kuaishou.com/profile/3xbyt4rb5kwkh9w",
            "screen": "1920*1080",
            "platform": "MacIntel",
            "log_time": str(time_int)
        },
        "events": [{
            "type": "pv",
            "data": {
                "event_time": 1012+time_int-157,
                "from": "/",
                "to": "/profile/3xbyt4rb5kwkh9w",
                "is_spammer": "false"
            }
        }, {
            "type": "show",
            "data": {
                "event_time": 1012+time_int-34,
                "show_name": "photo_card",
                "show_value": {
                    "author_id": "3xbyt4rb5kwkh9w",
                    "photo_id": "3xx9w53i9za24ay",
                    "exp_tag": "1_a/0_null"
                },
                "show_index": 6
            }
        }, {
            "type": "show",
            "data": {
                "event_time": 1012+time_int-15,
                "show_name": "photo_card",
                "show_value": {
                    "author_id": "3xbyt4rb5kwkh9w",
                    "photo_id": "3xzks89k5h72fzg",
                    "exp_tag": "1_a/0_null"
                },
                "show_index": 2
            }
        }, {
            "type": "show",
            "data": {
                "event_time": 1012+time_int-14,
                "show_name": "photo_card",
                "show_value": {
                    "author_id": "3xbyt4rb5kwkh9w",
                    "photo_id": "3xsrb32kyxj9f2i",
                    "exp_tag": "1_a/0_null"
                },
                "show_index": 3
            }
        }, {
            "type": "show",
            "data": {
                "event_time": 1012+time_int-2,
                "show_name": "photo_card",
                "show_value": {
                    "author_id": "3xbyt4rb5kwkh9w",
                    "photo_id": "3xzpm5rfm4fcr9s",
                    "exp_tag": "1_a/0_null"
                },
                "show_index": 5
            }
        }, {
            "type": "show",
            "data": {
                "event_time": 1012+time_int-2,
                "show_name": "photo_card",
                "show_value": {
                    "author_id": "3xbyt4rb5kwkh9w",
                    "photo_id": "3xscvj9yt24cjdk",
                    "exp_tag": "1_a/0_null"
                },
                "show_index": 0
            }
        }, {
            "type": "show",
            "data": {
                "event_time": 1012+time_int-2,
                "show_name": "photo_card",
                "show_value": {
                    "author_id": "3xbyt4rb5kwkh9w",
                    "photo_id": "3xfsy9e5azmxibs",
                    "exp_tag": "1_a/0_null"
                },
                "show_index": 1
            }
        }, {
            "type": "show",
            "data": {
                "event_time": 1012+time_int,
                "show_name": "photo_card",
                "show_value": {
                    "author_id": "3xbyt4rb5kwkh9w",
                    "photo_id": "3xrxjtpxspd4y44",
                    "exp_tag": "1_a/0_null"
                },
                "show_index": 4
            }
        }]
    }

    payload_data = {
        "base": {
            "session_id": "5Ev6XLOpPz4JiT8a",
            "page_id": "NifAMuoVt-buUS6s_1576753854624",
            "refer_page_id": "",
            "refer_show_id": "",
            "refer_url": "https://live.kuaishou.com/v/hot/",
            "page_live_stream_id": "",
            "url": "https://live.kuaishou.com/v/hot/",
            "screen": "1280*800",
            "platform": "MacIntel",
            "log_time": "{}".format(time_int)
        },
        "events": [{
            "type": "pv",
            "data": {
                "event_time": time_int-1012,
                "from": "/",
                "to": "/v/hot/",
                "is_spammer": 'false'
            }
        }]
    }

    register_url = 'https://live.kuaishou.com/rest/wd/live/web/log'
    r = requests.post(register_url, data=json.dumps(payload_data), headers=payloadHeader)

    if r.json()['result'] == 1:
        logger.info('Cookies register successed! Cookies:{}'.format(cookies))
        return True
    return False



if __name__ == '__main__':
    cookie = "did=web_94be0eafe9294373803600a07f300cf2; didv=577071729000; kuaishou.live.bfb1s=3e261140b0cf7444a0ba411c6f227d88"
    RegisterCookie(cookie)



