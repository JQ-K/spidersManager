# -*- coding: utf-8 -*-
import time
import datetime


def getCurDate():
    curTime = time.strftime("%Y%m%d", time.localtime())
    return int(curTime)


def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today-oneday
    return yesterday