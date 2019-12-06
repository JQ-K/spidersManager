# -*- coding: utf-8 -*-
import scrapy
import json


class KuxuanKolSpider(scrapy.Spider):
    name = 'kuxuan_kol'
    allowed_domains = ['data.kuxuan.com']

    def start_requests(self):
        start_url = 'https://data.kuxuan.com/api/kwai/showList'
        headers = {
            "origin": "https://data.kuxuan.com",
            "referer": "https://data.kuxuan.com/bigData/commodityVersion/",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"
        }
        for i in range(1, 900):
            try:
                data = {"page": i, "admin_id": "86", "ttl": "1574834999", "sign": "8d023248699f73c7d895cd5387ba5113"}

                yield scrapy.Request(
                    start_url, headers=headers, body=json.dumps(data),
                    method='POST', callback=self.parseCommentByPhotoId,
                    meta={'bodyJson': data},
                    cookies=self.getCookie()
                )
            except:
                scrapy.Spider.logger.info("sdff")

    def parse(self, response):
        print(response.text)
