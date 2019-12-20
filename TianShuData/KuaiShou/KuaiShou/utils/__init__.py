#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'

import random

def ProduceRandomStr(strlen):
    """
    获取指定个数的包含大小写字母和数字的字符串
    :param bits:
    :return:
    """
    num_set = [chr(i) for i in range(48,58)]
    b_char_set = [chr(i) for i in range(65,90)]
    s_char_set = [chr(i) for i in range(97,122)]
    total_set = num_set + s_char_set + b_char_set
    value_set = "".join(random.sample(total_set, strlen))
    return value_set