#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'

import requests, json
from loguru import logger
import sys, os
from PIL import Image
import cv2
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from tianshu.utils import get_project_configs
from scrapy.utils.project import get_project_settings

def down_picture(pic_url, pic_path):
    try:
        cap = cv2.VideoCapture(pic_url)
        if cap.isOpened() == False:
            pass
        rval, frame = cap.read()
        if pic_path[-3:] == 'gif':
            header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0'}
            req = requests.get(url=pic_url, headers=header, verify=False)
            req.encoding = 'utf-8'
            with open('%s' % pic_path, "wb") as f:  # 开始写文件，wb代表写二进制文件
                f.write(req.content)
        else:
            # 可处理图片裁剪
            cv2.imwrite(pic_path, frame)
        logger.info('图片下载完成，URL:{1}'.format(pic_path, pic_url))
        return True
    except Exception as e:
        logger.error(e)
        return False


def upload_picture(pic_path):
    try:
        settings = get_project_settings()
        dev = settings.get('DEV')
        api_json = get_project_configs('api.json')
        api_info = api_json[dev]
        image_upload_api = api_info['image_upload_api']
        if 'http' in pic_path:files = {'file': requests.get(pic_path).content}
        else:files = {'file': open(pic_path, 'rb')}
        img_r = requests.post(image_upload_api, files=files, verify=False)
        img_cnt = img_r.text

        img_cnt_json = json.loads(img_cnt)
        if img_cnt_json['code'] != 0:
            logger.warning("图片上传失败！返回结果：{}".format(img_cnt))
            return None
        img_url = img_cnt_json['data']['url']
        if int(img_cnt_json['code']) == 10900:
            logger.warning("图片上传失败！返回结果："+img_cnt)
            return None
        logger.info("图片上传成功！URL：{}".format(img_url))
        return img_url
    except Exception as e:
        logger.error(e)
        return None


def get_picture_size(pic_path):
    # 获取照片长宽
    src = Image.open(pic_path)
    w = src.size[0]
    h = src.size[1]
    return w,h