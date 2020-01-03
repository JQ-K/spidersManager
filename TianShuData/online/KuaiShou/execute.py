#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'

import os

# execute(['scrapy', 'crawl', 'kuaishou_test'])
# execute(['scrapy', 'crawl', 'kuxuan_kol_user'])
# execute(['scrapy', 'crawl', 'kuaishou_user_photo_info'])
# execute(['scrapy', 'crawl', 'kuaishou_user_info'])
# execute(['scrapy', 'crawl', 'kuaishou_photo_comment'])
# execute(['scrapy', 'crawl', 'kuaishou_cookie_info'])

def spider_run(spider_name):
    path = os.path.dirname(os.path.realpath(__file__))
    os.system("cd {} && nohup scrapy crawl {} >> /dev/null 2>&1 &".format(path,spider_name))




if __name__ == '__main__':
    spider_run('kuaishou_test')
