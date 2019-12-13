#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'
import re
import datetime


def SeedsFansPlan(value):
    """
    种子的策略：0-50W ，每3天
              50-100W，每2天
              100W以上，每1天
    :param value: 粉丝数量
    :return: 下次爬虫的日期
    """
    # 计算粉丝数
    fan_value, fan_unit = re.findall('([0-9\.]+)([a-zA-Z]{0,3})', value)[0]
    if fan_unit == '':
        fan_num = int(fan_value)
    elif fan_unit.lower() == 'k':
        fan_num = float(fan_value) * 1000
    elif fan_unit.lower() == 'w':
        fan_num = float(fan_value) * 10000
    elif fan_unit.lower() == 'kw':
        fan_num = float(fan_value) * 10000000
    # 计算间隔天数
    if fan_num < 500000:
        interval = 1
    elif fan_num >= 1000000:
        interval = 3
    else:
        interval = 2
    # 计算下一次执行时间
    today = datetime.datetime.now()
    interval_timedelta = datetime.timedelta(days=interval)
    next_scheduling_date= (today + interval_timedelta).strftime("%Y-%m-%d")
    return next_scheduling_date
