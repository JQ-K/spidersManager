#快手爬虫说明文档



## 一、spiders

### 1.spider:kuxuan_kol_user.py

（1）作用：从酷炫获取种子

（2）管道：KuaishouUserSeedsMySQLPipeline, KuaishouKafkaPipeline

- KuaishouUserSeedsMySQLPipeline

  主要是对MySQL库中kuaishou_user_seeds表的数据新增或更新，主要字段为：如下说明

  ```MySQL
  userId # 快手userId
  kwaiId # 快手kwaiId
  principalId, # 快手principalId
  status # 用户状态
  next_scheduling_date # 下一次任务时间
  pre_scheduling_date # 最近一次任务时间
  ```

- KuaishouKafkaPipeline

  主要是将抓取的酷炫数据发一份到kafka，主要字段为：如下说明

  ```Python
  name = scrapy.Field() # spider name, 即为为kuxuan_kol_user
  id = scrapy.Field() # 酷炫ID
  userId = scrapy.Field() # 快手userId
  kwaiId = scrapy.Field() # 快手kwaiId
  principalId = scrapy.Field() # 快手principalId
  cityName = scrapy.Field() # 城市
  fan = scrapy.Field() # 粉丝数
  headurl = scrapy.Field() # 头像url
  ku_value = scrapy.Field() # 酷炫值
  photo = scrapy.Field() # 作品数
  user_name = scrapy.Field() # 用户昵称
  user_sex = scrapy.Field() # 用户性别
  user_text = scrapy.Field() # 用户描述
  avg_view_count = scrapy.Field() 
  avg_like_count = scrapy.Field()
  avg_comment_count = scrapy.Field()
  categorys = scrapy.Field() # 分类
  
  ```

特别说明：目前已经抓取了一万多种子，且他们接口更新中，暂不使用

### 2.spider:kuaishou_register_did

（1）作用：注册快手did

（2）管道：KuaishouRedisPipeline

- KuaishouRedisPipeline

  主要是对Redis库中key为kuaishou_did的数据，建立一个did池，供快手爬虫使用，主要字段为：如下说明

  ```MySQL
  # value结构为：
  {'did': 'web_6f1b84f77f3d498ea1f8684517d9283f', 'didv': '1577082503000'}
  ```

（3）处理流程：

- [ ] step1：通过访问指定接口，产生did
- [ ] step2：通过访问特定接口，注册did



### 3.releasetask.py

（1）作用：分发任务，现在只做了简单的数据查询并分发，后期考虑如何将任务合理的分布在一天的各个时段

（2）类型：不缺失principalId任务 和  缺失principalId任务

（3）消息目的：kakfa消息列队

（4）消息结构：

- 不缺失principalId任务

  ```json
  {'name': 'kuanshou_kol_seeds', 'userId': 268937622, 'kwaiId': 'YangGe666', 'principalId': 'YangGe666'}
  ```

- 缺失principalId任务

  ```json
  {'name': 'kuanshou_seeds_search', 'userId': 570567973, 'kwaiId': '570567973'}
  ```

### 4.spider:kuaishou_search_principalid.py

（1）作用：处理releasetask发布的缺失principalId任务，即首次加入种子库，缺失principalId的情况

（2）管道：KuaishouUserSeedsMySQLPipeline, KuaishouKafkaPipeline

- 主要是对MySQL库中kuaishou_user_seeds表的数据新增或更新，主要字段为：如下说明

  ```json
  # 字段说明
  userId # 快手userId
  kwaiId # 快手kwaiId
  principalId, # 快手principalId
  status # 用户状态
  next_scheduling_date # 下一次任务时间
  pre_scheduling_date # 最近一次任务时间
  # SQL语句
  ...
  ```

- KuaishouKafkaPipeline

  主要是将抓取的快手数据发一份到kafka，主要字段为：如下说明

  ```json
  # 字段说明
  ...
  # json结构
  {'avatar': 'https://tx2.a.yximgs.com/uhead/AB/2019/06/13/10/BMjAxOTA2MTMxMDM2MzhfMTE0NzU4NjA5NF8yX2hkOTE3XzQ2MQ==_s.jpg', 'cityName': '吉林 四平市', 'constellation': '', 'description': '', 'fan': '껻뿮.\uaacbw', 'follow': '첬곝곝', 'kwaiId': '1147586094', 'liked': '곝', 'name': 'kuaishou_search_principalid', 'nickname': '玩具小故事3', 'open': '곝', 'photo': '믊뿮\uaacbꯍ', 'playback': '0', 'principalId': '3xvmq62dnjzs9q2', 'sex': 'F', 'userId': '1147586094'}
  ```

