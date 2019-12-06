# -*- coding: utf-8 -*-
import hashlib


def md5(word):
    m = hashlib.md5()
    b = word.encode(encoding='utf-8')
    m.update(b)
    return m.hexdigest()

