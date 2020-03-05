# -*- coding: utf-8 -*-
import hashlib
import urllib
import requests

class signatureUtil():
    SALT = "382700b563f4"

    def md5(self, word):
        m = hashlib.md5()
        b = word.encode(encoding='utf-8')
        m.update(b)
        return m.hexdigest()

    def getMapFromStr(self, urlStr):
        if urlStr is None:
            return None
        urlParts = urlStr.split("&")
        urlDict = {}
        for part in urlParts:
            itemElem = part.split("=", 1)
            urlDict[itemElem[0]] = itemElem[1]
        return urlDict

    def genSignature(self, urlDict, salt):
        keyList = list(urlDict.keys())
        keyList.sort()
        rltStr = ""
        for key in keyList:
            if key == '__NStokensig' or key == 'sig':
                continue
            value = urllib.parse.unquote(urlDict[key])
            rltStr += key + "=" + value
        rltStr += salt
        sign = self.md5(rltStr)
        return sign

    def getSig(self, urlStr):
        urlDict = self.getMapFromStr(urlStr)
        return self.genSignature(urlDict, self.SALT)


if __name__ == '__main__':
    sigUtil = signatureUtil()
    #srcStr = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982abcde39d99009&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&client_key=56c3713c&os=android&pcursor=0&sig=07e7e9d39e7dc7f798bf649c65df0bac"
    #srcStr = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982abcde39d99009&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&client_key=3c2cd3f3&os=android&pcursor=0&sig=c4108057708b9ffedc2854b85f6c3ced"
    #srcStr = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_3jy88vre7strvr8f&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&client_key=3c2cd3f3&os=android&pcursor=0&sig=d676bf38646cfbf989a4c5d244806ecb"
    #srcStr = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_33258vre7strvr8f&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&client_key=5aec8372&os=android&pcursor=0&sig=75ddb713e7f6ad869dad3b84cca4839b"
    srcStr = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_33258tgr7strvr8f&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&client_key=3c2cd3f3&os=android&pcursor=0&sig=085770968bf52b0ef8c2148be950be73"
    sig = sigUtil.getSig(srcStr)
    print(sig)

