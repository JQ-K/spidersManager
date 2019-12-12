#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'

import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import urllib,random

from ProxyIP.utils.useragent import UAPOOL

def ProxyAuthentication(url,port_ip):
    try:
        headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                      'User-Agent': random.choice(UAPOOL),
                      'Content-type':'text/html;charset=utf-8'}
        proxy_support = urllib.request.ProxyHandler(port_ip)
        opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        req = urllib.request.Request(url=url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=1)
        status = resp.getcode()
        resp.close()
        if status == 200:
            print(u'代理IP地址{},通过网站:{}的核验!!!!'.format(port_ip, url))
            return port_ip
    except Exception as e:
        print(u'IP:{},未能通过网站:{}的核验!!错误提示:{}'.format(port_ip, url, e))
        return None


if __name__ == '__main__':
    ProxyAuthentication('https://live.kuaishou.com',{'HTTP': '113.161.116.94:8080'})