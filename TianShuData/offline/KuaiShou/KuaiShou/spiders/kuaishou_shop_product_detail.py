# -*- coding: utf-8 -*-
import scrapy
import json

from pykafka import KafkaClient
from loguru import logger
from scrapy.utils.project import get_project_settings

from KuaiShou.items import KuaishouShopProductDetailItem


class KuaishouShopProductDetailSpider(scrapy.Spider):
    name = 'kuaishou_shop_product_detail'
    url = "https://www.kwaishop.com/rest/app/grocery/product/self/detail?itemId={}"


