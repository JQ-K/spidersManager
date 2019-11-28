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
    #srcStr = "app=0&lon=104.073269&did_gt=1551777466213&c=XIAOMI&sys=ANDROID_4.4.4&isp=&mod=Xiaomi%28MI%203%29&did=ANDROID_b07d34ee8ff226b0&hotfix_ver=&ver=6.1&net=WIFI&country_code=cn&iuid=&appver=6.1.2.8197&max_memory=192&oc=XIAOMI&ftt=&kpn=KUAISHOU&ud=1273257807&language=zh-cn&kpf=ANDROID_PHONE&lat=30.537794&user=74476707&token=6f8b8954c34e4462a1c0117ac5a5af21-1273257807&os=android&client_key=3c2cd3f3&sig=8ab207f1762b17b47d1ca0cc26ce6576&__NStokensig=334b7f77f9fec536c1dce00467f8cf79bed4f66cd8a24ffc205b3e1a151ab1e7"
    #srcStr = "mod=samsung(SM-G9200)&lon=120.117064&country_code=CN&did=ANDROID_7022e02d3b4933ec&net=WIFI&app=0&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_7.0&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.289624&ver=5.2&user=751807786&client_key=3c2cd3f3&os=android&sig=2475e92f9215920839513bb7693277e8"
    #srcStr = "mod=samsung(SM-G9200)&lon=120.117064&country_code=CN&did=ANDROID_7022e02d3b4933ec&net=WIFI&app=0&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_7.0&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.289624&ver=5.2&user=1075873564&client_key=3c2cd3f3&os=android&sig=2475e92f9215920839513bb7693277e8"
    #srcStr = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&type=7&page=2&coldStart=false&count=20&pv=false&id=6&refreshTimes=2&pcursor=&client_key=3c2cd3f3&os=android&sig=7acac1aa2531bde42798be884cae175d"
    #srcStr = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&type=7&page=1&coldStart=false&count=20&pv=false&id=6&refreshTimes=2&pcursor=&client_key=3c2cd3f3&os=android&sig=d2f719f141a45a24c173c5f421f3be2d"
    #srcStr = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&type=7&page=1&coldStart=false&count=20&pv=false&id=6&refreshTimes=2&pcursor=&client_key=3c2cd3f3&os=android"
    #srcStr = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&user=1215741150&client_key=3c2cd3f3&os=android&sig=723e6c8f2c74fea99fbc89bcc6d36737"
    #srcStr = "mod=OPPO(OPPO%20R11)&lon=120.174975&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270968&ver=5.2&token=&user_id=605395700&lang=zh&count=30&privacy=public&referer=ks%3A%2F%2Fprofile%2F605395700%2F5221360837644739313%2F1_a%2F2000005775957550673_h495%2F8&client_key=3c2cd3f3&os=android"
    #srcStr = "mod=samsung(SM-G9200)&lon=120.174933&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270955&ver=5.2&user=325629379&client_key=3c2cd3f3&os=androi"
    srcStr = "mod=samsung(SM-G9200)&lon=120.174933&country_code=CN&did=ANDROID_982cbccac9d99034&app=0&net=WIFI&oc=UNKNOWN&ud=0&c=ALI_CPD&sys=ANDROID_5.1.1&appver=5.2.1.4686&ftt=&language=zh-cn&lat=30.270955&ver=5.2&user=325629379&client_key=3c2cd3f4&os=android&sig=d3cb0a1b766a33dd15d2da9b95d5122c"
    sig = sigUtil.getSig(srcStr)
    print(sig)

