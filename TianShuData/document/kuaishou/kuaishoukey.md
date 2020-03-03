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

6. 视频信息
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

7.话题列表中单个话题的总揽信息
{
	"spider_name": "kuaishou_tag_rec_list",
	"tagId": 17842124,
	"tagName": "我的快手影集",
	"tagRecInfo": {
		"photos": [{
			"hasMusicTag": true,
			"music": {
				"image": "http://tx2.a.yximgs.com/udata/music/bgm_VKZAhWqHuGY_Ni0zd3tmTWM_scaled.jpg",
				"duration": 169,
				"name": "Wondrous",
				"id": "5xy92cpnmidz9ew",
				"type": 4,
				"lrcUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/udata/music/music_d7f13196-4ed8-4459-941b-c3bc6073498d.lrc"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/udata/music/music_d7f13196-4ed8-4459-941b-c3bc6073498d.lrc"
				}],
				"audioUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/udata/music/bm_dXH_gl2CqQ4_v.m4a"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/udata/music/bm_dXH_gl2CqQ4_v.m4a"
				}],
				"avatarUrl": "http://tx2.a.yximgs.com/udata/music/bgm_VKZAhWqHuGY_Ni0zd3tmTWM_scaled.jpg",
				"snippetUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/udata/music/bm_dXH_gl2CqQ4_vs.m4a"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/udata/music/bm_dXH_gl2CqQ4_vs.m4a"
				}],
				"snippetDuration": 20,
				"url": "http://tx2.a.yximgs.com/udata/music/bm_dXH_gl2CqQ4_v.m4a",
				"imageUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/udata/music/bgm_VKZAhWqHuGY_Ni0zd3tmTWM_scaled.jpg"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/udata/music/bgm_VKZAhWqHuGY_Ni0zd3tmTWM_scaled.jpg"
				}],
				"lrc": "http://tx2.a.yximgs.com/udata/music/music_d7f13196-4ed8-4459-941b-c3bc6073498d.lrc",
				"genreId": 0,
				"artist": "Thomas Greenberg",
				"avatarUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/udata/music/bgm_VKZAhWqHuGY_Ni0zd3tmTWM_scaled.jpg"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/udata/music/bgm_VKZAhWqHuGY_Ni0zd3tmTWM_scaled.jpg"
				}],
				"audioType": 1,
				"loudness": -17.781977
			},
			"recoTags": [],
			"fashionEntranceShow": {
				"showType": 3,
				"bizId": "5xy92cpnmidz9ew"
			},
			"sameFrame": {
				"allow": true,
				"showSameFrameCurrentTag": true,
				"availableDepth": 7
			},
			"adminTags": [],
			"tags": [{
				"id": 17842124,
				"name": "我的快手影集",
				"rich": true,
				"tag": "我的快手影集",
				"ksOrderId": "HTBDC-DD29C86A525E"
			}],
			"tag_hash_type": 1,
			"displayTime": null,
			"time": "2019-12-29 16:59:52",
			"timestamp": 1577609992718,
			"photo_id": 5188991213893824269,
			"photo_status": 0,
			"share_count": 0,
			"view_count": 2270022,
			"like_count": 128307,
			"caption": "感谢大家2019年的陪伴，我们一起重温美好瞬间~#我的快手影集",
			"unlike_count": 0,
			"forward_count": 0,
			"plcFeatureEntryAbFlag": 0,
			"noNeedToRequestPLCApi": true,
			"main_mv_urls": [{
				"cdn": "jsmov2.a.yximgs.com",
				"url": "http://jsmov2.a.yximgs.com/upic/2019/12/29/16/BMjAxOTEyMjkxNjU5NTBfMTA3NTg3MzU2NF8yMTA2MjkzODU0NV8yXzM=_b_Bf7c15c1664b78a6881aba243a80960b2.mp4?tag=1-1582859593-unknown-0-igvefebhts-a50396668b6ba23f&type=hot"
			}, {
				"cdn": "alimov2.a.yximgs.com",
				"url": "http://alimov2.a.yximgs.com/upic/2019/12/29/16/BMjAxOTEyMjkxNjU5NTBfMTA3NTg3MzU2NF8yMTA2MjkzODU0NV8yXzM=_b_Bf7c15c1664b78a6881aba243a80960b2.mp4?tag=1-1582859593-unknown-1-h6j2jf5f3r-d511eb9420a3a930&type=hot"
			}],
			"cover_thumbnail_urls": [{
				"cdn": "js2.a.yximgs.com",
				"url": "http://js2.a.yximgs.com/upic/2019/12/29/16/BMjAxOTEyMjkxNjU5NTBfMTA3NTg3MzU2NF8yMTA2MjkzODU0NV8yXzM=_low_B8499b8472678c4db39aa38fa35570a6c.webp?tag=1-1582859593-unknown-0-8ylxhksalx-a714f9fbce99088c&type=hot"
			}, {
				"cdn": "ali2.a.yximgs.com",
				"url": "http://ali2.a.yximgs.com/upic/2019/12/29/16/BMjAxOTEyMjkxNjU5NTBfMTA3NTg3MzU2NF8yMTA2MjkzODU0NV8yXzM=_low_B8499b8472678c4db39aa38fa35570a6c.webp?tag=1-1582859593-unknown-1-7jtg6au2us-396ed6241db56f18&type=hot"
			}],
			"main_mv_urls_h265": [{
				"cdn": "jsmov2.a.yximgs.com",
				"url": "http://jsmov2.a.yximgs.com/upic/2019/12/29/16/BMjAxOTEyMjkxNjU5NTBfMTA3NTg3MzU2NF8yMTA2MjkzODU0NV8yXzM=_swft_B5f39c55bc73b7dbcaeeab16f61348e2d.mp4?tag=1-1582859593-unknown-0-v6ondpxcul-a6be2cc4ca5f8baa&type=hot"
			}, {
				"cdn": "alimov2.a.yximgs.com",
				"url": "http://alimov2.a.yximgs.com/upic/2019/12/29/16/BMjAxOTEyMjkxNjU5NTBfMTA3NTg3MzU2NF8yMTA2MjkzODU0NV8yXzM=_swft_B5f39c55bc73b7dbcaeeab16f61348e2d.mp4?tag=1-1582859593-unknown-1-g8apiji8gr-53f6ff89b8f77039&type=hot"
			}],
			"comments": [],
			"us_c": 0,
			"comment_count": 4326,
			"following": 0,
			"verifiedDetail": {
				"description": "游戏领域创作者",
				"iconType": 1,
				"newVerified": true,
				"musicCompany": false,
				"type": 4
			},
			"kwaiId": "mengleimenglei2018",
			"verified": true,
			"user_sex": "M",
			"headurls": [{
				"cdn": "ali2.a.yximgs.com",
				"url": "http://ali2.a.yximgs.com/uhead/AB/2020/02/27/17/BMjAyMDAyMjcxNzE2MjVfMTA3NTg3MzU2NF8yX2hkMjRfMjM4_s.jpg",
				"urlPattern": "http://aliimg.a.yximgs.com/uhead/AB/2020/02/27/17/BMjAyMDAyMjcxNzE2MjVfMTA3NTg3MzU2NF8yX2hkMjRfMjM4_s.jpg@0e_0o_0l_{h}h_{w}w_85q.src"
			}, {
				"cdn": "js2.a.yximgs.com",
				"url": "http://js2.a.yximgs.com/uhead/AB/2020/02/27/17/BMjAyMDAyMjcxNzE2MjVfMTA3NTg3MzU2NF8yX2hkMjRfMjM4_s.jpg",
				"urlPattern": "http://js2.a.yximgs.com/uhead/AB/2020/02/27/17/BMjAyMDAyMjcxNzE2MjVfMTA3NTg3MzU2NF8yX2hkMjRfMjM4_s.jpg@base@tag=imgScale&r=0&q=85&w={w}&h={h}&rotate"
			}],
			"user_name": "AG超玩会王者梦泪",
			"moodLikeType": 0,
			"hated": 0,
			"liked": 0,
			"shareGuide": {},
			"us_d": 0,
			"enableShareToStory": true,
			"forward_stats_params": {
				"fid": "1577168521",
				"et": "1_a/2000027811785188513_t030"
			},
			"share_info": "userId=3x72h378ub5y2dy&photoId=3x7gnd4mkzvsf2a",
			"photoTextLocationInfo": {
				"leftRatio": 0.0013888889,
				"topRatio": 0.03046875,
				"widthRatio": 0.95694447,
				"heightRatio": 0.86640626
			},
			"editInfo": {},
			"duration": 46033,
			"type": 1,
			"ext_params": {
				"mtype": 3,
				"color": "0D0B0C",
				"w": 720,
				"sound": 45998,
				"h": 1280,
				"interval": 30,
				"video": 46033
			},
			"user_id": 1075873564,
			"exp_tag": "1_a/2000027811785188513_t030",
			"serverExpTag": "feed_photo|5188991213893824269|1075873564|1_a/2000027811785188513_t030",
			"reco_reason": "t030",
			"profilePagePrefetchInfo": {
				"profilePageType": 1
			},
			"followShoot": {
				"lrcUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/bs2/ost/MjEwNjI5Mzg1NDVfMTA3NTg3MzU2NA.trcx"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/bs2/ost/MjEwNjI5Mzg1NDVfMTA3NTg3MzU2NA.trcx"
				}]
			},
			"extEntry": null
		}, {
			"hasMusicTag": true,
			"music": {
				"image": "http://tx2.a.yximgs.com/udata/music/bgm_OSk5yutpU1E_Yrl6KNikqO0_scaled.jpg",
				"chorus": 66142,
				"duration": 245,
				"name": "ほたる火",
				"id": "5x2zdk4cgut7ray",
				"type": 4,
				"audioUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/udata/music/bm_eCy7v3gGIG4_v.m4a"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/udata/music/bm_eCy7v3gGIG4_v.m4a"
				}],
				"avatarUrl": "http://tx2.a.yximgs.com/udata/music/bgm_OSk5yutpU1E_Yrl6KNikqO0_scaled.jpg",
				"snippetUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/udata/music/bm_eCy7v3gGIG4_vs.m4a"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/udata/music/bm_eCy7v3gGIG4_vs.m4a"
				}],
				"snippetDuration": 60,
				"url": "http://tx2.a.yximgs.com/udata/music/bm_eCy7v3gGIG4_v.m4a",
				"imageUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/udata/music/bgm_OSk5yutpU1E_Yrl6KNikqO0_scaled.jpg"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/udata/music/bgm_OSk5yutpU1E_Yrl6KNikqO0_scaled.jpg"
				}],
				"genreId": 0,
				"artist": "a_hisa",
				"avatarUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/udata/music/bgm_OSk5yutpU1E_Yrl6KNikqO0_scaled.jpg"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/udata/music/bgm_OSk5yutpU1E_Yrl6KNikqO0_scaled.jpg"
				}],
				"audioType": 1,
				"loudness": -17.40149
			},
			"recoTags": [],
			"fashionEntranceShow": {
				"showType": 3,
				"bizId": "5x2zdk4cgut7ray"
			},
			"sameFrame": {
				"allow": false
			},
			"adminTags": [],
			"tags": [{
				"id": 17842124,
				"name": "我的快手影集",
				"rich": true,
				"tag": "我的快手影集",
				"ksOrderId": "HTBDC-DD29C86A525E"
			}],
			"tag_hash_type": 1,
			"displayTime": null,
			"time": "2020-01-08 21:38:37",
			"timestamp": 1578490717767,
			"photo_id": 5257671110347704905,
			"photo_status": 0,
			"share_count": 0,
			"view_count": 2826825,
			"like_count": 56115,
			"caption": "感谢大家2019年的陪伴，我们一起重温美好瞬间~#我的快手影集",
			"unlike_count": 0,
			"forward_count": 0,
			"plcFeatureEntryAbFlag": 0,
			"noNeedToRequestPLCApi": true,
			"main_mv_urls": [{
				"cdn": "csymov.a.yximgs.com",
				"url": "http://csymov.a.yximgs.com/upic/2020/01/08/21/BMjAyMDAxMDgyMTM4MzVfNTA0MjU1MzYyXzIxNDY3MzY5OTA4XzFfMw==_b_B09b63fc3c08f41d39376472c7e01e234.mp4?tag=1-1582859593-unknown-0-zd7igpu9ov-0ef5046a91d909a9"
			}, {
				"cdn": "jsmov2.a.yximgs.com",
				"url": "http://jsmov2.a.yximgs.com/upic/2020/01/08/21/BMjAyMDAxMDgyMTM4MzVfNTA0MjU1MzYyXzIxNDY3MzY5OTA4XzFfMw==_b_B09b63fc3c08f41d39376472c7e01e234.mp4?tag=1-1582859593-unknown-1-jqosmhbmng-8c2d176a6316b0a7"
			}],
			"cover_thumbnail_urls": [{
				"cdn": "tx2.a.yximgs.com",
				"url": "http://tx2.a.yximgs.com/upic/2020/01/08/21/BMjAyMDAxMDgyMTM4MzVfNTA0MjU1MzYyXzIxNDY3MzY5OTA4XzFfMw==_low_Beb4c582e84062ea5bffc9c4d95e60027.webp?tag=1-1582859593-unknown-0-jjs0ozbpes-f17f38740bbd28b0"
			}, {
				"cdn": "js2.a.yximgs.com",
				"url": "http://js2.a.yximgs.com/upic/2020/01/08/21/BMjAyMDAxMDgyMTM4MzVfNTA0MjU1MzYyXzIxNDY3MzY5OTA4XzFfMw==_low_Beb4c582e84062ea5bffc9c4d95e60027.webp?tag=1-1582859593-unknown-1-lavsdodhbz-688c856192435768"
			}],
			"main_mv_urls_h265": [{
				"cdn": "csymov.a.yximgs.com",
				"url": "http://csymov.a.yximgs.com/upic/2020/01/08/21/BMjAyMDAxMDgyMTM4MzVfNTA0MjU1MzYyXzIxNDY3MzY5OTA4XzFfMw==_swft_B8d58c6e0ea7d199db5f02fcbc44c37c9.mp4?tag=1-1582859593-unknown-0-czkcacmka7-f277237a01e8c857"
			}, {
				"cdn": "jsmov2.a.yximgs.com",
				"url": "http://jsmov2.a.yximgs.com/upic/2020/01/08/21/BMjAyMDAxMDgyMTM4MzVfNTA0MjU1MzYyXzIxNDY3MzY5OTA4XzFfMw==_swft_B8d58c6e0ea7d199db5f02fcbc44c37c9.mp4?tag=1-1582859593-unknown-1-tqhc7rtiku-a817949a4c789acf"
			}],
			"comments": [],
			"us_c": 0,
			"comment_count": 381,
			"following": 0,
			"verifiedDetail": {
				"description": "浙江卫视官方帐号",
				"iconType": 2,
				"newVerified": true,
				"musicCompany": false,
				"type": 7
			},
			"verified": true,
			"us_l": true,
			"user_sex": "M",
			"headurls": [{
				"cdn": "ali2.a.yximgs.com",
				"url": "http://ali2.a.yximgs.com/uhead/AB/2018/09/10/17/BMjAxODA5MTAxNzI1MDdfNTA0MjU1MzYyXzFfaGQxMzZfNDgx_s.jpg",
				"urlPattern": "http://aliimg.a.yximgs.com/uhead/AB/2018/09/10/17/BMjAxODA5MTAxNzI1MDdfNTA0MjU1MzYyXzFfaGQxMzZfNDgx_s.jpg@0e_0o_0l_{h}h_{w}w_85q.src"
			}, {
				"cdn": "js2.a.yximgs.com",
				"url": "http://js2.a.yximgs.com/uhead/AB/2018/09/10/17/BMjAxODA5MTAxNzI1MDdfNTA0MjU1MzYyXzFfaGQxMzZfNDgx_s.jpg",
				"urlPattern": "http://js2.a.yximgs.com/uhead/AB/2018/09/10/17/BMjAxODA5MTAxNzI1MDdfNTA0MjU1MzYyXzFfaGQxMzZfNDgx_s.jpg@base@tag=imgScale&r=0&q=85&w={w}&h={h}&rotate"
			}],
			"user_name": "浙江卫视中国蓝",
			"moodLikeType": 0,
			"hated": 0,
			"liked": 0,
			"shareGuide": {},
			"us_d": 0,
			"forward_stats_params": {
				"fid": "1577168521",
				"et": "1_i/2000027811785188513_t030"
			},
			"share_info": "userId=3x4du3ykwwi6e2e&photoId=3xuc62iy8ehp3mg",
			"photoTextLocationInfo": {
				"leftRatio": 0.18472221,
				"topRatio": 0.45625,
				"widthRatio": 0.6319444,
				"heightRatio": 0.3046875
			},
			"editInfo": {},
			"duration": 47200,
			"type": 1,
			"ext_params": {
				"mtype": 3,
				"color": "79635B",
				"w": 720,
				"sound": 47111,
				"h": 1280,
				"interval": 30,
				"video": 47200
			},
			"user_id": 504255362,
			"exp_tag": "1_i/2000027811785188513_t030",
			"serverExpTag": "feed_photo|5257671110347704905|504255362|1_i/2000027811785188513_t030",
			"reco_reason": "t030",
			"profilePagePrefetchInfo": {
				"profilePageType": 1
			},
			"followShoot": {
				"disableFollowShoot": true
			},
			"extEntry": null
		}, {
			"hasMusicTag": true,
			"music": {
				"image": "http://tx2.a.yximgs.com/udata/music/bm_O6kjsZcXAYY_v.jpg",
				"duration": 61,
				"name": "欢迎光顾",
				"id": "5x42vwpqek2p7na",
				"type": 4,
				"audioUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/udata/music/bm_O6kjsZcXAYY_v.m4a"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/udata/music/bm_O6kjsZcXAYY_v.m4a"
				}],
				"avatarUrl": "http://tx2.a.yximgs.com/udata/music/bm_O6kjsZcXAYY_v.jpg",
				"instrumental": true,
				"snippetUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/udata/music/bm_O6kjsZcXAYY_vs.m4a"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/udata/music/bm_O6kjsZcXAYY_vs.m4a"
				}],
				"snippetDuration": 60,
				"url": "http://tx2.a.yximgs.com/udata/music/bm_O6kjsZcXAYY_v.m4a",
				"imageUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/udata/music/bm_O6kjsZcXAYY_v.jpg"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/udata/music/bm_O6kjsZcXAYY_v.jpg"
				}],
				"genreId": 0,
				"artist": "纯音乐",
				"avatarUrls": [{
					"cdn": "tx2.a.yximgs.com",
					"url": "http://tx2.a.yximgs.com/udata/music/bm_O6kjsZcXAYY_v.jpg"
				}, {
					"cdn": "static.yximgs.com",
					"url": "http://static.yximgs.com/udata/music/bm_O6kjsZcXAYY_v.jpg"
				}],
				"audioType": 2,
				"loudness": -15.0
			},
			"recoTags": [],
			"fashionEntranceShow": {
				"showType": 3,
				"bizId": "5x42vwpqek2p7na"
			},
			"sameFrame": {
				"allow": false
			},
			"adminTags": [],
			"tags": [{
				"id": 17842124,
				"name": "我的快手影集",
				"rich": true,
				"tag": "我的快手影集",
				"ksOrderId": "HTBDC-DD29C86A525E"
			}],
			"tag_hash_type": 1,
			"displayTime": null,
			"time": "2019-12-29 15:48:18",
			"timestamp": 1577605698295,
			"photo_id": 5219953461028470142,
			"photo_status": 0,
			"share_count": 0,
			"view_count": 3024402,
			"like_count": 51050,
			"caption": "感谢大家2019年的陪伴，我们一起重温美好瞬间@喵喵互娱  2019我最怀念我的头发~#我的快手影集 #",
			"unlike_count": 0,
			"forward_count": 0,
			"plcFeatureEntryAbFlag": 0,
			"noNeedToRequestPLCApi": true,
			"main_mv_urls": [{
				"cdn": "jsmov2.a.yximgs.com",
				"url": "http://jsmov2.a.yximgs.com/upic/2019/12/29/15/BMjAxOTEyMjkxNTQ4MTZfMjM4NTYwNTE2XzIxMDU5MjE3MTQ0XzFfMw==_b_B9ae98e33b8ac82b7abe4a4443d5f3588.mp4?tag=1-1582859593-unknown-0-g9uakk7jbm-77a5af1035183d62&type=hot"
			}, {
				"cdn": "alimov2.a.yximgs.com",
				"url": "http://alimov2.a.yximgs.com/upic/2019/12/29/15/BMjAxOTEyMjkxNTQ4MTZfMjM4NTYwNTE2XzIxMDU5MjE3MTQ0XzFfMw==_b_B9ae98e33b8ac82b7abe4a4443d5f3588.mp4?tag=1-1582859593-unknown-1-j6iycqpko9-7fa274c57910d610&type=hot"
			}],
			"cover_thumbnail_urls": [{
				"cdn": "js2.a.yximgs.com",
				"url": "http://js2.a.yximgs.com/upic/2019/12/29/15/BMjAxOTEyMjkxNTQ4MTZfMjM4NTYwNTE2XzIxMDU5MjE3MTQ0XzFfMw==_low_B051bb34d954f9451750917b79f58cf45.webp?tag=1-1582859593-unknown-0-x0qzeyxec7-d71cf1da6012cc41&type=hot"
			}, {
				"cdn": "ali2.a.yximgs.com",
				"url": "http://ali2.a.yximgs.com/upic/2019/12/29/15/BMjAxOTEyMjkxNTQ4MTZfMjM4NTYwNTE2XzIxMDU5MjE3MTQ0XzFfMw==_low_B051bb34d954f9451750917b79f58cf45.webp?tag=1-1582859593-unknown-1-sg3o1nwosf-7386c18f32f24ee4&type=hot"
			}],
			"main_mv_urls_h265": [{
				"cdn": "jsmov2.a.yximgs.com",
				"url": "http://jsmov2.a.yximgs.com/upic/2019/12/29/15/BMjAxOTEyMjkxNTQ4MTZfMjM4NTYwNTE2XzIxMDU5MjE3MTQ0XzFfMw==_swft_Bb3673978b692b5b0a16b0106e80ef4e2.mp4?tag=1-1582859593-unknown-0-gsxdarpj2r-cb6f40e6e7a69f96&type=hot"
			}, {
				"cdn": "alimov2.a.yximgs.com",
				"url": "http://alimov2.a.yximgs.com/upic/2019/12/29/15/BMjAxOTEyMjkxNTQ4MTZfMjM4NTYwNTE2XzIxMDU5MjE3MTQ0XzFfMw==_swft_Bb3673978b692b5b0a16b0106e80ef4e2.mp4?tag=1-1582859593-unknown-1-kxrmjlzrhr-9aef248d167da294&type=hot"
			}],
			"comments": [],
			"us_c": 0,
			"comment_count": 2484,
			"following": 0,
			"verifiedDetail": {
				"description": "快手音乐人 快手认证用户",
				"iconType": 1,
				"newVerified": false,
				"musicCompany": false,
				"type": 5
			},
			"kwaiId": "Y574859234",
			"verified": true,
			"us_l": true,
			"user_sex": "M",
			"headurls": [{
				"cdn": "ali2.a.yximgs.com",
				"url": "http://ali2.a.yximgs.com/uhead/AB/2019/10/14/11/BMjAxOTEwMTQxMTAxMDRfMjM4NTYwNTE2XzNfaGQxODlfMA==.jpg",
				"urlPattern": "http://aliimg.a.yximgs.com/uhead/AB/2019/10/14/11/BMjAxOTEwMTQxMTAxMDRfMjM4NTYwNTE2XzNfaGQxODlfMA==.jpg@0e_0o_0l_{h}h_{w}w_85q.src"
			}, {
				"cdn": "js2.a.yximgs.com",
				"url": "http://js2.a.yximgs.com/uhead/AB/2019/10/14/11/BMjAxOTEwMTQxMTAxMDRfMjM4NTYwNTE2XzNfaGQxODlfMA==.jpg",
				"urlPattern": "http://js2.a.yximgs.com/uhead/AB/2019/10/14/11/BMjAxOTEwMTQxMTAxMDRfMjM4NTYwNTE2XzNfaGQxODlfMA==.jpg@base@tag=imgScale&r=0&q=85&w={w}&h={h}&rotate"
			}],
			"user_name": "小沈阳",
			"moodLikeType": 0,
			"hated": 0,
			"liked": 0,
			"shareGuide": {},
			"us_d": 0,
			"enableShareToStory": true,
			"forward_stats_params": {
				"fid": "1577168521",
				"et": "1_i/2000027811785188513_t030"
			},
			"share_info": "userId=3xxnp2exegthwhy&photoId=3xfjzapt5zjdafg",
			"photoTextLocationInfo": {
				"leftRatio": 0.06944445,
				"topRatio": 0.24296875,
				"widthRatio": 0.8541667,
				"heightRatio": 0.525
			},
			"editInfo": {},
			"duration": 49200,
			"type": 1,
			"ext_params": {
				"mtype": 3,
				"color": "537D39",
				"w": 720,
				"sound": 49155,
				"h": 1280,
				"interval": 30,
				"video": 49200
			},
			"user_id": 238560516,
			"exp_tag": "1_i/2000027811785188513_t030",
			"serverExpTag": "feed_photo|5219953461028470142|238560516|1_i/2000027811785188513_t030",
			"reco_reason": "t030",
			"profilePagePrefetchInfo": {
				"profilePageType": 1
			},
			"extEntry": null
		}],
		"photoCount": 25711275,
		"tag": {
			"name": "我的快手影集",
			"rich": true,
			"id": 17842124
		},
		"type": "TEXT_TAG",
		"exp_tag": "2000027811785188513_tl3"
	},
	"spider_datetime": "2020-02-28 11:13:13"
}

