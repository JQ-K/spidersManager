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
	'productId': 38951473034,
	'productInfo': {
		'addType': 0,
		'imageUrl': 'https://ali-ec.static.yximgs.com/ufile/adsocial/04d73b3e-eff2-4c50-83c8-d43124deaeb9-i38951473034.jpg',
		'itemId': 38951473034,
		'itemLinkUrl': 'https://www.kwaishop.com/merchant/shop/detail?id=38951473034',
		'itemTagList': [],
		'productPrice': 168000,
		'productTitle': '19年新款男士短款无领',
		'showCoupon': False,
		'sourceType': 99,
		'stock': 0,
		'updateTime': 1578724493927,
		'volume': 91
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

5. 小店商品评论
{
	'commentId': 449056631,
	'productComment': {
		'anonymous': 0,
		'auditStatus': 1,
		'auto': 0,
		'commentId': 449056631,
		'commentImgUrls': [],
		'commentUser': {
			'avatar': 'https://tx2.a.yximgs.com/uhead/AB/2019/12/20/23/BMjAxOTEyMjAyMzExMjVfMTIwNDQ0NzU2NF8yX2hkNzEzXzQwNQ==_s.jpg',
			'nickName': '天山雪鹰526'
		},
		'commentUserId': 1204447564,
		'commentVideoIds': [],
		'commentVideoUrls': [],
		'complainStatus': 0,
		'content': '此用户未填写评价内容',
		'creditScore': 5,
		'itemId': 38951473034,
		'itemSkuId': 38951476034,
		'itemSkuSpecDesc': 'XL',
		'itemUserId': 144077034,
		'likeCount': 0,
		'liked': 0,
		'likedByVisitor': 0,
		'logisticsScore': 5,
		'oid': 2000400007082564,
		'qualityScore': 5,
		'replied': 0,
		'replyCnt': 0,
		'serviceScore': 5,
		'subComments': [{
			'anonymous': 0,
			'attached': 0,
			'auditStatus': 1,
			'commentId': 449133933,
			'commentImgUrls': ['https://ali-ec.static.yximgs.com/ufile/adsocial/0fd73993-a553-45de-a20e-a0623a89e183.jpg', 'https://ali-ec.static.yximgs.com/ufile/adsocial/cde38aa9-ef96-478d-8da2-bab0c852f4c7.jpg'],
			'commentUser': {
				'avatar': 'https://tx2.a.yximgs.com/uhead/AB/2019/12/20/23/BMjAxOTEyMjAyMzExMjVfMTIwNDQ0NzU2NF8yX2hkNzEzXzQwNQ==_s.jpg',
				'nickName': '天山雪鹰526'
			},
			'commentUserId': 1204447564,
			'commentVideoIds': [],
			'commentVideoUrls': [],
			'complainStatus': 0,
			'content': '货真价实又便宜还真毛最实惠了朋友们赶快拿起手机定够吧',
			'itemId': 38951473034,
			'itemSkuId': 38951476034,
			'itemUserId': 144077034,
			'itemUserReply': 0,
			'likeCount': 0,
			'liked': 0,
			'logisticsScore': 0,
			'qualityScore': 0,
			'replied': 0,
			'replyToCommentId': 449056631,
			'serviceScore': 0,
			'timestamp': 1578907047343
		}],
		'timestamp': 1578905315101
	},
	'productId': 38951473034,
	'spider_datetime': '2020-01-16 09:55:22',
	'spider_name': 'kuaishou_shop_product_comment'
}

6. 视频信息_pc端版本
{
	"spider_name": "kuaishou_public_feeds",
	"spider_datetime": "2020-02-20 09:55:22",
	"photo_id": "3x69cc7hgugxruc",
	"user_photo_info": {
		"id": "3x69cc7hgugxruc",
		"thumbnailUrl": "https://tx2.a.yximgs.com/upic/2019/12/18/22/BMjAxOTEyMTgyMjQ5MDlfMTQ0MDc3MDM0XzIwNjYwNDM4MzE2XzFfMw==_Bc8163177e264f79905d38bffc2529d7c.jpg",
		"poster": "https://tx2.a.yximgs.com/upic/2019/12/18/22/BMjAxOTEyMTgyMjQ5MDlfMTQ0MDc3MDM0XzIwNjYwNDM4MzE2XzFfMw==_Bc8163177e264f79905d38bffc2529d7c.jpg",
		"workType": "video",
		"type": "work",
		"useVideoPlayer": true,
		"imgUrls": [],
		"imgSizes": [],
		"magicFace": null,
		"musicName": null,
		"caption": "#热 #热门 #官方大大我要上热门 #官方大大我要热门官方大大 #感谢快手我要上热门",
		"location": null,
		"liked": false,
		"onlyFollowerCanComment": true,
		"relativeHeight": null,
		"timestamp": 1576680551300,
		"width": 720,
		"height": 1280,
		"counts": {
			"displayView": "4.1w",
			"displayLike": "435",
			"displayComment": "3",
			"__typename": "VideoCountInfo"
		},
		"user": {
			"id": "CCTT7777",
			"eid": "3x6fazsj5q2ujfy",
			"name": "小马皮草店",
			"avatar": "https://js2.a.yximgs.com/uhead/AB/2018/12/20/21/BMjAxODEyMjAyMTI4MDNfMTQ0MDc3MDM0XzFfaGQyNV80ODI=_s.jpg",
			"__typename": "User"
		},
		"expTag": "1_i/0_null",
		"__typename": "VideoFeed"
	}
}

6.视频信息_手机端5.2版本



7.话题列表中单个话题的总揽信息
{
	"spider_name": "kuaishou_tag_rec_list_v5",
	"tagId": 17842124,
	"tagName": "我的快手影集",
	"tagRecInfo": {
		"photos": [{
			"displayTime": "",
			"time": "2020-02-24 18:46:58",
			"timestamp": 1582541218971,
			"photo_id": 5241627039121698367,
			"photo_status": 0,
			"share_count": 0,
			"view_count": 462463,
			"like_count": 24490,
			"caption": "#我的快手影集 #支持快手传 #快影我想上次热门 #感谢快手提供绿色平台 #感谢快手官大大送上热门  @王者荣耀喜策(O1415261932) @今天拍点啥(O840386039) 热门冲冲冲！",
			"unlike_count": 0,
			"forward_count": 0,
			"plcFeatureEntryAbFlag": 0,
			"noNeedToRequestPLCApi": true,
			"main_mv_urls": [{
				"cdn": "txmov2.a.kwimgs.com",
				"url": "http://txmov2.a.kwimgs.com/upic/2020/02/24/18/BMjAyMDAyMjQxODQ2NTVfMTExMjI5OTE2MF8yMzk5OTk3NTQ1NF8yXzM=_b_B96b83255153f945a2d642315279639f5.mp4?tag=1-1583299547-unknown-0-2gondzetgu-a617e204b58a1eb6"
			}, {
				"cdn": "alimov2.a.yximgs.com",
				"url": "http://alimov2.a.yximgs.com/upic/2020/02/24/18/BMjAyMDAyMjQxODQ2NTVfMTExMjI5OTE2MF8yMzk5OTk3NTQ1NF8yXzM=_b_B96b83255153f945a2d642315279639f5.mp4?tag=1-1583299547-unknown-1-yquxx2yyzc-48f8c449cdd9ec03"
			}],
			"cover_thumbnail_urls": [{
				"cdn": "tx2.a.yximgs.com",
				"url": "http://tx2.a.yximgs.com/upic/2020/02/24/18/BMjAyMDAyMjQxODQ2NTVfMTExMjI5OTE2MF8yMzk5OTk3NTQ1NF8yXzM=_low_Bbd1bc3faad2e741d9c0340582fab13c8.webp?tag=1-1583299547-unknown-0-5tkkwz330p-6086f2ca4333bb4f"
			}, {
				"cdn": "ali2.a.yximgs.com",
				"url": "http://ali2.a.yximgs.com/upic/2020/02/24/18/BMjAyMDAyMjQxODQ2NTVfMTExMjI5OTE2MF8yMzk5OTk3NTQ1NF8yXzM=_low_Bbd1bc3faad2e741d9c0340582fab13c8.webp?tag=1-1583299547-unknown-1-bmyrltkyrb-28180518d394a12b"
			}],
			"poi": {
				"city": "安阳市",
				"title": "女洗手间",
				"latitude": 36.095865,
				"longitude": 114.349101,
				"address": "河南省安阳市文峰区学巷街与西大街交叉口东北50米",
				"id": 231109884,
				"category": 0
			},
			"comments": [],
			"us_c": 0,
			"comment_count": 1558,
			"tubeEntryInfo": {},
			"recoTags": [],
			"adminTags": [],
			"tags": [{
				"id": 17842124,
				"name": "我的快手影集",
				"rich": true,
				"tag": "我的快手影集",
				"ksOrderId": "HTBDC-DD29C86A525E"
			}],
			"tag_hash_type": 1,
			"following": 0,
			"kwaiId": "master-hand123",
			"verified": false,
			"user_sex": "M",
			"headurls": [{
				"cdn": "ali2.a.yximgs.com",
				"url": "http://ali2.a.yximgs.com/uhead/AB/2020/02/16/12/BMjAyMDAyMTYxMjU1MzRfMTExMjI5OTE2MF8yX2hkOTgxXzYzNg==_s.jpg",
				"urlPattern": "http://aliimg.a.yximgs.com/uhead/AB/2020/02/16/12/BMjAyMDAyMTYxMjU1MzRfMTExMjI5OTE2MF8yX2hkOTgxXzYzNg==_s.jpg@0e_0o_0l_{h}h_{w}w_85q.src"
			}, {
				"cdn": "js2.a.yximgs.com",
				"url": "http://js2.a.yximgs.com/uhead/AB/2020/02/16/12/BMjAyMDAyMTYxMjU1MzRfMTExMjI5OTE2MF8yX2hkOTgxXzYzNg==_s.jpg",
				"urlPattern": "http://js2.a.yximgs.com/uhead/AB/2020/02/16/12/BMjAyMDAyMTYxMjU1MzRfMTExMjI5OTE2MF8yX2hkOTgxXzYzNg==_s.jpg@base@tag=imgScale&r=0&q=85&w={w}&h={h}&rotate"
			}],
			"user_name": "王者荣耀无畔（全能王）",
			"moodLikeType": 0,
			"hated": 0,
			"liked": 0,
			"shareGuide": {},
			"us_d": 0,
			"enableShareToStory": true,
			"forward_stats_params": {
				"et": "1_a/2000029291261195793_t030"
			},
			"share_info": "userId=3xen36zjdxpy5ee&photoId=3x2jb97twxmbkfu",
			"editInfo": {},
			"duration": 49033,
			"type": 1,
			"ext_params": {
				"mtype": 3,
				"color": "040505",
				"w": 720,
				"sound": 48994,
				"h": 1280,
				"interval": 30,
				"video": 49033
			},
			"user_id": 1112299160,
			"exp_tag": "1_a/2000029291261195793_t030",
			"serverExpTag": "feed_photo|5241627039121698367|1112299160|1_a/2000029291261195793_t030",
			"reco_reason": "t030",
			"extEntry": null
		}, {
			"displayTime": "",
			"longVideo": true,
			"time": "2019-12-30 17:12:56",
			"timestamp": 1577697176209,
			"photo_id": 5234027211469098365,
			"photo_status": 0,
			"share_count": 0,
			"view_count": 6127225,
			"like_count": 435572,
			"caption": "双击加关注\n #我的快手影集 #",
			"unlike_count": 0,
			"forward_count": 0,
			"plcFeatureEntryAbFlag": 0,
			"noNeedToRequestPLCApi": true,
			"main_mv_urls": [{
				"cdn": "jsmov2.a.yximgs.com",
				"url": "http://jsmov2.a.yximgs.com/upic/2019/12/30/17/BMjAxOTEyMzAxNzEyNTFfNzEzMjU0MTAwXzIxMTAzODg5NjkxXzJfMw==_b_Be3393ab42fcdc2db37c5c9af32f8da0b.mp4?tag=1-1583299547-unknown-0-y6a3vbmquy-192d9ddd17e50d5f&type=hot"
			}, {
				"cdn": "alimov2.a.yximgs.com",
				"url": "http://alimov2.a.yximgs.com/upic/2019/12/30/17/BMjAxOTEyMzAxNzEyNTFfNzEzMjU0MTAwXzIxMTAzODg5NjkxXzJfMw==_b_Be3393ab42fcdc2db37c5c9af32f8da0b.mp4?tag=1-1583299547-unknown-1-bv67jgskff-ceb4ab3f2088d336&type=hot"
			}],
			"cover_thumbnail_urls": [{
				"cdn": "js2.a.yximgs.com",
				"url": "http://js2.a.yximgs.com/upic/2019/12/30/17/BMjAxOTEyMzAxNzEyNTFfNzEzMjU0MTAwXzIxMTAzODg5NjkxXzJfMw==_low_B5c27936c9ed478106b2fd12e38448b8a.webp?tag=1-1583299547-unknown-0-6icxk13jbk-663da19d9928036f&type=hot"
			}, {
				"cdn": "ali2.a.yximgs.com",
				"url": "http://ali2.a.yximgs.com/upic/2019/12/30/17/BMjAxOTEyMzAxNzEyNTFfNzEzMjU0MTAwXzIxMTAzODg5NjkxXzJfMw==_low_B5c27936c9ed478106b2fd12e38448b8a.webp?tag=1-1583299547-unknown-1-5qhjvc2bly-39d4846714b3d3f0&type=hot"
			}],
			"comments": [],
			"us_c": 0,
			"comment_count": 17521,
			"hasMusicTag": true,
			"music": {
				"musicianUid": 95331508,
				"chorus": 49160,
				"duration": 243,
				"name": "奶奶",
				"id": 34650,
				"type": 4,
				"loudness": -17.718918,
				"lrcUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/udata/music/bgm_138b5428-1abf-4dae-a59b-7027c6db37fb.lrc"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/udata/music/bgm_138b5428-1abf-4dae-a59b-7027c6db37fb.lrc"
				}],
				"audioUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/udata/music/bm_s7DCf1Z4Gx0_v.m4a"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/udata/music/bm_s7DCf1Z4Gx0_v.m4a"
				}],
				"avatarUrl": "http://tx2.a.yximgs.com/udata/music/artist_1tgdhYQEYMo_4gHmZkCHlKs_scaled.jpg",
				"url": "http://tx2.a.yximgs.com/udata/music/bm_s7DCf1Z4Gx0_v.m4a",
				"lrc": "http://tx2.a.yximgs.com/udata/music/bgm_138b5428-1abf-4dae-a59b-7027c6db37fb.lrc",
				"genreId": 0,
				"artist": "韩安旭",
				"avatarUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/udata/music/artist_1tgdhYQEYMo_4gHmZkCHlKs_scaled.jpg"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/udata/music/artist_1tgdhYQEYMo_4gHmZkCHlKs_scaled.jpg"
				}],
				"audioType": 1
			},
			"tubeEntryInfo": {},
			"recoTags": [],
			"adminTags": [],
			"tags": [{
				"id": 17842124,
				"name": "我的快手影集",
				"rich": true,
				"tag": "我的快手影集",
				"ksOrderId": "HTBDC-DD29C86A525E"
			}],
			"tag_hash_type": 1,
			"following": 0,
			"kwaiId": "luyou123456",
			"verified": false,
			"user_sex": "M",
			"us_l": true,
			"headurls": [{
				"cdn": "ali2.a.yximgs.com",
				"url": "http://ali2.a.yximgs.com/uhead/AB/2020/03/03/12/BMjAyMDAzMDMxMjAyMjZfNzEzMjU0MTAwXzJfaGQ3ODVfNTMz_s.jpg",
				"urlPattern": "http://aliimg.a.yximgs.com/uhead/AB/2020/03/03/12/BMjAyMDAzMDMxMjAyMjZfNzEzMjU0MTAwXzJfaGQ3ODVfNTMz_s.jpg@0e_0o_0l_{h}h_{w}w_85q.src"
			}, {
				"cdn": "js2.a.yximgs.com",
				"url": "http://js2.a.yximgs.com/uhead/AB/2020/03/03/12/BMjAyMDAzMDMxMjAyMjZfNzEzMjU0MTAwXzJfaGQ3ODVfNTMz_s.jpg",
				"urlPattern": "http://js2.a.yximgs.com/uhead/AB/2020/03/03/12/BMjAyMDAzMDMxMjAyMjZfNzEzMjU0MTAwXzJfaGQ3ODVfNTMz_s.jpg@base@tag=imgScale&r=0&q=85&w={w}&h={h}&rotate"
			}],
			"user_name": "断臂男孩跟奶奶",
			"moodLikeType": 0,
			"hated": 0,
			"liked": 0,
			"shareGuide": {},
			"us_d": 0,
			"enableShareToStory": true,
			"forward_stats_params": {
				"et": "1_a/2000029291261195793_t030"
			},
			"share_info": "userId=3x4zzcjtj3p3veq&photoId=3xce55myjxittyi",
			"editInfo": {},
			"duration": 61833,
			"type": 1,
			"ext_params": {
				"mtype": 3,
				"color": "443227",
				"w": 720,
				"sound": 61760,
				"h": 1280,
				"interval": 30,
				"video": 61833
			},
			"user_id": 713254100,
			"exp_tag": "1_a/2000029291261195793_t030",
			"serverExpTag": "feed_photo|5234027211469098365|713254100|1_a/2000029291261195793_t030",
			"reco_reason": "t030",
			"followShoot": {
				"lrcUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/bs2/ost/MjExMDM4ODk2OTFfNzEzMjU0MTAw.trcx"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/bs2/ost/MjExMDM4ODk2OTFfNzEzMjU0MTAw.trcx"
				}]
			},
			"extEntry": null
		}, {
			"displayTime": "",
			"longVideo": true,
			"time": "2020-02-10 23:55:02",
			"timestamp": 1581350102173,
			"photo_id": 5203346443520184305,
			"photo_status": 0,
			"share_count": 0,
			"view_count": 1632022,
			"like_count": 121546,
			"caption": "#快手有戏精 #我的快手影集 #逆光行动 #热门发现 #感谢快手我要上热门",
			"unlike_count": 0,
			"forward_count": 0,
			"plcFeatureEntryAbFlag": 0,
			"noNeedToRequestPLCApi": true,
			"main_mv_urls": [{
				"cdn": "jsmov2.a.yximgs.com",
				"url": "http://jsmov2.a.yximgs.com/upic/2020/02/10/23/BMjAyMDAyMTAyMzU0NThfMTQ4NzQ0NzA1OF8yMzI4Mzg5OTQyMF8yXzM=_b_B3c89827dcdec240b901d100439852d34.mp4?tag=1-1583299547-unknown-0-sln2r96h7y-64dc8dc06019e2d3&type=hot"
			}, {
				"cdn": "alimov2.a.yximgs.com",
				"url": "http://alimov2.a.yximgs.com/upic/2020/02/10/23/BMjAyMDAyMTAyMzU0NThfMTQ4NzQ0NzA1OF8yMzI4Mzg5OTQyMF8yXzM=_b_B3c89827dcdec240b901d100439852d34.mp4?tag=1-1583299547-unknown-1-cgmial1imj-cdb03b2a567f1922&type=hot"
			}],
			"cover_thumbnail_urls": [{
				"cdn": "js2.a.yximgs.com",
				"url": "http://js2.a.yximgs.com/upic/2020/02/10/23/BMjAyMDAyMTAyMzU0NThfMTQ4NzQ0NzA1OF8yMzI4Mzg5OTQyMF8yXzM=_low_B5abbc0517d93af89458ce28dc657b19a.webp?tag=1-1583299547-unknown-0-kat28re24g-6201abcc7d24154b&type=hot"
			}, {
				"cdn": "ali2.a.yximgs.com",
				"url": "http://ali2.a.yximgs.com/upic/2020/02/10/23/BMjAyMDAyMTAyMzU0NThfMTQ4NzQ0NzA1OF8yMzI4Mzg5OTQyMF8yXzM=_low_B5abbc0517d93af89458ce28dc657b19a.webp?tag=1-1583299547-unknown-1-eyw75ypzww-8fb9519579768008&type=hot"
			}],
			"comments": [],
			"us_c": 0,
			"comment_count": 3234,
			"tubeEntryInfo": {},
			"recoTags": [],
			"adminTags": [],
			"tags": [{
				"id": 17842124,
				"name": "我的快手影集",
				"rich": true,
				"tag": "我的快手影集",
				"ksOrderId": "HTBDC-DD29C86A525E"
			}, {
				"id": 40744001,
				"name": "快手有戏精",
				"rich": true,
				"tag": "快手有戏精",
				"ksOrderId": "HTBDC-86CE5A74E70D"
			}, {
				"id": 9462295,
				"name": "感谢快手我要上热门",
				"rich": true,
				"tag": "感谢快手我要上热门"
			}],
			"tag_hash_type": 1,
			"following": 0,
			"verified": false,
			"user_sex": "F",
			"us_l": true,
			"headurls": [{
				"cdn": "ali2.a.yximgs.com",
				"url": "http://ali2.a.yximgs.com/uhead/AB/2019/12/04/01/BMjAxOTEyMDQwMTIyMTBfMTQ4NzQ0NzA1OF8yX2hkNzY4XzE1OQ==_s.jpg",
				"urlPattern": "http://aliimg.a.yximgs.com/uhead/AB/2019/12/04/01/BMjAxOTEyMDQwMTIyMTBfMTQ4NzQ0NzA1OF8yX2hkNzY4XzE1OQ==_s.jpg@0e_0o_0l_{h}h_{w}w_85q.src"
			}, {
				"cdn": "js2.a.yximgs.com",
				"url": "http://js2.a.yximgs.com/uhead/AB/2019/12/04/01/BMjAxOTEyMDQwMTIyMTBfMTQ4NzQ0NzA1OF8yX2hkNzY4XzE1OQ==_s.jpg",
				"urlPattern": "http://js2.a.yximgs.com/uhead/AB/2019/12/04/01/BMjAxOTEyMDQwMTIyMTBfMTQ4NzQ0NzA1OF8yX2hkNzY4XzE1OQ==_s.jpg@base@tag=imgScale&r=0&q=85&w={w}&h={h}&rotate"
			}],
			"user_name": "梓皙芳妹儿",
			"moodLikeType": 0,
			"hated": 0,
			"liked": 0,
			"shareGuide": {},
			"us_d": 1,
			"enableShareToStory": true,
			"forward_stats_params": {
				"et": "1_a/2000029291261195793_t030"
			},
			"share_info": "userId=3xvjevysxc6c7n9&photoId=3x37u432jpeawgk",
			"editInfo": {},
			"duration": 237700,
			"type": 1,
			"ext_params": {
				"mtype": 3,
				"color": "464444",
				"w": 714,
				"sound": 237679,
				"h": 1272,
				"interval": 30,
				"video": 237700
			},
			"user_id": 1487447058,
			"exp_tag": "1_a/2000029291261195793_t030",
			"serverExpTag": "feed_photo|5203346443520184305|1487447058|1_a/2000029291261195793_t030",
			"reco_reason": "t030",
			"extEntry": null
		}],
		"photoCount": 25911896,
		"tag": {
			"name": "我的快手影集",
			"rich": true,
			"id": 17842124
		},
		"type": "TEXT_TAG",
		"exp_tag": "2000029291261195793_tl3"
	},
	"spider_datetime": "2020-03-04 13:25:48"
}

