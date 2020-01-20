## 快手爬取字段说明文档



###1.快手用户信息字段表

| 字段          | 字段名称                             |
| ------------- | ------------------------------------ |
| kwaiId        | 快手号                               |
| userId        | 快手id                               |
| principalId   | 随机唯一id，又称作eid等              |
| name          | 昵称                                 |
| sex           | 性别                                 |
| description   | 简介                                 |
| profile       | 头像地址                             |
| homepage      | 个人主页                             |
| cityCode      | 邮编                                 |
| cityName      | 城市                                 |
| constellation | 星座                                 |
| varified      | 认证情况                             |
| collect       | 收藏数                               |
| fan           | 粉丝数                               |
| follow        | 关注数                               |
| liked         | 点赞数                               |
| photo         | 作品数                               |
| private       | ?                                    |
| userTags      | 用户标签，非原始字段，需后期人工添加 |

###2.快手用户作品信息表

| 字段           | 字段名                               |
| -------------- | ------------------------------------ |
| photoId        | 作品的ID                             |
| poster         | 封面                                 |
| name           | 作者名称                             |
| displayView    | 播放数                               |
| displayLike    | 收藏数                               |
| displayComment | 评论数                               |
| caption        | 文字说明，描述/标题的意思            |
| photoTags      | 作品标签，非原始字段，需后期人工添加 |

###3.快手小店信息表

| 字段                    | 字段名称             |
| ----------------------- | -------------------- |
| user_id                 | 快手id               |
| containTaoBao           | 淘宝是否有           |
| shopLogisticsScore      | 商品Logistic评分     |
| shopLogisticsScoreLevel | 商品Logistic评分等级 |
| shopQualityScore        | 商品质量评分         |
| shopQualityScoreLevel   | 商品质量评分等级     |
| shopServiceScore        | 服务态度评分         |
| shopServiceScoreLevel   | 服务态度评分等级     |
| totalOrderPayCount      | 总订单数             |
| validCommentCount       | 订单有效评论数       |

###4.快手小店商品信息表

| 字段         | 字段名称           |
| ------------ | ------------------ |
| user_id      | 快手id             |
| itemId       | 商品id             |
| nickName     | 店名               |
| imageUrl     | 商品图片url        |
| itemLinkUrl  | 商品url            | 
| itemTagList  | 商品标签           |
| productPrice | 商品价格，单位：分 |
| productTitle | 商品标题           |
| showCoupon   | 是否展示优惠券     |
| sourceType   | 来源类型           |
| stock        | 库存               |
| updatetime   | 更新时间           |
| volume       | 销量               |


####爬虫采集并发送kafka结果队列的数据json样例：
1. 每日用户统计信息更新接口 kuaishou_search_overview  spider采集样例：
{'avatar': 'https://js2.a.yximgs.com/uhead/AB/2019/09/11/22/BMjAxOTA5MTEyMjU2NTlfNjgxMzcxMF8xX2hkNjM0Xzk1Mg==_s.jpg', 
   'description': '', 'fan': '1778.7w', 'follow': '368', 'is_successed': 1, 
   'nickname': '浩南 'photo': '53', 'principalId': 'haonan666', 'sex': 'M', 
   'spider_datetime': '2020-01-14 10:43:31', 'spider_name': 'kuaishou_search_overview', 
   'userId': 6813710
}
   
2. 小店首页整体统计信息：
{
	'shopInfo': {
		'containTaoBao': False,
		'result': 1,
		'userShopScoreView': {
			'shopLogisticsScore': 4.6186886,
			'shopLogisticsScoreLevel': -1.7,
			'shopQualityScore': 4.683446,
			'shopQualityScoreLevel': 1.6,
			'shopServiceScore': 4.7481937,
			'shopServiceScoreLevel': 1.4,
			'totalOrderPayCount': 338,
			'validCommentCount': 139
		}
	},
	'spider_datetime': '2020-01-15 15:48:02',
	'spider_name': 'kuaishou_shop_score',
	'userId': 144077034
}

