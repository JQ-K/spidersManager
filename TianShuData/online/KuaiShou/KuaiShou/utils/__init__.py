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
    n_set = [chr(i) for i in range(48,58)]
    b_char_set = [chr(i) for i in range(65,90)]
    s_char_set = [chr(i) for i in range(97,122)]
    o_char_set = [chr(95),chr(45)]
    total_set = n_set + s_char_set + b_char_set + o_char_set
    value_set = "".join(random.sample(total_set, strlen))
    return value_set