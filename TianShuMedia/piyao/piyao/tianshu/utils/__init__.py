#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'

import json, os


def get_project_configs(filename):
    try:
        current_path = os.path.abspath(__file__)
        configs_path_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),
                                         'configs/{}'.format(filename))
        if os.path.exists(configs_path_path):
            with open(configs_path_path, 'r', encoding='utf-8') as f:
                jstxt = f.read()
            jstxt = jstxt.replace("\\\\", "/").replace("\\", "/")  # 防止json中有 / 导致无法识别
            jsbd = json.loads(jstxt)
            return jsbd
        else:
            jsbd = {}
    except:
        jsbd = {}
    finally:
        return jsbd


def str_to_bool(str):
    return True if str.lower() == 'ture' else False