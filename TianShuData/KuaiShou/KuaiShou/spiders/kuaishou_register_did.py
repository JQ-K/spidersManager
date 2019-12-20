# -*- coding: utf-8 -*-
import scrapy

from loguru import logger
import re,time
import json, requests

from KuaiShou.utils import ProduceRandomStr


class KuaishouRegisterDidSpider(scrapy.Spider):
    name = 'kuaishou_register_did'
    # allowed_domains = ['live.kuaishou.com/graphql']
    # start_urls = ['http://live.kuaishou.com/graphql/']

    host = 'live.kuaishou.com'
    origin = 'https://live.kuaishou.com'
    headers = {}

    def start_requests(self):
        # start_url = 'https://live.kuaishou.com/v/hot/'
        start_url = 'https://live.kuaishou.com/profile/h2296602615'
        yield scrapy.Request(start_url, method='GET', callback=self.produce_did)

    def produce_did(self, response):
        referer = response.url
        cookie = re.findall('(kuaishou\.live\.bfb1s=[0-9a-z]+; )', str(response.headers))[0] \
                 + re.findall('(clientid=\d{0,}; )', str(response.headers))[0] \
                 + re.findall('(did=web_[0-9a-z]+; )', str(response.headers))[0] \
                 + re.findall('(client_key=[0-9a-z]+; )', str(response.headers))[0] \
                 + re.findall('(didv=\d+)', str(response.headers))[0]

        graphql_url = 'https://live.kuaishou.com/graphql'
        userInfoQuery = {"operationName": "userInfoQuery", "variables": {},
                         "query": "query userInfoQuery {\n  kshellBalance {\n    kshell\n    __typename\n  }\n  ownerInfo {\n    id\n    principalId\n    kwaiId\n    eid\n    userId\n    profile\n    name\n    description\n    sex\n    constellation\n    cityName\n    following\n    living\n    watchingCount\n    isNew\n    privacy\n    timestamp\n    feeds {\n      eid\n      photoId\n      thumbnailUrl\n      timestamp\n      __typename\n    }\n    verifiedStatus {\n      verified\n      description\n      type\n      new\n      __typename\n    }\n    countsInfo {\n      fan\n      follow\n      photo\n      liked\n      open\n      playback\n      private\n      __typename\n    }\n    bannedStatus {\n      banned\n      defriend\n      isolate\n      socialBanned\n      __typename\n    }\n    __typename\n  }\n}\n"}
        # categoryListQuery = {"operationName": "categoryListQuery",
        #                      "variables": {"type": "brief", "categoryCardList": "true"},
        #                      "query": "query categoryListQuery($limit: Int, $type: String, $categoryCardList: Boolean) {\n  categoryList(limit: $limit, type: $type, categoryCardList: $categoryCardList) {\n    list {\n      id\n      categoryId\n      text\n      category\n      title\n      src\n      roomNumber\n      shortName\n      gameDescription\n      watchingCount\n      subList\n      __typename\n    }\n    __typename\n  }\n}\n"}
        # searchHotQuery = {"operationName": "searchHotQuery", "variables": {"limit": 5},
        #                   "query": "query searchHotQuery($limit: Int) {\n  searchHot(limit: $limit) {\n    hotWords\n    __typename\n  }\n}\n"}
        # commentListQuery = {"operationName": "commentListQuery", "variables": {},
        #                     "query": "query commentListQuery($photoId: String, $page: Int, $pcursor: String, $count: Int) {\n  shortVideoCommentList(photoId: $photoId, page: $page, pcursor: $pcursor, count: $count) {\n    commentCount\n    realCommentCount\n    pcursor\n    commentList {\n      commentId\n      authorId\n      authorName\n      content\n      headurl\n      timestamp\n      authorEid\n      status\n      subCommentCount\n      subCommentsPcursor\n      likedCount\n      liked\n      subComments {\n        commentId\n        authorId\n        authorName\n        content\n        headurl\n        timestamp\n        authorEid\n        status\n        replyToUserName\n        replyTo\n        replyToEid\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}

        followInfoQuery = {"operationName": "followInfoQuery", "variables": {"principalId": "h2296602615"},
         "query": "query followInfoQuery($principalId: String) {\n  userInfo(principalId: $principalId) {\n    following\n    __typename\n  }\n}\n"}
        payloads = [userInfoQuery, followInfoQuery]
        self.headers['Cookie'] = '{};kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAe2shej7Uyocn0Mr2prd07W7bpZoxFTnEQr4PLmrVxbQlMk4t3FK2i3HTPcAMLVGLfrAzqtzrf8HLr11kmfVYNT6vpvNEmW3_9Vy2u6SSpg6zgBsOFNWTJH7OnnJDg1g4-I3bYzQqsx9Cz-Re8KbEmP4xuDzmGMunpTKDorM5MSUCe3rtbpplGDSrcv5CfKJ_060gCr6-RLMJ527Nydaj48aEo_d-PiuxE4duU2DjxXdbB5BSiIgDTlRnYYHZixhDUQh5d2drkZFB24vblRoboYdO1TStKUoBTAB'.format(cookie)
        self.headers['Referer'] = referer
        for query in payloads:
            time.sleep(0.1)
            scrapy.Request(graphql_url, headers=self.headers, body=json.dumps(query),
                           method='POST', meta={'bodyJson': query},
                           dont_filter=True
                           )
        time_int = int(time.time() * 1000)
        collect_url = 'https://live.kuaishou.com/rest/wd/live/web/collect'
        from_data = {

                "session_id": ProduceRandomStr(16),
                "page_id": "{}_{}".format(ProduceRandomStr(16),time_int-31012),
                "refer_page_id": "{}_{}".format(ProduceRandomStr(16),time_int-1012),
                "refer_show_id": "",
                "refer_url": "https://live.kuaishou.com/profile/h2296602615",
                "page_live_stream_id": "",
                "url": "https://live.kuaishou.com/profile/h2296602615",
                "screen": "1920*1080",
                "platform": "MacIntel",
                "log_time": "{}".format(time_int-1000),
                "from": "/",
                "to": "/profile/h2296602615",
                "type": "pv",
                "is_spammer": "false",
        }

        self.headers['kpf'] = 'PC_WEB'
        self.headers['kpn'] = 'GAME_ZONE'
        self.headers['Content-Type'] = "multipart/form-data; boundary=----WebKitFormBoundaryXRz4hTchXEz8VWW3"
        self.headers['Accept-Encoding'] = 'gzip, deflate, br'
        self.headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
        self.headers['Connection'] = 'keep-alive'
        self.headers['Sec-Fetch-Mode'] = 'cors'
        self.headers['Sec-Fetch-Site'] = 'same-origin'
        self.headers[
            'User-Agent'] = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'

        yield scrapy.Request(collect_url, headers=self.headers, body=json.dumps(from_data),
                       method='POST', meta={'bodyJson': from_data}, callback=self.pare_process_mode,
                       dont_filter=True
                       )

    def pare_process_mode(self, response):
        logger.info(response.text)


    #     time_int = int(time.time() * 1000)
    #     register_url = 'https://live.kuaishou.com/rest/wd/live/web/log'
    #     payload_data = {
    #         "base": {
    #             "session_id": ProduceRandomStr(16),
    #             "page_id": '{}_{}'.format(ProduceRandomStr(16),time_int-1012),
    #             "refer_page_id": "",
    #             "refer_show_id": "",
    #             "refer_url": "https://live.kuaishou.com/profile/h2296602615",
    #             "page_live_stream_id": "",
    #             "url": "https://live.kuaishou.com/profile/h2296602615",
    #             "screen": "1280*800",
    #             "platform": "MacIntel",
    #             "log_time": "{}".format(time_int)
    #         },
    #         "events": [{
    #             "type": "pv",
    #             "data": {
    #                 "event_time": time_int-1012,
    #                 "from": "/",
    #                 "to": "/v/hot/",
    #                 "is_spammer": 'false'
    #             }
    #         }]
    #     }
    #
    #     self.headers['kpf'] = 'PC_WEB'
    #     self.headers['kpn'] = 'GAME_ZONE'
    #     self.headers['Content-Type'] = "text/plain;charset=UTF-8"
    #     self.headers['Accept-Encoding'] = 'gzip, deflate, br'
    #     self.headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
    #     self.headers['Connection'] = 'keep-alive'
    #     self.headers['Sec-Fetch-Mode'] = 'cors'
    #     self.headers['Sec-Fetch-Site'] = 'same-origin'
    #     self.headers['User-Agent'] = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'
    #
    #     yield scrapy.Request(register_url, headers=self.headers, body=json.dumps(payload_data),
    #                        method='POST', meta={'cookie': cookie}, callback=self.parse,
    #                        dont_filter=True
    #                        )
    #
    #     logger.info(self.headers)
    #
    # def parse(self, response):
    #     logger.info(response.text)
    #     logger.info(response.meta['cookie'])