8. 话题信息
{
	"spider_name": "kuaishou_tag_info",
	"tagId": 17842124,
	"tagName": "我的快手影集",
	"tagInfo": {
		"textRichInfo": {
			"flashTemplateId": 0,
			"bannerUrls": [{
				"cdn": "static.yximgs.com",
				"url": "https://static.yximgs.com/bs2/adminBlock/block-20200205103600-NaVVljIr.png"
			}],
			"allowJumpFlashTemplate": false,
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
			}],
			"isCollected": false
		},
		"viewCountText": "59.8亿 播放",
		"viewCount": 5976390044,
		"photoCountText": "2572.2W 个作品",
		"tagStyleInfo": {
			"tagViewStyle": 1,
			"bannerUrls": [{
				"cdn": "static.yximgs.com",
				"url": "https://static.yximgs.com/bs2/adminBlock/block-20200205103600-NaVVljIr.png"
			}],
			"description": "2019快手影集来啦！升级至最新版本，点击下方“去生成”，或去个人主页、本地作品集查看你的快手影集吧！生成影集需要有一定的作品量，如果没有影集，请多发好看的作品，期待下次为你生成~记得与大家分享你的影集哦！"
		},
		"photoCount": 25722305
	},
	"spider_datetime": "2020-02-28 16:27:11"
}

