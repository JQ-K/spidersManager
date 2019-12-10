# -*- coding: utf-8 -*-
import scrapy
import time
import json

from OwhatLab.conf.configure import *
from OwhatLab.utils.myredis import RedisClient
from OwhatLab.items import OwhatLabShopProductItem


class SpiderShopsInfoSpider(scrapy.Spider):
    name = 'spider_shops_info'
    allowed_domains = ['appo4.owhat.cn']
    start_urls = ['http://appo4.owhat.cn/']

    # 首页url：PreUrl + listMainUrl
    PreUrl = "https://appo4.owhat.cn/api?"

    flag1 = 0


    # jalouse频道首页--该频道只有一个用户user_id=8244418,s所以无需遍历整个list直接赋值user_id即可
    # 用户详情页--商品类信息ur;：
    #shopMainUrl = "apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m=home&cmd_s=userindex&data=%7B%22goodssort%22%3A1%2C%22ascordesc%22%3A0%2C%22userid%22%3A{}%2C%22pagenum%22%3A{}%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575256927.646932&v=1.0"

    # "apiv=1.0.0&client=%7B%22platform%22%3A%22ios%22%2C%22deviceid%22%3A%22E1DBCBDA-629A-4491-98BC-39B8DFEC248C%22%2C%22channel%22%3A%22AppStore%22%2C%22version%22%3A%221.2.2L%22%7D&cmd_m=home&cmd_s=userindex&data=%7B%22userid%22%3A%228244418%22%2C%22tabtype%22%3A2%2C%22pagenum%22%3A%221%22%2C%22pagesize%22%3A%2220%22%7D&requesttimestap=1575283078.534425&v=1.0"

    # 爬虫步骤： 先对具体某个频道的主页url进入找到内容list，每页显示20条，可以翻页展示-----再对list中的每一项找到对应的user_id-------然后在ArticleMainUrl中传入user_id参数，抓取该用户的全部文章信息


    def __init__(self):
        # connect redis
        self.redisClient = RedisClient.from_settings(DB_CONF_DIR)
        new_CHANNEL_CONF = json.dumps(CHANNEL_CONF)
        self.redisClient.put("CHANNEL_CONF", new_CHANNEL_CONF, None, False)

        self.shop_set_key = REDIS_KEY['shop_id']

        channelJsonStr = self.redisClient.get("CHANNEL_CONF", -1)
        self.channelDict = json.loads(channelJsonStr)
        # print(self.channelDict)
        print('Owhat商品信息爬虫开始...')


    def start_requests(self):
        for value in self.channelDict.values():
            if value['itemIndex'] in ['2', '3', '4', '6', '7', '8']:
                self.flag1 = 1
                curPage = 1
                cmd_m = value['cmd_m']
                cmd_s = value['cmd_s']
                itemIndex = value['itemIndex']
                columnid = str(value['columnid'])
                apiv = value['apiv']

                while curPage > 0 and self.flag1 == 1 and curPage < 81:
                    # print('curPage:', curPage)
                    print('商品信息抓取：正在抓取itemIndex={}，频道={}，第{}页内容...'.format(itemIndex, columnid, curPage))
                    if itemIndex == 2:
                        tempUrl = apiv.format(cmd_m, cmd_s, itemIndex, columnid, curPage)
                    else:
                        tempUrl = apiv.format(cmd_m, cmd_s, columnid, itemIndex, curPage)
                    curPage += 1
                    listUrl = self.PreUrl + tempUrl
                    print('商品信息抓取listUrl：', listUrl)
                    time.sleep(5)
                    yield scrapy.Request(listUrl, method='POST',  # headers=self.headers,
                                        callback=self.parseListUrl)
            else:
                continue


    def parseListUrl(self, response):
        # print(response.text)
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        content = rltJson['data']
        if content == "":
            print('get list interface error: ' + response.text)
            return
        videoList = content['list']
        # print('videoList内容：', videoList)
        if len(videoList) > 0:
            for videoInfo in videoList:
                if 'shopmaxprice' in videoInfo:
                    shop_id = videoInfo['entityid']
                    # print(shop_id)
                    flag = self.redisClient.sismember(self.shop_set_key, shop_id)
                    if flag == 1:
                        # print('该用户信息已爬虫，不再重复爬取')
                        continue
                    else:
                        self.redisClient.sadd(self.shop_set_key, shop_id)
                        yield self.getShopInfoItem(videoInfo)  # 此处yield函数不可少
                else:
                    continue
        else:
            # print('该频道主页内容的商品爬虫已完毕！')
            self.flag1 = 0
            return


    def getShopInfoItem(self, shop):
        shopItem = OwhatLabShopProductItem()

        if 'entityid' in shop:
            shopItem['shop_id'] = shop['entityid']
        if 'publishtime' in shop:
            shopItem['publish_time'] = str(shop['publishtime'])[0:10]
        if 'title' in shop:
            shopItem['title'] = shop['title']
        if 'entityimgurl' in shop:
            shopItem['shop_imgurl'] = shop['entityimgurl']
        if 'columnid' in shop:
            shopItem['column_id'] = shop['columnid']
        if 'columnname' in shop:
            shopItem['column_name'] = shop['columnname']
        if 'shopmaxprice' in shop:
            shopItem['shop_max_price'] = shop['shopmaxprice']
        if 'shopminprice' in shop:
            shopItem['shop_min_price'] = shop['shopminprice']
        if 'shopsaletotal' in shop:
            shopItem['shop_sale_total'] = shop['shopsaletotal']
        if 'publisherid' in shop:
            shopItem['publisher_id'] = shop['publisherid']
        if 'publishername' in shop:
            shopItem['publisher_name'] = shop['publishername']
        if 'publisheravatarimg' in shop:
            shopItem['publisher_pic_url'] = shop['publisheravatarimg']

        if 'columnid' not in shop:
            shopItem['column_id'] = "未知"
        if 'columnname' not in shop:
            shopItem['column_name'] = "未知"

        shopItem['update_time'] = time.time()

        print('shopItem：', shopItem)

        return shopItem  # 此处必须用return返回