3. 小店商品列表单个商品的总览信息
{
	'productId': 56684372034,
	'productInfo': {
		'addType': 0,
		'imageUrl': 'https://ali-ec.static.yximgs.com/ufile/adsocial/1d32f5f6-f983-4f36-a668-3ed0145c9e48.jpg',
		'itemId': 56684372034,
		'itemLinkUrl': 'https://www.kwaishop.com/merchant/shop/detail?id=56684372034',
		'itemTagList': [],
		'productPrice': 338000,
		'productTitle': '男士新款水貂整貂内胆狐狸毛领',
		'showCoupon': False,
		'sourceType': 99,
		'stock': 0,
		'updateTime': 1577547082953,
		'volume': 7
	},
	'spider_datetime': '2020-01-15 16:06:16',
	'spider_name': 'kuaishou_shop_product_list',
	'userId': 144077034
}

4. 小店中单个商品详情页信息
{
	'productDetail': {
		'address': '河北省 衡水市 枣强县',
		'bannerImage': {
			'fontColor': None,
			'picHeight': 0,
			'picUrl': None,
			'picWidth': 0,
			'stretch': None
		},
		'buyerCommentEnable': 1,
		'categoryId': 1003,
		'couponList': None,
		'detailImageUrls': ['https://ali-ec.static.yximgs.com/ufile/adsocial/603595c4-e76e-4a81-a9e7-22c9e9e324d1.jpg', 'https://ali-ec.static.yximgs.com/ufile/adsocial/907534ea-84fe-4ba1-873d-b1044179bf2c.jpg', 'https://ali-ec.static.yximgs.com/ufile/adsocial/84f940e7-5efa-4daa-b2c3-0245bb785865.jpg', 'https://ali-ec.static.yximgs.com/ufile/adsocial/5384ddd8-8ad1-4c01-b0f6-da2ea1d6f181.jpg'],
		'details': '定制产品 不支持退货 不合适可以调码',
		'expressFee': 0,
		'expressTemplate': {
			'calType': 1,
			'config': '{"type":1,"content":{"includeProvinces":[11,12,13,14,15,21,22,23,31,32,33,34,35,36,37,41,42,43,44,45,46,50,51,52,53,54,61,62,63,64,65],"excludeProvinces":[],"provinceFees":[]}}',
			'createTime': 1558586280722,
			'deleteTime': 0,
			'id': 46036634,
			'name': '默认包邮模板2019',
			'sellerId': 144077034,
			'sendCityCode': 1311,
			'sendCityName': '衡水市',
			'sendDistrictCode': 131121,
			'sendDistrictName': '枣强县',
			'sendProvinceCode': 13,
			'sendProvinceName': '河北省',
			'sendTime': 48,
			'sourceType': 0,
			'status': 1,
			'updateTime': 1574090063655,
			'used': False
		},
		'expressTemplateId': 46036634,
		'hasVideoRelateProduct': True,
		'imageUrls': ['https://ali-ec.static.yximgs.com/ufile/adsocial/d11cb8e1-d617-4f00-86e8-07b1b26a3d49.jpg', 'https://ali-ec.static.yximgs.com/ufile/adsocial/7d788f41-2e8e-4ccd-b5d4-4c975cbde748.jpg', 'https://ali-ec.static.yximgs.com/ufile/adsocial/ddaacde4-c1b6-4c1f-9680-ff2d9056f887.jpg'],
		'isPurchaseLimit': 0,
		'itemCdnPicUrl': None,
		'itemCommentCount': 59,
		'itemCommentRecoList': [{
			'anonymous': 0,
			'avatar': 'https://tx2.a.yximgs.com/uhead/AB/2014/12/30/06/BMjAxNDEyMzAwNjA2MjFfMjg3MzM3ODdfMV9oZDY1.jpg',
			'commentId': 446892429,
			'content': '衣服用料不错，穿起来暖和，大器！',
			'creditScore': 5,
			'nickName': '习惯G有你'
		}, {
			'anonymous': 0,
			'avatar': 'https://tx2.a.yximgs.com/uhead/AB/2019/07/25/19/BMjAxOTA3MjUxOTMwMTZfMTM4NDE4OTk1M18xX2hkNTU3XzQ0Nw==_s.jpg',
			'commentId': 422071057,
			'content': '这么冷的天、快递人员辛苦了、祝你们新年快乐。衣服收到了、非常满意、愿你们工作愉快、天天好心情！',
			'creditScore': 5,
			'nickName': '电气石化'
		}, {
			'anonymous': 0,
			'avatar': 'http://static.yximgs.com/s1/i/def/head_m.png',
			'commentId': 420911637,
			'content': '衣服质量挺好的，服务也很好',
			'creditScore': 5,
			'nickName': '以诚相待2734'
		}],
		'itemId': 38951473034,
		'itemLinkUrl': None,
		'itemTagList': [],
		'nickName': '小马皮草店',
		'platformFeeRatio': 0,
		'price': 168000,
		'purchaseLimitCount': None,
		'sellerId': 144077034,
		'serviceRule': {
			'certificateGuarantee': '0',
			'depositRule': '1',
			'refundRule': '1',
			'refundRuleVO': {
				'code': '1',
				'text': '满足相应条件时，消费者可申请“七天无理由退换货”',
				'title': '支持7天无理由退货'
			},
			'theDayOfDeliverGoodsTime': -1
		},
		'skuInfoList': [{
			'appkey': None,
			'imageUrl': 'https://ali-ec.static.yximgs.com/ufile/adsocial/701c41ac-b6e4-48b1-a6d9-7c065935465f.jpg',
			'relSkuId': 0,
			'skuDesc': '青根貂本色M',
			'skuId': 38951474034,
			'skuNick': '',
			'skuSalePrice': 168000,
			'skuStock': 996,
			'specification': '青根貂本色M',
			'volume': 4
		}, {
			'appkey': None,
			'imageUrl': 'https://ali-ec.static.yximgs.com/ufile/adsocial/88c3865b-bb06-4b98-8839-66678e886dd9.jpg',
			'relSkuId': 0,
			'skuDesc': 'L',
			'skuId': 38951475034,
			'skuNick': '',
			'skuSalePrice': 168000,
			'skuStock': 986,
			'specification': 'L',
			'volume': 14
		}, {
			'appkey': None,
			'imageUrl': 'https://ali-ec.static.yximgs.com/ufile/adsocial/feb7d4ef-1510-45d5-b605-90ddd6937b0e.jpg',
			'relSkuId': 0,
			'skuDesc': 'XL',
			'skuId': 38951476034,
			'skuNick': '',
			'skuSalePrice': 168000,
			'skuStock': 984,
			'specification': 'XL',
			'volume': 16
		}, {
			'appkey': None,
			'imageUrl': 'https://ali-ec.static.yximgs.com/ufile/adsocial/4368e009-8f57-432c-8b5a-d07cd1c21f58.jpg',
			'relSkuId': 0,
			'skuDesc': '2XL',
			'skuId': 38951477034,
			'skuNick': '',
			'skuSalePrice': 168000,
			'skuStock': 984,
			'specification': '2XL',
			'volume': 16
		}, {
			'appkey': None,
			'imageUrl': 'https://ali-ec.static.yximgs.com/ufile/adsocial/d83c01d8-42e8-431b-b9f3-e65606e64e5d.jpg',
			'relSkuId': 0,
			'skuDesc': '3XL',
			'skuId': 38951478034,
			'skuNick': '',
			'skuSalePrice': 168000,
			'skuStock': 988,
			'specification': '3XL',
			'volume': 12
		}, {
			'appkey': None,
			'imageUrl': 'https://ali-ec.static.yximgs.com/ufile/adsocial/11e9a18b-d68c-4fdb-929f-169ad4e1d28c.jpg',
			'relSkuId': 0,
			'skuDesc': '4XL',
			'skuId': 38951479034,
			'skuNick': '',
			'skuSalePrice': 178000,
			'skuStock': 996,
			'specification': '4XL',
			'volume': 4
		}, {
			'appkey': None,
			'imageUrl': 'https://ali-ec.static.yximgs.com/ufile/adsocial/aa01f619-9cf7-497f-a18c-6bf8046fe5af.jpg',
			'relSkuId': 0,
			'skuDesc': '全黑青根貂M',
			'skuId': 38951480034,
			'skuNick': '',
			'skuSalePrice': 168000,
			'skuStock': 999,
			'specification': '全黑青根貂M',
			'volume': 1
		}, {
			'appkey': None,
			'imageUrl': 'https://ali-ec.static.yximgs.com/ufile/adsocial/e077d8b6-0cec-4981-9334-de6847c9c060.jpg',
			'relSkuId': 0,
			'skuDesc': '黑L',
			'skuId': 38951481034,
			'skuNick': '',
			'skuSalePrice': 168000,
			'skuStock': 996,
			'specification': '黑L',
			'volume': 4
		}, {
			'appkey': None,
			'imageUrl': 'https://ali-ec.static.yximgs.com/ufile/adsocial/6dcdb3df-8f07-4bfc-9db0-c30e75eb81d8.jpg',
			'relSkuId': 0,
			'skuDesc': '黑XL',
			'skuId': 38951482034,
			'skuNick': '',
			'skuSalePrice': 168000,
			'skuStock': 990,
			'specification': '黑XL',
			'volume': 10
		}, {
			'appkey': None,
			'imageUrl': 'https://ali-ec.static.yximgs.com/ufile/adsocial/3ca9207b-ad4d-4912-8976-5fd63f64dd75.jpg',
			'relSkuId': 0,
			'skuDesc': '黑2XL',
			'skuId': 38951483034,
			'skuNick': '',
			'skuSalePrice': 168000,
			'skuStock': 996,
			'specification': '黑2XL',
			'volume': 4
		}, {
			'appkey': None,
			'imageUrl': 'https://ali-ec.static.yximgs.com/ufile/adsocial/6ce000b3-7e19-4381-99e7-c8eeb66202a6.jpg',
			'relSkuId': 0,
			'skuDesc': '黑3XL',
			'skuId': 38951484034,
			'skuNick': '',
			'skuSalePrice': 168000,
			'skuStock': 993,
			'specification': '黑3XL',
			'volume': 7
		}, {
			'appkey': None,
			'imageUrl': 'https://ali-ec.static.yximgs.com/ufile/adsocial/3127f141-2a2f-4b18-bc3d-28e6fd3a16f4.jpg',
			'relSkuId': 0,
			'skuDesc': '黑4XL',
			'skuId': 38951485034,
			'skuNick': '',
			'skuSalePrice': 178000,
			'skuStock': 998,
			'specification': '黑4XL',
			'volume': 2
		}],
		'soldAmount': 91,
		'sourceType': 99,
		'specificationList': None,
		'tagList': [{
			'reportName': '有图',
			'tagName': '有图(4)',
			'tagUrl': 'https://www.kwaishop.com/merchant/shop/detail/comment?itemId=38951473034&tagId=1&carrierType=3'
		}, {
			'reportName': '视频',
			'tagName': '有视频(1)',
			'tagUrl': 'https://www.kwaishop.com/merchant/shop/detail/comment?itemId=38951473034&tagId=2&carrierType=3'
		}, {
			'reportName': '追加',
			'tagName': '追加(5)',
			'tagUrl': 'https://www.kwaishop.com/merchant/shop/detail/comment?itemId=38951473034&tagId=3&carrierType=3'
		}],
		'title': '19年新款男士短款无领',
		'videoBO': {
			'caption': '#热 #热门 #官方大大我要上热门 #官方大大我要热门官方大大 '
			'#感谢快手我要上热门 ',
			'mainUrl': 'https://txmov2.a.yximgs.com/upic/2019/10/28/22/BMjAxOTEwMjgyMjMzMDRfMTQ0MDc3MDM0XzE4OTc5MzQwOTIzXzFfMw==_b_B1aa4e5949a9ea53338806c73b45cf9d2.mp4?tag=1-1579033051-unknown-0-3capcwl9x5-f8b797c22859e1b6',
			'photoStatus': 0,
			'publishTime': 1572273185741,
			'reviewed': True,
			'thumbnailUrl': 'https://tx2.a.yximgs.com/upic/2019/10/28/22/BMjAxOTEwMjgyMjMzMDRfMTQ0MDc3MDM0XzE4OTc5MzQwOTIzXzFfMw==_Be64a6a4072ce9898a532024b2eb65347.jpg?tag=1-1579033051-unknown-0-eic3eus65h-4720792fb52b8e8e',
			'userId': 144077034,
			'video': True,
			'videoDuration': 10443,
			'videoId': 18979340923
		},
		'videoNotRelateProductReason': None
	},
	'productId': 38951473034,
	'spider_datetime': '2020-01-15 16:03:47',
	'spider_name': 'kuaishou_shop_product_detail'
}