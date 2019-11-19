# -*- coding: utf-8 -*-
import scrapy


class KuaishouSpider(scrapy.Spider):
    name = 'kuaishou'
    #host = "https://apinew.gifshow.com"
    listUrl = "https://apinew.gifshow.com/" \
              "rest/n/feed/hot?" \
              "extId=89314196caa21dc7b9e11b9f483754ec&" \
              "lon=120.1698471757097&" \
              "kpf=IPHONE&net=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8_5&" \
              "appver=6.10.1.1242&" \
              "kpn=KUAISHOU&" \
              "c=a&mod=iPhone8%2C1&sys=ios10.3.3&sh=1334&ver=6.10&" \
              "isp=&did=F125510A-A382-4D14-A2C4-F3DC7B50EB9C&" \
              "lat=30.27415585993351&browseType=1&" \
              "sw=750&egid=DFP93EEB903386E6783D08EDF66DDD1E77867C6D4B8263839735A1A77E06F45E&" \
              "__NS_sig3=2154968078c639fa905c955a76db2ea9a00aff3d7e&client_key=56c3713c&" \
              "count=20&country_code=cn&id=20&kuaishou.api_st=&" \
              "language=zh-Hans-CN%3Bq%3D1&needInterestTag=0&pv=false&" \
              "refreshTimes=19&sig=e0f5a96e7bbcb16e23083b5d36a65d54&source=1&" \
              "token=&type=7"

    headers = {
        'Host': 'apinew.gifshow.com',
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'X-REQUESTID': '157274774643478471',
        'Cookie': 'region_ticket=RT_D21FBE64BD7AA1DAEAFD84DFC6609862ED25E581436012F8EDAAE0C1468BC',
        'User-Agent': 'kwai-ios',
        'Accept-Language': 'zh-Hans-CN;q=1',
        'Accept-Encoding': 'gzip, deflate',
    }

    def start_requests(self):
        yield scrapy.Request(self.listUrl, headers=self.headers, method='POST', callback=self.parseListUrl)


    def parseListUrl(self, response):
        print(response.text)

