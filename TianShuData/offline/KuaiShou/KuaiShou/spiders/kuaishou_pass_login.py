# -*- coding: utf-8 -*-
import scrapy
import json


class KuaishouPassLoginSpider(scrapy.Spider):
    name = 'kuaishou_pass_login'

    # allowed_domains = ['id.kuaishou.com/pass/kuaishou/login/phone']
    # start_urls = ['https://id.kuaishou.com/pass/kuaishou/login/phone/']

    def start_requests(self):
        start_url = 'https://id.kuaishou.com/pass/kuaishou/login/phone'
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Length": "95",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "id.kuaishou.com",
            "Origin": "https://live.kuaishou.com",
            "Referer": "https://live.kuaishou.com/v/hot/"
        }
        formdata = {
            "sid": "kuaishou.live.web",
            "countryCode": "+86",
            "phone": "18758879865",
            "kwaiId": "",
            "password": "112723",
            "captchaToken": ""
        }



        yield scrapy.FormRequest(start_url, method='POST',
                                 headers=headers,
                                 formdata=formdata, callback=self.parse,
                                 )
        pass

    def parse(self, response):
        print(response.text)
        pass
