#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'


import os
import requests
import re
from fontTools.ttLib import TTFont
from requests.exceptions import RequestException

requests.packages.urllib3.disable_warnings()

font_map = {
    (0, 0, 0, 0): ' ',
    (729, 526, -6, 32): '0',
    (726, 363, 13, 98): '1',
    (732, 527, 13, 32): '2',
    (730, 525, -6, 25): '3',
    (731, 536, 13, 26): '4',
    (717, 526, -5, 33): '5',
    (732, 530, -5, 39): '6',
    (717, 536, 13, 38): '7',
    (731, 525, -7, 33): '8',
    (730, 521, -7, 37): '9',
}


def decrypt_font(charater, mapping):
    """ 解密单个字符，如果可以解密就输出解密后的数字，否则原样返回"""
    s = charater.encode('unicode_escape').decode().strip('\\').upper().strip('U')
    res = mapping.get(s)
    return res if res else charater


def get_number_offset(c, max_offset=20):
    """ 根据偏移量计算映射出来的数字 """
    number = None
    # i, j 分别代表y和x的偏移量
    for i in range(max_offset+1):
        for j in range(max_offset+1):
            # 正向偏移
            number = font_map.get((c.yMax+i, c.xMax+j, c.yMin+i, c.xMin+j))
            if number:
                # print('offset x:{} y:{}'.format(i,j))
                return number
            # 负向偏移
            number = font_map.get((c.yMax-i, c.xMax-j, c.yMin-i, c.xMin-j))
            if number:
                # print('offset x:{} y:{}'.format(i,j))
                return number
    return number


def create_mapping(font_file):
    """ 打开字体文件并创建字符和数字之间的映射. """
    # 打开字体文件，加载glyf
    font = TTFont(font_file)
    glyf = font.get('glyf')
    current_map = {}
    # 创建当前字体文件的数字映射
    for i in glyf.keys():
        # 忽略不是uni开头的字符
        if not i.startswith('uni'):
            continue
        c = glyf[i]
        number = get_number_offset(c)
        # 发现有字符不在已有的集合中, 抛出异常.
        if number is None:
            print((c.yMax, c.xMax, c.yMin, c.xMin))
            raise Exception
        current_map[i.strip('uni')] = number
    # print(json.dumps(current_map, indent=4))
    return current_map


def decrypt_str(s, mapping):
    """ 解密字符串， 不需要解密的部分原样返回 """
    res = ''
    for c in s:
        res = res + decrypt_font(c, mapping)
    return res

def get_mapping(page):
    m = re.search('(http.*?.woff)', page)
    # print(m)
    # print(m.group(1))
    if m:
        woff_link = m.group(1)
        headers1 = {
            'Host': "static.yximgs.com",
            'Connection': "keep-alive",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cache-Control': "no-cache",
            'Postman-Token': "0d97a0b9-6e4d-4eb4-8192-8cf365f77ef6,ca4b1512-7916-4238-8c94-7b1afb3fad56",
            'cache-control': "no-cache"
        }
        woff_res = requests.get(woff_link, headers=headers1, verify=False)
        file_name = woff_link.split('/')[-1]
        with open(file_name, 'wb') as f:
            f.write(woff_res.content)
        mapping = create_mapping(file_name)
        os.remove(file_name)
        return mapping


def kuaishou_decoder(url, str):
    headers = {
        "Host": "live.kuaishou.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        'Cookie': 'did=web_d54ea5e1190a41e481809b9cd17f92aa; didv=1574056613000; clientid=3; client_key=65890b29; kuaishou.live.bfb1s=477cb0011daca84b36b3a4676857e5a1; userId=1537755176; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAaJugToRJTLfgDSM4JY6TDGIWXSFgsXYAL5vUVlgROHXOQqR0N9chBkFZKS-MFT2fgRLcWwmlgQj3-8aT8aISBY2UR_qdAiOzsG8SRvm2xtiNZd3gAPJSG-ssufpJMhRAQSIFeWDwVse84Rt6fHslyIGYge6ZCwWz-5Y9V014ABmcnrMGJ-t6IlMcEQP-fNt9xif434leuOV4AlQKuDbj8YaEhrHsWfESUHgv806qk-5eqStgCIg1w7uEFYlp5iQsH8xqegbYkRyGuuUAn0JV7PksrO2Z34oBTAB; kuaishou.live.web_ph=6fd3b324201a7554fd20880da29ade8d1458; userId=1537755176'
    }

    r = requests.get(url, headers=headers, verify=False)
    for i in range(3):
        try:
            mapping = get_mapping(r.text)
            break
        except:
            pass
    return decrypt_str(str, mapping)

if __name__ == '__main__':
    # url = 'https://live.kuaishou.com/profile/h952814899'
    # res = kuaishou_decoder(url, '뷝껚.뾮w')
    # url = 'https://live.kuaishou.com/profile/haonan666'
    # res = kuaishou_decoder(url, '믊껻곝꫋.ꯍw')
    url = 'https://live.kuaishou.com/profile/w17861031657'
    res = kuaishou_decoder(url, '믊첬뷊')
    print(res)