（3）监听消息的结构为：

```json
{'name': 'kuanshou_seeds_search', 'userId': 570567973, 'kwaiId': '570567973'}
```

（4）消息名称：kuanshou_seeds_search

（5）处理流程：

- [ ] step1：监听kafka消息，拦截name= kuanshou_seeds_search的消息
- [ ] step2：根据消息中的userId，通过查询接口获取principalId及相关信息，实现了spider:kuaishou_user_counts；
- [ ] step2：根据principalId，通过用户隐私信息接口获取粉丝数等相关信息，实现了spider:kuaishou_user_info；



###5.spider:kuaishou_user_counts.py

（1）作用：处理releasetask发布的缺失principalId任务，即首次加入种子库，缺失principalId的情况

（2）用途：监听kafka的kuanshou_kol_seeds消息

（2）管道： KuaishouKafkaPipeline

- KuaishouKafkaPipeline

  主要是将抓取的快手数据发一份到kafka，主要字段为：如下说明

  ```json
  # 字段说明
  ...
  # json结构
  {'avatar': 'https://tx2.a.yximgs.com/uhead/AB/2019/09/07/16/BMjAxOTA5MDcxNjQyNTFfMTExOTg5NzU5XzJfaGQ0NDJfODc2_s.jpg', 'description': '优秀的擂台霸主\n巅峰擂台对决每晚19:40分直播\n擂台赛互动群 : 1011084471', 'fan': '99.2w', 'follow': '46', 'kwaiId': 'pi7758258', 'name': 'kuaishou_user_counts', 'nickname': '王者荣耀小皮【擂台赛】', 'photo': 107, 'sex': 'M'}
  ```

（3）监听消息的结构为：

```json
{'name': 'kuanshou_kol_seeds', 'userId': 570567973, 'kwaiId': '570567973'}
```

（4）消息名称：kuanshou_kol_seeds

（5）处理流程：

- [ ] step1：监听kafka消息，拦截name= kuanshou_kol_seeds的消息
- [ ] step2：根据消息中的userId，通过查询接口获取principalId及相关信息，实现了spider:kuaishou_user_counts；

（6）相关接口：

- 查询接口api:https://live.kuaishou.com/m_graphql

  注：keyword，这里选userid。这个跟他的搜索规则有关。

  post:

  ```json
  {
      "operationName": "SearchOverviewQuery",
      "variables": {
          "keyword": "7778",
          "ussid": "null"
      },
      "query": "query SearchOverviewQuery($keyword: String, $ussid: String) {\n  pcSearchOverview(keyword: $keyword, ussid: $ussid) {\n    list {\n      ... on SearchCategoryList {\n        type\n        list {\n          categoryId\n          categoryAbbr\n          title\n          src\n          __typename\n        }\n        __typename\n      }\n      ... on SearchUserList {\n        type\n        ussid\n        list {\n          id\n          name\n          living\n          avatar\n          sex\n          description\n          counts {\n            fan\n            follow\n            photo\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on SearchLivestreamList {\n        type\n        lssid\n        list {\n          user {\n            id\n            avatar\n            name\n            __typename\n          }\n          poster\n          coverUrl\n          caption\n          id\n          playUrls {\n            quality\n            url\n            __typename\n          }\n          quality\n          gameInfo {\n            category\n            name\n            pubgSurvival\n            type\n            kingHero\n            __typename\n          }\n          hasRedPack\n          liveGuess\n          expTag\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
  }
  ```

  respose:

  ```json
  {
      "data": {
          "pcSearchOverview": {
              "list": [
                  {
                      "type": "categories",
                      "list": [
                          {
                              "categoryId": "22028",
                              "categoryAbbr": "DJRY",
                              "title": "NBA2K18",
                              "src": "https://js2.a.yximgs.com/udata/pkg/cover-game-22028-20181129163746.jpg",
                              "__typename": "Category"
                          }
                      ],
                      "__typename": "SearchCategoryList"
                  },
                  {
                      "type": "authors",
                      "ussid": "MV8wXzE1NzcwOTU2NjIzODVfNTAwNzMwMTQ4XzUxMzM",
                      "list": [
                          {
                              "id": "3xfkj9h33i6tmse",
                              "name": "🌻山西白静🎤",
                              "living": false,
                              "avatar": "https://js2.a.yximgs.com/uhead/AB/2018/04/15/22/BMjAxODA0MTUyMjQ3MDhfNTAwNzMwMTQ4XzJfaGQ1NjhfMzQy_s.jpg",
                              "sex": "F",
                              "description": "白静，山西襄汾人。童年的农家小院，田间地头，都曾留下我的歌声!喜欢结交有孝心，有爱心的朋友！\n      马甲：🌻 ……\n      🌻🌻🌻向日葵寓意：正能量的静家军，如向日葵般生气蓬勃，心向阳光！\n      每早8:30——12:00（接待电商）\n      每晚7:00——9：30（娱乐场，不卖货）\n      认真直播!风雨无阻！\n     sx5992300100",
                              "counts": {
                                  "fan": "81.9w",
                                  "follow": "652",
                                  "photo": 343,
                                  "__typename": "CountInfo"
                              },
                              "__typename": "User"
                          }
                      ],
                      "__typename": "SearchUserList"
                  },
                  {
                      "type": "liveStreams",
                      "lssid": null,
                      "list": [],
                      "__typename": "SearchLivestreamList"
                  }
              ],
              "__typename": "SearchOverview"
          }
      }
  }
  ```

  

