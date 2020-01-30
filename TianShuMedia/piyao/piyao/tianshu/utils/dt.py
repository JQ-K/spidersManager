#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'

import time
from datetime import datetime
from loguru import logger


def string_to_timestamp(dt_str, dt_type):
    return time.mktime(time.strptime(dt_str, dt_type))


def compute_time_interval(dt_sub, dt_sub_end):
    """
    计算时间间隔
    :param dt_sub:
    :param dt_sub_end:
    :param dt_type:
    :return:
    """
    try:
        if type(dt_sub) == int:
            "时间戳转时间"
            dt_sub_array = time.localtime(dt_sub)
            dt_sub_str = time.strftime("%Y-%m-%d %H:%M:%S", dt_sub_array)
            dt_sub_fomat = datetime.strptime(dt_sub_str, '%Y-%m-%d %H:%M:%S')

        else:
            "字符串转时间"
            dt_sub_str = dt_sub
            dt_sub_fomat = datetime.strptime(dt_sub_str, '%Y-%m-%d %H:%M:%S')

        if type(dt_sub_end) == int:
            "时间戳转时间"
            dt_sub_end_array = time.localtime(dt_sub_end)
            dt_sub_end_str = time.strftime("%Y-%m-%d %H:%M:%S", dt_sub_end_array)
            dt_sub_end_fomat = datetime.strptime(dt_sub_end_str, '%Y-%m-%d %H:%M:%S')
        else:
            "字符串转时间"
            dt_sub_end_str = dt_sub_end
            dt_sub_end_fomat = datetime.strptime(dt_sub_end_str, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        logger.error("Error, Time format is invaild, {} ".format(e))

    return (dt_sub_fomat - dt_sub_end_fomat).total_seconds(), dt_sub_str, dt_sub_end_str
