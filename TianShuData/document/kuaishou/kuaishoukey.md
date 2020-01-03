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