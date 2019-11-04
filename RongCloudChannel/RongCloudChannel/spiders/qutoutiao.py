# -*- coding: utf-8 -*-
import scrapy

from scrapy.http import FormRequest


class QutoutiaoSpider(scrapy.Spider):
    name = 'QuTouTiao'

# https://qac-qupost.qutoutiao.net/member/login
# https://mp.qutoutiao.net/login


    def start_requests(self):
        return [FormRequest("https://qac-qupost.qutoutiao.net/member/login", method='POST',
                    formdata={"email": "zjtmkj@8531.cn",
                              "password": "zswh2019",
                              "is_secret": "0",
                              "dtu": "200",
                              #"telephone":"",
                              #"keep":"",
                              #"captcha":"",
                              #"source":"0",
                              #"k":"",
                              #"token":"undefined",
                              }, callback=self.parse1)]


    def parse1(self, response):
        print(response.url)
        print(response.text)
