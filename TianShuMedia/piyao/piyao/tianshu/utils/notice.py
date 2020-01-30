#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'

import requests
import json
from loguru import logger


class DingDingMsg:
    def __init__(self, atMobiles=[], isAtAll=False, msgNotify=False):
        self.msgtype = "text"
        self.content = ""
        self.atMobiles = atMobiles
        self.isAtAll = isAtAll
        self.msgNotify = msgNotify
        self.url = "https://oapi.dingtalk.com/robot/send?access_token=c67222252406a8f79450706269edad1b907ce6f7ecee9b719c5ca81124172cd2"

    def send(self, content):
        if self.msgNotify is False:
            return
        self.content = content
        try:
            data = {
                "msgtype": self.msgtype,
                "text": {
                    "content": self.content
                },
                "at": {
                    "atMobiles": self.atMobiles,
                    "isAtAll": self.isAtAll,
                }
            }
            headers = {
                "Content-Type": "application/json;charset=utf-8"
            }
            requests.post(self.url, data=json.dumps(data), headers=headers, verify = False)
        except Exception as ex:
            logger.error(ex)


if __name__ == '__main__':
    atMobiles = [18758879865]
    app = DingDingMsg(atMobiles, False, True)
    app.send(
        '2019-10-22 17:47:49.679 | INFO     | scrapypjt.utils.record:public_record:31 - 发布成功！{"code":0,"message":"SUCCESS","data":{"id":"443"}}')
