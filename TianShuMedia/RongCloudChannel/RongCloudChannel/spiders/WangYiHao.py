# -*- coding: utf-8 -*-
import scrapy


class WangyihaoSpider(scrapy.Spider):
    name = 'WangYiHao'
    channel_id = '网易号'

    vid = "VZQ286CKP"
    videoUrl = 'https://gw.m.163.com/nc-gateway/api/v1/video/detail/{}'  #json
    tid = "EVNRO15405468U2Q"
    articalUrl = 'https://dy.163.com/v2/article/detail/{}.html' #html parse
