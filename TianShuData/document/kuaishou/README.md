# 天枢数据说明文档





###  一、项目结构

```python
.
├── __init__.py
├── offline
│   ├── KuaiShou
│   │   ├── KuaiShou
│   │   │   ├── __init__.py
│   │   │   ├── items.py
│   │   │   ├── middlewares.py
│   │   │   ├── pipelines.py
│   │   │   ├── settings.py
│   │   │   ├── spiders
│   │   │   │   ├── __init__.py
│   │   │   │   ├── kuaishou_photo_comment.py
│   │   │   │   ├── kuaishou_register_did.py
│   │   │   │   ├── kuaishou_search_principalid.py
│   │   │   │   ├── kuaishou_shop_info.py
│   │   │   │   ├── kuaishou_shop_product.py
│   │   │   │   ├── kuaishou_shop_product_comment.py
│   │   │   │   ├── kuaishou_shop_product_detail.py
│   │   │   │   ├── kuaishou_user_info.py
│   │   │   │   ├── kuaishou_user_photo_info.py
│   │   │   │   └── kuxuan_kol_user.py
│   │   │   └── utils
│   │   │       ├── __init__.py
│   │   │       ├── decoder.py
│   │   │       ├── did.py
│   │   │       ├── mysql.py
│   │   │       ├── signatureUtil.py
│   │   │       ├── spiderplan.py
│   │   │       └── useragent.py
│   │   ├── README.md
│   │   ├── execute.py
│   │   └── scrapy.cfg
│   └── ProxyIP
│       ├── ProxyIP
│       │   ├── __init__.py
│       │   ├── items.py
│       │   ├── middlewares.py
│       │   ├── pipelines.py
│       │   ├── settings.py
│       │   ├── spiders
│       │   │   ├── __init__.py
│       │   │   ├── ip3366_free.py
│       │   │   ├── iphai_free.py
│       │   │   ├── ipyqie_free.py
│       │   │   ├── kuaidaili_free.py
│       │   │   ├── qydaili_free.py
│       │   │   ├── xicidaili_free.py
│       │   │   └── y89ip_free.py
│       │   └── utils
│       │       ├── __init__.py
│       │       └── useragent.py
│       ├── ProxyIP.zip
│       ├── execute.py
│       └── scrapy.cfg
└── online
    └── KuaiShou
        ├── KuaiShou
        │   ├── __init__.py
        │   ├── items.py
        │   ├── middlewares.py
        │   ├── pipelines.py
        │   ├── settings.py
        │   ├── spiders
        │   │   ├── __init__.py
        │   │   └── kuaishou_user_counts.py
        │   └── utils
        │       ├── __init__.py
        │       ├── decoder.py
        │       ├── did.py
        │       ├── mysql.py
        │       ├── signatureUtil.py
        │       ├── spiderplan.py
        │       └── useragent.py
        ├── README.md
        ├── execute.py
        ├── online_kuaishou.zip
        └── scrapy.cfg

```

### 二、项目说明

整个项目分按照运营得类型分为两块：实时更新和离线更新。下面分别对二者进行详细的说明：

- 实时更新

  1.KuaiShou项目工程

  该工程基于scrapy框架，对快手得相关信息进行爬取，并将抓取得数据结果分发到kafka消息列队中，其中topic为[暂为tianshu_online]，下面详细说明框架中各个代码得功能。

  

  

  

- 离线更新