9.话题相关热门视频信息
{
	"spider_name": "kuaishou_tag_feed_hot",
	"tagId": 17842124,
	"tagName": "我的快手影集",
	"photo_id": 5246412114540658736,
	"photoInfo": {
		"displayTime": null,
		"time": "2020-02-22 09:36:29",
		"timestamp": 1582335389891,
		"photo_id": 5246412114540658736,
		"photo_status": 0,
		"share_count": 12,
		"view_count": 21874,
		"like_count": 882,
		"caption": "@梦诗意🎈梦涵🎐创始人(O373950281) @梦诗意🎈诗涵🎐创始人(O1240820614) @梦诗意🎈意涵🎐创始人(O1389095272) @梦诗意🎈诗琪🎐(O1328881115) @梦诗意🎈玉怡🎐(O1342650079) @梦诗意🎈琪荨🎐(O1760268254) @梦诗意🎈薇琳🎐(O1484224295) @梦诗意🎈雅音🎐(O1487454382) @梦诗意🎈玉米🎐(O662758326) @梦诗意🎈薇洁🎐破三千(O1501637752) @梦诗意🎈薇婷🎐破五千(O1140672920) @梦诗意🎈雅婷🎐破1千(O846203917) @梦诗意🎈诗婷🎐冲3千(O482644033) @梦诗意🎈雅思🎐破一千(O975380652) @婷玉生活号(O1779560346) @薇婷生活号(O1560436046) @薇萌生活号(O1779521211) @梦诗意🎈梦声🎐(O1098570295) @梦诗意🎈雅琴🎐(O1641731116) @梦诗意🎈梦辉🎐(O505693622) @梦诗意🎈诗雅🎐(O428112610) @梦诗意🎈琪雅🎐(O1083512734) @梦诗意🎈琪姗🎐(O1444732379) @梦诗意🎈梦祎🎐(O1246233367) @梦诗意🎈梦耶🎐(O986134373) #我的快手影集 #希望这段视频官方能送上热门",
		"unlike_count": 0,
		"forward_count": 0,
		"plcFeatureEntryAbFlag": 0,
		"noNeedToRequestPLCApi": true,
		"cover_thumbnail_urls": [{
			"cdn": "hw.a.yximgs.com",
			"url": "http://hw.a.yximgs.com/upic/2020/02/22/09/BMjAyMDAyMjIwOTM2MjhfMTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8yXzY=_thumbnail_Bc4a758abb4ed20df44ac9b240d0fc540.webp?tag=1-1582955618-t-0-yhlp11zhbt-e3721bddb08aa801"
		}, {
			"cdn": "js2.a.yximgs.com",
			"url": "http://js2.a.yximgs.com/upic/2020/02/22/09/BMjAyMDAyMjIwOTM2MjhfMTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8yXzY=_thumbnail_Bc4a758abb4ed20df44ac9b240d0fc540.webp?tag=1-1582955618-t-1-hk8n4bladq-9491b2b70e48b36f"
		}],
		"cover_urls": [{
			"cdn": "hw.a.yximgs.com",
			"url": "http://hw.a.yximgs.com/upic/2020/02/22/09/BMjAyMDAyMjIwOTM2MjhfMTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8yXzY=_Bf5d291bd9b8cc9a4bfc5e95d4f560a72.jpg?tag=1-1582955618-t-0-73cjgktned-3ae10129dc127903"
		}, {
			"cdn": "js2.a.yximgs.com",
			"url": "http://js2.a.yximgs.com/upic/2020/02/22/09/BMjAyMDAyMjIwOTM2MjhfMTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8yXzY=_Bf5d291bd9b8cc9a4bfc5e95d4f560a72.jpg?tag=1-1582955618-t-1-m1rnmr4mc4-465c16d502625311"
		}],
		"comments": [],
		"us_c": 0,
		"comment_count": 57,
		"hasMusicTag": true,
		"music": {
			"audioUrls": [{
				"cdn": "tx2.a.yximgs.com",
				"url": "http://tx2.a.yximgs.com/bs2/ost/MjI5Mjk1MjM1ODhfOTE3ODY5MjU5.m4a"
			}, {
				"cdn": "static.yximgs.com",
				"url": "http://static.yximgs.com/bs2/ost/MjI5Mjk1MjM1ODhfOTE3ODY5MjU5.m4a"
			}],
			"nameChanged": true,
			"photoId": 5224457065962357126,
			"user": {
				"kwaiId": "dgubcccczxgh",
				"headurls": [{
					"cdn": "ali2.a.yximgs.com",
					"url": "http://ali2.a.yximgs.com/uhead/AB/2020/02/16/10/BMjAyMDAyMTYxMDE0NTJfOTE3ODY5MjU5XzJfaGQ5NzVfNTI5_s.jpg",
					"urlPattern": "http://aliimg.a.yximgs.com/uhead/AB/2020/02/16/10/BMjAyMDAyMTYxMDE0NTJfOTE3ODY5MjU5XzJfaGQ5NzVfNTI5_s.jpg@0e_0o_0l_{h}h_{w}w_85q.src"
				}, {
					"cdn": "js2.a.yximgs.com",
					"url": "http://js2.a.yximgs.com/uhead/AB/2020/02/16/10/BMjAyMDAyMTYxMDE0NTJfOTE3ODY5MjU5XzJfaGQ5NzVfNTI5_s.jpg",
					"urlPattern": "http://js2.a.yximgs.com/uhead/AB/2020/02/16/10/BMjAyMDAyMTYxMDE0NTJfOTE3ODY5MjU5XzJfaGQ5NzVfNTI5_s.jpg@base@tag=imgScale&r=0&q=85&w={w}&h={h}&rotate"
				}],
				"user_id": 917869259,
				"user_sex": "F",
				"headurl": "http://ali2.a.yximgs.com/uhead/AB/2020/02/16/10/BMjAyMDAyMTYxMDE0NTJfOTE3ODY5MjU5XzJfaGQ5NzVfNTI5_s.jpg",
				"profilePagePrefetchInfo": {
					"profilePageType": 1
				},
				"eid": "3x4dhw3cwtyk974",
				"user_name": "王甜甜.℡"
			},
			"imageUrls": [{
				"cdn": "tx2.a.yximgs.com",
				"url": "http://tx2.a.yximgs.com/bs2/ost/MjI5Mjk1MjM1ODhfOTE3ODY5MjU5.jpg"
			}, {
				"cdn": "static.yximgs.com",
				"url": "http://static.yximgs.com/bs2/ost/MjI5Mjk1MjM1ODhfOTE3ODY5MjU5.jpg"
			}],
			"artist": "王甜甜.℡",
			"avatarUrls": [{
				"cdn": "tx2.a.yximgs.com",
				"url": "http://tx2.a.yximgs.com/bs2/ost/MjI5Mjk1MjM1ODhfOTE3ODY5MjU5.jpg"
			}, {
				"cdn": "static.yximgs.com",
				"url": "http://static.yximgs.com/bs2/ost/MjI5Mjk1MjM1ODhfOTE3ODY5MjU5.jpg"
			}],
			"name": "是什么样的爱情",
			"genreId": 0,
			"audioType": 1,
			"loudness": -15.0,
			"id": "5xzpatmxwpr8cum",
			"type": 9,
			"disableEnhancedEntry": true
		},
		"recoTags": [],
		"fashionEntranceShow": {
			"showType": 3,
			"bizId": "5xzpatmxwpr8cum"
		},
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
		"verified": false,
		"user_sex": "F",
		"headurls": [{
			"cdn": "js2.a.yximgs.com",
			"url": "http://js2.a.yximgs.com/uhead/AB/2020/01/28/07/BMjAyMDAxMjgwNzU2MjhfMTEwNDk3MDk5OF8yX2hkNTAzXzk5Nw==_s.jpg",
			"urlPattern": "http://js2.a.yximgs.com/uhead/AB/2020/01/28/07/BMjAyMDAxMjgwNzU2MjhfMTEwNDk3MDk5OF8yX2hkNTAzXzk5Nw==_s.jpg@base@tag=imgScale&r=0&q=85&w={w}&h={h}&rotate"
		}, {
			"cdn": "ali2.a.yximgs.com",
			"url": "http://ali2.a.yximgs.com/uhead/AB/2020/01/28/07/BMjAyMDAxMjgwNzU2MjhfMTEwNDk3MDk5OF8yX2hkNTAzXzk5Nw==_s.jpg",
			"urlPattern": "http://aliimg.a.yximgs.com/uhead/AB/2020/01/28/07/BMjAyMDAxMjgwNzU2MjhfMTEwNDk3MDk5OF8yX2hkNTAzXzk5Nw==_s.jpg@0e_0o_0l_{h}h_{w}w_85q.src"
		}],
		"user_name": "梦诗意🎈婷玉🎐",
		"editInfo": {},
		"moodLikeType": 0,
		"hated": 0,
		"liked": 0,
		"shareGuide": {},
		"us_d": 0,
		"enableShareToStory": true,
		"forward_stats_params": {
			"fid": "1577168521",
			"et": "1_a/2000029608969927666_t30"
		},
		"share_info": "userId=3xz7errqzs45zmu&photoId=3xcw4223z97afrm",
		"type": 1,
		"ext_params": {
			"mtype": 6,
			"color": "191925",
			"f": 0,
			"atlas": {
				"volume": 1.0,
				"music": "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0.m4a",
				"cdnList": [{
					"cdn": "hw.a.yximgs.com"
				}, {
					"cdn": "js2.a.yximgs.com"
				}],
				"size": [{
					"w": 332,
					"h": 498
				}, {
					"w": 720,
					"h": 1520
				}, {
					"w": 720,
					"h": 1520
				}, {
					"w": 720,
					"h": 1520
				}, {
					"w": 720,
					"h": 1520
				}, {
					"w": 720,
					"h": 1520
				}, {
					"w": 720,
					"h": 1520
				}, {
					"w": 720,
					"h": 1520
				}, {
					"w": 720,
					"h": 1520
				}, {
					"w": 720,
					"h": 1520
				}, {
					"w": 720,
					"h": 1520
				}, {
					"w": 720,
					"h": 1520
				}, {
					"w": 720,
					"h": 1520
				}, {
					"w": 720,
					"h": 1520
				}, {
					"w": 720,
					"h": 1520
				}, {
					"w": 720,
					"h": 1520
				}, {
					"w": 720,
					"h": 1520
				}, {
					"w": 720,
					"h": 1520
				}],
				"type": 2,
				"cdn": ["hw.a.yximgs.com", "js2.a.yximgs.com"],
				"list": ["/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_0.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_1.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_2.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_3.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_4.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_5.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_6.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_7.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_8.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_9.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_10.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_11.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_12.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_13.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_14.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_15.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_16.webp", "/ufile/atlas/MTEwNDk3MDk5OF8yMzg3MDk1NTYxOV8xNTgyMzM1Mzg5ODk0_17.webp"]
			},
			"w": 580,
			"h": 872
		},
		"user_id": 1104970998,
		"exp_tag": "1_a/2000029608969927666_t30",
		"serverExpTag": "feed_photo|5246412114540658736|1104970998|1_a/2000029608969927666_t30",
		"reco_reason": "t30",
		"extEntry": null,
		"profilePagePrefetchInfo": {
			"profilePageType": 1
		}
	},
	"spider_datetime": "2020-02-29 13:53:38"
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
