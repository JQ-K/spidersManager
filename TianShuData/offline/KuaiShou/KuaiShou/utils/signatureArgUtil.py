# -*- coding: utf-8 -*-
import random

class signatureArgUtil:

    def getMod(self):
        modList = ['OPPO(OPPO%20R11)',
                   'Xiaomi%20(MI%206%20)',
                   'Xiaomi%20(Mi%20Note%202)',
                   'HUAWEI%20(HUAWEI%20MLA-AL10)',
                   'vivo(vivo%20X20)',
                   'vivo(vivo%20X20A)',
                   'vivo(vivo%20X9i)',
                   'Meizu(M6%20Note)', ]
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

    def getDid(self):
        #模拟did：ANDROID_982abcde39d99009，ANDROID_后跟上16位数字英文组成的字符串
        preStr = 'ANDROID_'
        chList = [chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]
        rltList = [random.choice(chList) for i in range(16)]
        return preStr + ''.join(rltList)

    def getClientKey(self):
        #client_key随机模拟结果不可使用
        #client_key:需要安装5.2版本真实的client_key,使用新版本client_key会提示签名验证失败
        # {
        #     "result": 40,
        #     "error_msg": "服务器繁忙，请稍后再试。"
        # }
        # {
        #     "result": 3,
        #     "error_msg": "客户端版本太旧，请升级到最新版本。"
        # }
        pass


if __name__ == '__main__':
    argUtil = signatureArgUtil()
    print(argUtil.getMod())
    print(argUtil.getLon())
    print(argUtil.getLat())
    print(argUtil.getDid())