8. 话题信息
{
	"spider_name": "kuaishou_tag_info_v5",
	"tagId": 17842124,
	"tagName": "我的快手影集",
	"tagInfo": {
		"textRichInfo": {
			"bannerUrls": [{
				"cdn": "static.yximgs.com",
				"url": "https://static.yximgs.com/bs2/adminBlock/block-20200205103600-NaVVljIr.png"
			}],
			"tagId": 17842124,
			"description": "2019快手影集来啦！升级至最新版本，点击下方“去生成”，或去个人主页、本地作品集查看你的快手影集吧！生成影集需要有一定的作品量，如果没有影集，请多发好看的作品，期待下次为你生成~记得与大家分享你的影集哦！",
			"tag": "我的快手影集",
			"coverUrls": [{
				"cdn": "ali2.a.yximgs.com",
				"url": "http://ali2.a.yximgs.com/uhead/AB/2019/01/30/09/BMjAxOTAxMzAwOTUyMzhfMF90MTc4NDIxMjRfbHY=.jpg",
				"urlPattern": "http://aliimg.a.yximgs.com/uhead/AB/2019/01/30/09/BMjAxOTAxMzAwOTUyMzhfMF90MTc4NDIxMjRfbHY=.jpg@0e_0o_0l_{h}h_{w}w_85q.src"
			}, {
				"cdn": "js2.a.yximgs.com",
				"url": "http://js2.a.yximgs.com/uhead/AB/2019/01/30/09/BMjAxOTAxMzAwOTUyMzhfMF90MTc4NDIxMjRfbHY=.jpg",
				"urlPattern": "http://js2.a.yximgs.com/uhead/AB/2019/01/30/09/BMjAxOTAxMzAwOTUyMzhfMF90MTc4NDIxMjRfbHY=.jpg@base@tag=imgScale&r=0&q=85&w={w}&h={h}&rotate"
			}]
		},
		"viewCountText": "60.8亿 播放",
		"viewCount": 6075064965,
		"photoCountText": "2591.4W 个作品",
		"tagStyleInfo": {
			"tagViewStyle": 1,
			"bannerUrls": [{
				"cdn": "static.yximgs.com",
				"url": "https://static.yximgs.com/bs2/adminBlock/block-20200205103600-NaVVljIr.png"
			}],
			"description": "2019快手影集来啦！升级至最新版本，点击下方“去生成”，或去个人主页、本地作品集查看你的快手影集吧！生成影集需要有一定的作品量，如果没有影集，请多发好看的作品，期待下次为你生成~记得与大家分享你的影集哦！"
		},
		"photoCount": 25913978
	},
	"spider_datetime": "2020-03-04 14:40:25"
}

