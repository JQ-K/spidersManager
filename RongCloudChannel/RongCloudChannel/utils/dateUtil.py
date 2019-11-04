# -*- coding: utf-8 -*-
import time

def getCurDate():
    curTime = time.strftime("%Y%m%d", time.localtime())
    return int(curTime)

