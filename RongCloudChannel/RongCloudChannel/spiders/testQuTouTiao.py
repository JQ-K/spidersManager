# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

class TestqutoutiaoSpider(scrapy.Spider):
    name = 'testQuTouTiao'
    dtu = "200"
    loginUrl = "https://qac-qupost.qutoutiao.net/member/login"

    def start_requests(self):
        user = "15802103561"
        formdata = {"password": "qtt123456", "is_secret": "0", "dtu": self.dtu, }
        if user.find("@") > 0:
            formdata["email"] = user
        else:
            formdata["telephone"] = user
            formdata["source"] = "1"
        # print(formdata)
        yield FormRequest(self.loginUrl, method='POST',
                          formdata=formdata, callback=self.parseLoginPage, meta={'formdata': formdata})

    def parseLoginPage(self, response):
        print(response.text)