9.话题相关热门视频信息
{
	"spider_name": "kuaishou_tag_feed_hot_v5",
	"tagId": 17842124,
	"tagName": "我的快手影集",
	"photo_id": 5195183669524280930,
	"photoInfo": {
		"displayTime": "",
		"longVideo": true,
		"time": "2020-02-29 11:36:58",
		"timestamp": 1582947418093,
		"photo_id": 5195183669524280930,
		"photo_status": 0,
		"share_count": 0,
		"view_count": 25408,
		"like_count": 943,
		"caption": "更新了兄弟们，马的看见精彩部分完了，哎，又要等一周了。 #斗罗大陆 #我的快手影集",
		"unlike_count": 0,
		"forward_count": 0,
		"plcFeatureEntryAbFlag": 0,
		"noNeedToRequestPLCApi": true,
		"main_mv_urls": [{
			"cdn": "hwmov.a.yximgs.com",
			"url": "http://hwmov.a.yximgs.com/upic/2020/02/29/11/BMjAyMDAyMjkxMTM2NTNfMTEyOTEzODU3M18yNDIzNTIyNzY5M18yXzM=_b_B7aa63646359539ba612643c5d534a712.mp4?tag=1-1583307520-t-0-lvzfosl8xc-0703c9a94a5ab894"
		}, {
			"cdn": "jsmov2.a.yximgs.com",
			"url": "http://jsmov2.a.yximgs.com/upic/2020/02/29/11/BMjAyMDAyMjkxMTM2NTNfMTEyOTEzODU3M18yNDIzNTIyNzY5M18yXzM=_b_B7aa63646359539ba612643c5d534a712.mp4?tag=1-1583307520-t-1-kafppwutll-8d233c061ff7c3ad"
		}],
		"cover_thumbnail_urls": [{
			"cdn": "hw.a.yximgs.com",
			"url": "http://hw.a.yximgs.com/upic/2020/02/29/11/BMjAyMDAyMjkxMTM2NTNfMTEyOTEzODU3M18yNDIzNTIyNzY5M18yXzM=_low_Bf2f9b800d7c66c15ff5dd2bfb5c489a5.webp?tag=1-1583307520-t-0-uyjrnh4tyk-b603b5c1056eca44"
		}, {
			"cdn": "js2.a.yximgs.com",
			"url": "http://js2.a.yximgs.com/upic/2020/02/29/11/BMjAyMDAyMjkxMTM2NTNfMTEyOTEzODU3M18yNDIzNTIyNzY5M18yXzM=_low_Bf2f9b800d7c66c15ff5dd2bfb5c489a5.webp?tag=1-1583307520-t-1-tgzbt5if5z-281a695a9a690697"
		}],
		"comments": [],
		"us_c": 0,
		"comment_count": 65,
		"hasMusicTag": true,
		"music": {
			"musicianUid": 776028418,
			"artistName": "Jin-Music",
			"user": {
				"kwaiId": "JIn13147788",
				"user_id": 776028418,
				"user_sex": "M",
				"headurl": "http://ali2.a.yximgs.com/uhead/AB/2018/08/04/13/BMjAxODA4MDQxMzEwMDZfNzc2MDI4NDE4XzFfaGQzNTBfOTY2_s.jpg",
				"headurls": [{
					"cdn": "ali2.a.yximgs.com",
					"url": "http://ali2.a.yximgs.com/uhead/AB/2018/08/04/13/BMjAxODA4MDQxMzEwMDZfNzc2MDI4NDE4XzFfaGQzNTBfOTY2_s.jpg",
					"urlPattern": "http://aliimg.a.yximgs.com/uhead/AB/2018/08/04/13/BMjAxODA4MDQxMzEwMDZfNzc2MDI4NDE4XzFfaGQzNTBfOTY2_s.jpg@0e_0o_0l_{h}h_{w}w_85q.src"
				}, {
					"cdn": "js2.a.yximgs.com",
					"url": "http://js2.a.yximgs.com/uhead/AB/2018/08/04/13/BMjAxODA4MDQxMzEwMDZfNzc2MDI4NDE4XzFfaGQzNTBfOTY2_s.jpg",
					"urlPattern": "http://js2.a.yximgs.com/uhead/AB/2018/08/04/13/BMjAxODA4MDQxMzEwMDZfNzc2MDI4NDE4XzFfaGQzNTBfOTY2_s.jpg@base@tag=imgScale&r=0&q=85&w={w}&h={h}&rotate"
				}],
				"eid": "3xgsma2ynzv76bm",
				"user_name": "Jin-Music"
			},
			"uploadTime": 1539521473193,
			"auditStatus": 3,
			"genreId": 5,
			"artist": "Jin-Music",
			"avatarUrls": [{
				"cdn": "tx2.a.yximgs.com",
				"url": "http://tx2.a.yximgs.com/udata/music/om_7cSJxLWuFa0_v.jpg"
			}, {
				"cdn": "static.yximgs.com",
				"url": "http://static.yximgs.com/udata/music/om_7cSJxLWuFa0_v.jpg"
			}],
			"duration": 122,
			"name": "Jin(Edit)",
			"id": 458730459,
			"type": 7,
			"audioUrls": [{
				"cdn": "tx2.a.yximgs.com",
				"url": "http://tx2.a.yximgs.com/udata/music/om_P2v_s_VVpgs_v.m4a"
			}, {
				"cdn": "static.yximgs.com",
				"url": "http://static.yximgs.com/udata/music/om_P2v_s_VVpgs_v.m4a"
			}],
			"avatarUrl": "http://tx2.a.yximgs.com/udata/music/om_7cSJxLWuFa0_v.jpg",
			"instrumental": true,
			"url": "http://tx2.a.yximgs.com/udata/music/om_P2v_s_VVpgs_v.m4a",
			"imageUrls": [{
				"cdn": "tx2.a.yximgs.com",
				"url": "http://tx2.a.yximgs.com/udata/music/om_7cSJxLWuFa0_v.jpg"
			}, {
				"cdn": "static.yximgs.com",
				"url": "http://static.yximgs.com/udata/music/om_7cSJxLWuFa0_v.jpg"
			}],
			"audioType": 2,
			"loudness": -13.777812,
			"isOriginal": true
		},
		"tubeEntryInfo": {},
		"recoTags": [],
		"adminTags": [],
		"tags": [{
			"id": 17842124,
			"name": "我的快手影集",
			"rich": true,
			"tag": "我的快手影集",
			"ksOrderId": "HTBDC-DD29C86A525E"
		}],
		"tag_hash_type": 1,
		"following": 0,
		"kwaiId": "asdasd1887415157",
		"verified": false,
		"user_sex": "M",
		"headurls": [{
			"cdn": "ali2.a.yximgs.com",
			"url": "http://ali2.a.yximgs.com/uhead/AB/2020/02/15/08/BMjAyMDAyMTUwODIxMDlfMTEyOTEzODU3M18yX2hkNjM3Xzc1Mw==_s.jpg",
			"urlPattern": "http://aliimg.a.yximgs.com/uhead/AB/2020/02/15/08/BMjAyMDAyMTUwODIxMDlfMTEyOTEzODU3M18yX2hkNjM3Xzc1Mw==_s.jpg@0e_0o_0l_{h}h_{w}w_85q.src"
		}, {
			"cdn": "js2.a.yximgs.com",
			"url": "http://js2.a.yximgs.com/uhead/AB/2020/02/15/08/BMjAyMDAyMTUwODIxMDlfMTEyOTEzODU3M18yX2hkNjM3Xzc1Mw==_s.jpg",
			"urlPattern": "http://js2.a.yximgs.com/uhead/AB/2020/02/15/08/BMjAyMDAyMTUwODIxMDlfMTEyOTEzODU3M18yX2hkNjM3Xzc1Mw==_s.jpg@base@tag=imgScale&r=0&q=85&w={w}&h={h}&rotate"
		}],
		"user_name": "沫七✨（动漫）",
		"shareGuide": {},
		"us_d": 0,
		"enableShareToStory": true,
		"forward_stats_params": {
			"et": "1_a/2000029258054013409_t90"
		},
		"share_info": "userId=3x84a3kibms9mqy&photoId=3xzyed7r7xfiep9",
		"hated": 0,
		"moodLikeType": 0,
		"liked": 0,
		"editInfo": {},
		"duration": 186500,
		"type": 1,
		"ext_params": {
			"mtype": 3,
			"color": "6B4841",
			"w": 720,
			"sound": 186479,
			"h": 1280,
			"interval": 30,
			"video": 186500
		},
		"user_id": 1129138573,
		"exp_tag": "1_a/2000029258054013409_t90",
		"serverExpTag": "feed_photo|5195183669524280930|1129138573|1_a/2000029258054013409_t90",
		"reco_reason": "t90",
		"extEntry": null
	},
	"spider_datetime": "2020-03-04 15:38:40"
}

