import requests

'''headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'SUB=_2AkMqi8mRf8NxqwJRmfwWxWnhb4xxzwvEieKc1zhKJRMxHRl-yT83qkpftRB6AQvnfUXimls9hl2GSsUajCG-eXZ0XHs4; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWzsxWWsMuH7dIjfPwSPm-o; _s_tentry=passport.weibo.com; Apache=5971602491889.376.1574389416544; SINAGLOBAL=5971602491889.376.1574389416544; ULV=1574389416593:1:1:1:5971602491889.376.1574389416544:; Ugrow-G0=5c7144e56a57a456abed1d1511ad79e8; YF-V5-G0=260e732907e3bd813efaef67866e5183; login_sid_t=3b90273524ad6125679f07666451ea2f; cross_origin_proto=SSL; wb_view_log=1280*7201.5; YF-Page-G0=20a0c65c6e2ee949c1f78305a122073b|1574406485|1574406381',
    'Host': 'weibo.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
}'''

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'SUB=_2AkMqi8mRf8NxqwJRmfwWxWnhb4xxzwvEieKc1zhKJRMxHRl-yT83qkpftRB6AQvnfUXimls9hl2GSsUajCG-eXZ0XHs4; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWzsxWWsMuH7dIjfPwSPm-o; _s_tentry=passport.weibo.com; Apache=5971602491889.376.1574389416544; SINAGLOBAL=5971602491889.376.1574389416544; ULV=1574389416593:1:1:1:5971602491889.376.1574389416544:; Ugrow-G0=5c7144e56a57a456abed1d1511ad79e8; YF-V5-G0=260e732907e3bd813efaef67866e5183; login_sid_t=3b90273524ad6125679f07666451ea2f; cross_origin_proto=SSL; wb_view_log=1280*7201.5; YF-Page-G0=96c3bfa80dc53c34a567607076bb434e|1574412911|1574412911',
    'Host': 'weibo.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
}


url = 'http://weibo.com/1036713140/Igj2um9gI'
rlt = requests.get(url, headers=headers).text

print(rlt)