### 6.spider:kuaishou_user_info.py

（1）作用：根据principalId，更新用户隐私信息数据，包括：kwaiId，userId，constellation，cityName，fan，follow，photo，liked，open

（2）用途：监听kuanshou_kol_seeds，批量处理用户信息缺失的情况。比如适合目前有种子，但无用户信息的情况

（3）管道： KuaishouKafkaPipeline

- KuaishouKafkaPipeline

  主要是将抓取的快手数据发一份到kafka，主要字段为：如下说明

  ```json
  # 字段说明
  ...
  # json结构
  {'cityName': '广西 南宁市', 'constellation': '双鱼座', 'fan': '뿮뿮.첬w', 'follow': '뿮뿮.첬w', 'kwaiId': 'pi7758258', 'liked': '뿮뿮.첬w', 'name': 'kuaishou_user_info', 'open': '뿮뿮.첬w', 'photo': '뿮뿮.첬w', 'playback': '뿮뿮.첬w', 'principalId': 'pi7758258', 'userId': '111989759'}
  ```

（3）监听消息的结构为：

```json
{'name': 'kuanshou_kol_seeds', 'userId': 570567973, 'kwaiId': '570567973'}
```

（4）消息名称：kuanshou_kol_seeds

（5）处理流程：

- [ ] step1：监听kafka消息，拦截name= kuanshou_kol_seeds的消息
- [ ] step2：根据消息中的userId，通过查询接口获取principalId及相关信息，实现了spider:kuaishou_user_counts；

（6）相关接口：

- 用户隐私信息接口api:https://live.kuaishou.com/graphql

  post:

  ```json
  {
      "operationName": "sensitiveUserInfoQuery",
      "variables": {
          "principalId": "3xjcyhicecuz54q"
      },
      "query": "query sensitiveUserInfoQuery($principalId: String) {\n  sensitiveUserInfo(principalId: $principalId) {\n    kwaiId\n    userId\n    constellation\n    cityName\n    countsInfo {\n      fan\n      follow\n      photo\n      liked\n      open\n      playback\n      private\n      __typename\n    }\n    __typename\n  }\n}\n"
  }
  ```

  respose:

  ```json
  {
  	"data": {
  		"sensitiveUserInfo": {
  			"kwaiId": "842036714",
  			"userId": "842036714",
  			"constellation": "",
  			"cityName": "安徽 蚌埠市",
  			"countsInfo": {
  				"fan": "궬.궪w",
  				"follow": "궪궬",
  				"photo": "궬ꫝ뺻",
  				"liked": "ꫝ",
  				"open": "ꫝ",
  				"playback": "0",
  				"private": "ꫝ",
  				"__typename": "CountsInfo"
  			},
  			"__typename": "User"
  		}
  	}
  }
  ```



### 7.spider:kuaishou_user_photo_info.py

### 8.spider:kuaishou_photo_comment.py