10.话题相关最新视频信息
{
	"spider_name": "kuaishou_tag_feed_new",
	"tagId": 17842124,
	"tagName": "仙女下凡",
	"photo_id": 5200531691760255188,
	"photoInfo": {
		"displayTime": null,
		"time": "2020-02-29 09:06:00",
		"timestamp": 1582938360176,
		"photo_id": 5200531691760255188,
		"photo_status": 0,
		"share_count": 1,
		"view_count": 146,
		"like_count": 2,
		"caption": "#仙女下凡",
		"unlike_count": 0,
		"forward_count": 0,
		"plcFeatureEntryAbFlag": 0,
		"noNeedToRequestPLCApi": true,
		"main_mv_urls": [{
			"cdn": "txmov2.a.kwimgs.com",
			"url": "http://txmov2.a.kwimgs.com/upic/2020/02/29/09/BMjAyMDAyMjkwOTA1NTdfMTIxMjk1MjQ1M18yNDIyOTQ1MTQ4OV8yXzM=_b_B8810b31454a246249902f4671bd1be55.mp4?tag=1-1582956231-t-0-cofc99vjgy-371137aa9f6ff494"
		}, {
			"cdn": "alimov2.a.yximgs.com",
			"url": "http://alimov2.a.yximgs.com/upic/2020/02/29/09/BMjAyMDAyMjkwOTA1NTdfMTIxMjk1MjQ1M18yNDIyOTQ1MTQ4OV8yXzM=_b_B8810b31454a246249902f4671bd1be55.mp4?tag=1-1582956231-t-1-cj5xytqehx-2854a456abb2fee0"
		}],
		"cover_thumbnail_urls": [{
			"cdn": "tx2.a.yximgs.com",
			"url": "http://tx2.a.yximgs.com/upic/2020/02/29/09/BMjAyMDAyMjkwOTA1NTdfMTIxMjk1MjQ1M18yNDIyOTQ1MTQ4OV8yXzM=_low_B449ad1fc0b73213107c2e6ce86e730c8.webp?tag=1-1582956231-t-0-qwghbwoytk-f40e4c014c0efd73"
		}, {
			"cdn": "ali2.a.yximgs.com",
			"url": "http://ali2.a.yximgs.com/upic/2020/02/29/09/BMjAyMDAyMjkwOTA1NTdfMTIxMjk1MjQ1M18yNDIyOTQ1MTQ4OV8yXzM=_low_B449ad1fc0b73213107c2e6ce86e730c8.webp?tag=1-1582956231-t-1-caoeoe3utz-817081b9fdc64514"
		}],
		"comments": [],
		"us_c": 0,
		"comment_count": 3,
		"recoTags": [],
		"adminTags": [],
		"tags": [],
		"tag_hash_type": 1,
		"following": 0,
		"verified": false,
		"user_sex": "F",
		"headurls": [{
			"cdn": "ali2.a.yximgs.com",
			"url": "http://ali2.a.yximgs.com/uhead/AB/2020/02/29/12/BMjAyMDAyMjkxMjAyMjZfMTIxMjk1MjQ1M18yX2hkMTI2Xzc4OQ==_s.jpg",
			"urlPattern": "http://aliimg.a.yximgs.com/uhead/AB/2020/02/29/12/BMjAyMDAyMjkxMjAyMjZfMTIxMjk1MjQ1M18yX2hkMTI2Xzc4OQ==_s.jpg@0e_0o_0l_{h}h_{w}w_85q.src"
		}, {
			"cdn": "js2.a.yximgs.com",
			"url": "http://js2.a.yximgs.com/uhead/AB/2020/02/29/12/BMjAyMDAyMjkxMjAyMjZfMTIxMjk1MjQ1M18yX2hkMTI2Xzc4OQ==_s.jpg",
			"urlPattern": "http://js2.a.yximgs.com/uhead/AB/2020/02/29/12/BMjAyMDAyMjkxMjAyMjZfMTIxMjk1MjQ1M18yX2hkMTI2Xzc4OQ==_s.jpg@base@tag=imgScale&r=0&q=85&w={w}&h={h}&rotate"
		}],
		"user_name": "食品图片君哦🍦🍦",
		"moodLikeType": 0,
		"hated": 0,
		"liked": 0,
		"shareGuide": {},
		"us_d": 0,
		"forward_stats_params": {
			"fid": "1577168521",
			"et": "1_a/2000029621159760226_t11"
		},
		"share_info": "userId=3x5aj4td62jaz8i&photoId=3xm3xvqkkfs285s",
		"editInfo": {},
		"type": 1,
		"ext_params": {
			"mtype": 3,
			"color": "F8F8FB",
			"w": 540,
			"sound": 12586,
			"h": 540,
			"interval": 20,
			"video": 12600
		},
		"user_id": 1212952453,
		"exp_tag": "1_a/2000029621159760226_t11",
		"serverExpTag": "feed_photo|5200531691760255188|1212952453|1_a/2000029621159760226_t11",
		"reco_reason": "t11",
		"profilePagePrefetchInfo": {
			"profilePageType": 1
		},
		"extEntry": null
	},
	"spider_datetime": "2020-02-29 14:03:51"
}

