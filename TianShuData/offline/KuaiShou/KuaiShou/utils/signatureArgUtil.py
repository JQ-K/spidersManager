# -*- coding: utf-8 -*-
import random

class signatureArgUtil:

    def getMod(self):
        modList = ['OPPO(OPPO%20R11)', 'Xiaomi%20(MI%206%20)', 'HUAWEI%20(HUAWEI%20MLA-AL10)']
        return random.choice(modList)

    def getLon(self):
        #模拟杭州及周边范围经纬度
        intPartList = [118, 119, 120]
        intPart = str(random.choice(intPartList))
        decPart = str(random.choice(range(0, 1000000))).zfill(6)
        return intPart + '.' + decPart

    def getLat(self):
        #模拟杭州及周边范围经纬度
        intPartList = [29, 30]
        intPart = str(random.choice(intPartList))
        decPart = str(random.choice(range(0, 1000000))).zfill(6)
        return intPart + '.' + decPart


if __name__ == '__main__':
    argUtil = signatureArgUtil()
    print(argUtil.getMod())
    print(argUtil.getLon())
    print(argUtil.getLat())


