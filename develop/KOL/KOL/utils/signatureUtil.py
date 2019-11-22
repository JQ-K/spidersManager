# -*- coding: utf-8 -*-

class signatureUtil():
    FANS_SALT = "382700b563f4"

    def getMapFromStr(self, urlStr):
        if urlStr is None:
            return None
        utlParts = urlStr.split("&")
        urlDict = {}