#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'

import requests
import sys, os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from scrapy.utils.project import get_project_settings
from loguru import logger

from tianshu.utils import get_project_configs


def public_record_wechat(record,custom_id):
    api_json = get_project_configs('api.json')
    settings = get_project_settings()
    dev = settings.get('DEV')
    api_dict = api_json[dev]
    try:
        wechat_create_api = api_dict['wechat_create_api']
        logger.info(wechat_create_api)
        record['custom_id'] = custom_id
        record['secret'] = 'be9eb337beb1cfefed645084f605838d'
        create_r = requests.post(wechat_create_api, json=record)
        return create_r.json()
    except Exception as e:
        logger.error("Public fail,error:{}".format(e))
        return {"message": "public fail", "error": e}

def public_record_wechat_piyao(record,custom_id):
    api_json = get_project_configs('api.json')
    settings = get_project_settings()
    dev = settings.get('DEV')
    api_dict = api_json[dev]
    try:
        wechat_create_api = api_dict['wechat_create_api_piyao']
        logger.info(wechat_create_api)
        record['custom_id'] = custom_id
        record['secret'] = 'be9eb337beb1cfefed645084f605838d'
        create_r = requests.post(wechat_create_api, json=record)
        return create_r.json()
    except Exception as e:
        logger.error("Public fail,error:{}".format(e))
        return {"message": "public fail", "error": e}