11. 视频评论信息
{
	"spider_name": "kuaishou_photo_comment",
	"photo_id": "3x7qgrnnavc5tja",
	"commentId": "158843589390",
	"commentInfo": {
		"commentId": "158843589390",
		"authorId": "353658718",
		"authorName": "媛宝兔兔🐰🐰",
		"content": "新年快乐，祝娜姐全家幸福也祝跳跳和俏俏健康茁壮成长[赞][赞][赞]",
		"headurl": "https://js2.a.yximgs.com/uhead/AB/2019/06/24/16/BMjAxOTA2MjQxNjQ5MzlfMzUzNjU4NzE4XzJfaGQxNV80NjA=_s.jpg",
		"timestamp": 1577777387088,
		"authorEid": "3xfi7z53dztjmt6",
		"status": "done",
		"subCommentCount": "155",
		"subCommentsPcursor": "158849881539",
		"likedCount": "1.6w",
		"liked": false,
		"subComments": [{
			"commentId": "158847102650",
			"authorId": "1003899050",
			"authorName": "90后《岁月》",
			"content": "回复 鹏鹏⭐满天星辰：[赞][赞]",
			"headurl": "https://js2.a.yximgs.com/uhead/AB/2019/12/22/18/BMjAxOTEyMjIxODE0NTRfMTAwMzg5OTA1MF8yX2hkMTk2XzE2NQ==_s.jpg",
			"timestamp": 1577778400744,
			"authorEid": "3xvbtz4q7zjc2kw",
			"status": "done",
			"replyToUserName": "鹏鹏⭐满天星辰",
			"replyTo": "520939510",
			"replyToEid": "3xrnsan7y8w9xzu",
			"__typename": "SubComment"
		}, {
			"commentId": "158847981678",
			"authorId": "535294647",
			"authorName": "无敌美少女战士✨",
			"content": "回复 媛宝兔兔🐰🐰：[赞][赞][赞]",
			"headurl": "https://tx2.a.yximgs.com/uhead/AB/2020/03/08/19/BMjAyMDAzMDgxOTI3MTdfNTM1Mjk0NjQ3XzJfaGQxOTVfODcw_s.jpg",
			"timestamp": 1577778647381,
			"authorEid": "3xrc2ptddchfbzy",
			"status": "done",
			"replyToUserName": "媛宝兔兔🐰🐰",
			"replyTo": "353658718",
			"replyToEid": "3xfi7z53dztjmt6",
			"__typename": "SubComment"
		}, {
			"commentId": "158848788013",
			"authorId": "1522879126",
			"authorName": "施舍温柔♞",
			"content": "回复 媛宝兔兔🐰🐰：[赞][赞][赞]",
			"headurl": "https://js2.a.yximgs.com/uhead/AB/2020/03/10/09/BMjAyMDAzMTAwOTQ4MzdfMTUyMjg3OTEyNl8yX2hkNDk2Xzk4_s.jpg",
			"timestamp": 1577778870250,
			"authorEid": "3xgk492p954eui4",
			"status": "done",
			"replyToUserName": "媛宝兔兔🐰🐰",
			"replyTo": "353658718",
			"replyToEid": "3xfi7z53dztjmt6",
			"__typename": "SubComment"
		}],
		"__typename": "Comment"
	},
	"hasSubComment": true,
	"spider_datetime": "2020-03-11 13:35:29"
}

12. 视频子评论信息
{
	"spider_name": "kuaishou_photo_sub_comment",
	"photo_id": "3x7qgrnnavc5tja",
	"rootCommentId": "158878958708",
	"commentId": "159041322328",
	"commentInfo": {
		"commentId": "159041322328",
		"authorId": "1314330984",
		"authorName": "9520享受🍹😋甜美",
		"content": "回复 牛奶咖啡☕＠加面包：新年快乐娜姐姐",
		"headurl": "https://js2.a.yximgs.com/uhead/AB/2020/01/10/09/BMjAyMDAxMTAwOTQyMTNfMTMxNDMzMDk4NF8yX2hkNjJfNzQz_s.jpg",
		"timestamp": 1577807572406,
		"authorEid": "3xjtraddn8na8fu",
		"status": "done",
		"replyToUserName": "牛奶咖啡☕＠加面包",
		"replyTo": "627910311",
		"replyToEid": "3xt4kkcc96zh4e6",
		"__typename": "SubComment"
	},
	"spider_datetime": "2020-03-11 14:38:28"
}