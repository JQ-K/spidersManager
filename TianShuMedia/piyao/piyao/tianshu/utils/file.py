#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'

import os


def read_cnt(iPath, slice_i, split_key=','):
    """
    指定文件每行按指定分隔符号分隔后，获取指定列
    :param iPath:
    :param slice_i:
    :param split_key:
    :return:
    """
    try:
        if os.path.exists(iPath):
            f = open(iPath, 'r')
            rows = f.readlines()
            row_key_list = [row.split(split_key)[slice_i].replace('\n','') for row in rows]
            f.close()
        else:
            row_key_list = []
    except:
        row_key_list = []
    finally:
        return row_key_list


def write_cnt(wlist, ipath, split_key=','):
    """
    指定的文件按某分隔符号写入内容
    :param wlist:
    :param ipath:
    :param split_key:
    :return:
    """
    row = split_key.join(str(para) for para in wlist) + '\n'
    f = open(ipath, 'a+')
    f.write(row)
    f.close()



def para_isexists_file(path,para,slice_i=0,split_str="|||"):
    """
    判断指定内容是否存在文件中
    :param path:
    :param para:
    :param slice_i:
    :param split_str:
    :return:
    """
    if os.path.exists(os.path.dirname(path)) == False:
        os.makedirs(os.path.dirname(path))
    # 判断是否已经抓取
    if os.path.exists(path):
        infos = read_cnt(path, slice_i, split_str)
        if str(para) in infos:
            return True
    return False