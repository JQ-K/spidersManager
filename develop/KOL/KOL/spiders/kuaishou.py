# -*- coding: utf-8 -*-
import scrapy
import json
import time

from KOL.items import KuaiShouUserIterm;

class KuaishouSpider(scrapy.Spider):
    name = 'kuaishou'

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

    userUrl = "https://apinew.gifshow.com/" \
              "rest/n/user/profile/" \
              "adBusiness?lon=120.1698587728025&kpf=IPHONE&" \
              "net=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8_5&" \
              "appver=6.10.1.1242&isp=&c=a&kpn=KUAISHOU&mod=iPhone8%2C1&sh=1334&" \
              "ver=6.10&sys=ios10.3.3&" \
              "did=F125510A-A382-4D14-A2C4-F3DC7B50EB9C&" \
              "lat=30.27413144385589&ud=1577168521&" \
              "sw=750&browseType=1&" \
              "egid=DFP93EEB903386E6783D08EDF66DDD1E77867C6D4B8263839735A1A77E06F45E&" \
              "__NS_sig3=2154973388c60b2c90cfa66db783d88e81af6ff210&" \
              "__NStokensig=6393c737583112709b7f6834da10cf314aacfb97b76e738f6b15c17156d5638a&" \
              "client_key=56c3713c&country_code=cn&exp_tag=1_i%2F2000004126832556657_scbf0&" \
              "kuaishou.api_st=Cg9rdWFpc2hvdS5hcGkuc3QSoAEi6ieXaXEajKxOBAI5uqprumkDesnyBN_eVTY7wN5B1dUFs-jECeFTz-YILxOncjYR3dTAaOgwwxzz0CxyKj6QTfFwF9rdy-e_B3BqHBhkereZhy9TMuebj0wELxlUZTDeQN8-JP1P42dVlJaNMnBt1FguPKHYfk1bJ0IHdtYsRY2FSfQTNuXotRk9Mogfv_BnQgIHCc0eZRV5KDgJWSRJGhJDuMiqtgZPubHrzEMdgDufEMEiIBLMIJkt0X0A-met9wYLP-xEmSaRD9S-lWPTAvBjxImjKAUwAQ&language=zh-Hans-CN%3Bq%3D1&pv=1&sig=6cb58cb420cd91af04350ce45ba9a04c&token=58cc04a5b35d446c9d16e65e991214e7-1577168521&" \
              "user={}"

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
        yield scrapy.Request(self.listUrl, headers=self.headers, method='POST',
                             callback=self.parseListUrl)


    def parseListUrl(self, response):
        #print(response.text)
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        videoList = rltJson['feeds']
        for videoInfo in videoList:
            '''userItem = KuaiShouUserIterm()
            userItem['user_id'] = videoInfo['user_id']  #此处只取user_id即可
            userItem['user_name'] = videoInfo['user_name']
            userItem['user_sex'] = videoInfo['user_sex']
            yield userItem'''
            user_id = videoInfo['user_id']
            time.sleep(1)
            yield scrapy.Request(self.userUrl.format(user_id), headers=self.headers, method='POST',
                                 callback=self.parseUserInfoUrl)



    def parseUserInfoUrl(self, response):
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        print(response.text)


