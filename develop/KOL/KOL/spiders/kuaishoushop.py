# -*- coding: utf-8 -*-
import scrapy
import json
import time

from KOL.items import KuaiShouShopInfoItem, KuaiShouShopProductItem

class KuaishoushopSpider(scrapy.Spider):
    name = 'kuaishoushop'

    user_id = '8290094'
    #user_id = '2'

    #快手小店评分url
    shopScoreUrl = "https://www.kwaishop.com/rest/app/grocery/ks/shop/score?sellerId={}"
    #快手小店商品列表url
    productUrl = "https://www.kwaishop.com/rest/app/grocery/product/self/midPage/list"

    def start_requests(self):
        yield scrapy.Request(self.shopScoreUrl.format(self.user_id), method='GET',
                             callback=self.parseShopScoreUrl)

        #time.sleep(3)

        bodyDict = {
            'listProductParam': {
                'id': self.user_id,
                'page': 1
            }
        }
        yield scrapy.Request(self.productUrl, method='POST',
                             body=json.dumps(bodyDict), headers={'Content-Type': 'application/json'},
                             callback=self.parseProductUrl,
                             meta={'bodyDict': bodyDict, 'beginFlag': True, 'curPage': 1, 'totalPage': 1})


    def parseShopScoreUrl(self, response):
        # print(response.text)
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        if rltJson['result'] != 1:
            print('get interface error: ' + response.text)
            return
        infoItem = KuaiShouShopInfoItem()
        if 'containTaoBao' in rltJson:
            infoItem['containTaoBao'] = rltJson['containTaoBao']
        if 'userShopScoreView' in rltJson:
            shopInfo = rltJson['userShopScoreView']
            if shopInfo is None:
                return
            if 'shopLogisticsScore' in shopInfo:
                infoItem['shopLogisticsScore'] = shopInfo['shopLogisticsScore']
            if 'shopLogisticsScoreLevel' in shopInfo:
                infoItem['shopLogisticsScoreLevel'] = shopInfo['shopLogisticsScoreLevel']
            if 'shopQualityScore' in shopInfo:
                infoItem['shopQualityScore'] = shopInfo['shopQualityScore']
            if 'shopQualityScoreLevel' in shopInfo:
                infoItem['shopQualityScoreLevel'] = shopInfo['shopQualityScoreLevel']
            if 'shopServiceScore' in shopInfo:
                infoItem['shopServiceScore'] = shopInfo['shopServiceScore']
            if 'shopServiceScoreLevel' in shopInfo:
                infoItem['shopServiceScoreLevel'] = shopInfo['shopServiceScoreLevel']
            if 'totalOrderPayCount' in shopInfo:
                infoItem['totalOrderPayCount'] = shopInfo['totalOrderPayCount']
            if 'validCommentCount' in shopInfo:
                infoItem['validCommentCount'] = shopInfo['validCommentCount']
        print(json.dumps(dict(infoItem)))
        #yield infoItem


    def parseProductUrl(self, response):
        #print(response.text)
        if response.status != 200:
            print('get url error: ' + response.url)
            return
        rltJson = json.loads(response.text)
        if rltJson['result'] != 1:
            print('get interface error: ' + response.text)
            return
        if 'itemSize' not in rltJson:
            return
        else:
            if rltJson['itemSize'] == 0:
                return
        bodyDict = response.meta['bodyDict']
        beginFlag = response.meta['beginFlag']
        curPage = response.meta['curPage']
        totalPage = response.meta['totalPage']

        if beginFlag:
            totalPage = rltJson['pageNum']
            beginFlag = False

        if 'products' not in rltJson:
            return

        products = rltJson['products']
        for product in products:
            productItem = KuaiShouShopProductItem()
            productItem['user_id'] = bodyDict['listProductParam']['id']
            if 'itemId' in product:
                productItem['itemId'] = product['itemId']
            if 'addType' in product:
                productItem['addType'] = product['addType']
            if 'imageUrl' in product:
                productItem['imageUrl'] = product['imageUrl']
            if 'itemLinkUrl' in product:
                productItem['itemLinkUrl'] = product['itemLinkUrl']
            if 'itemTagList' in product:
                productItem['itemTagList'] = product['itemTagList']
            if 'productPrice' in product:
                productItem['productPrice'] = product['productPrice']
            if 'productTitle' in product:
                productItem['productTitle'] = product['productTitle']
            if 'showCoupon' in product:
                productItem['showCoupon'] = product['showCoupon']
            if 'sourceType' in product:
                productItem['sourceType'] = product['sourceType']
            if 'stock' in product:
                productItem['stock'] = product['stock']
            if 'updatetime' in product:
                productItem['updatetime'] = product['updatetime']
            if 'volume' in product:
                productItem['volume'] = product['volume']
            #print(productItem)
            print(json.dumps(dict(productItem)))
            #yield productItem

        curPage += 1
        if curPage <= totalPage:
            bodyDict['listProductParam']['page'] = curPage
            yield scrapy.Request(self.productUrl, method='POST',
                                 body=json.dumps(bodyDict), headers={'Content-Type': 'application/json'},
                                 callback=self.parseProductUrl,
                                 meta={'bodyDict': bodyDict, 'beginFlag': beginFlag, 'curPage': curPage, 'totalPage': totalPage})

