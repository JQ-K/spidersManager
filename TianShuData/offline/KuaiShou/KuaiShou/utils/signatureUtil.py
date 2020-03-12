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
    #srcStr = "mod=Xiaomi%20(Redmi%20Note%204)&lon=120.174727&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270966&ver=5.2&user_id=252933812&lang=zh&count=30&privacy=public&client_key=3c2cd3f3&os=android&sig=63218036783b4ba905948234c1e617ae"
    #srcStr = "mod=Xiaomi%20(Redmi%20Note%204)&lon=120.174727&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270966&ver=5.2&user_id=252933812&lang=zh&count=30&privacy=public&os=android&sig=d32a563573e7dcba0fbee4d5278b63e4"
    #srcStr = "mod=Xiaomi%20(Redmi%20Note%204)&lon=120.174727&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270966&ver=5.2&user_id=252933812&lang=zh&count=30&privacy=public&client_key=3c2cd3f3&os=android&pcursor=0&sig=d32a563573e7dcba0fbee4d5278b63e4"
    srcStr = "mod=Xiaomi%20(Redmi%20Note%204)&lon=120.174727&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270966&ver=5.2&user_id=252933812&lang=zh&count=30&privacy=public&client_key=3c2cd3f3&os=android&pcursor=1.575344074591E12&sig=c4b8cbb2bbc240e9aa0653e955bced63"
    sig = sigUtil.getSig(srcStr)
    print(sig)

