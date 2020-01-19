import requests

url = "https://live.kuaishou.com/m_graphql"

payload = "{\n    \"operationName\": \"SearchOverviewQuery\",\n    \"variables\": {\n        \"keyword\": \"666\",\n        \"ussid\": \"null\"\n    },\n    \"query\": \"query SearchOverviewQuery($keyword: String, $ussid: String) {\\n  pcSearchOverview(keyword: $keyword, ussid: $ussid) {\\n    list {\\n      ... on SearchCategoryList {\\n        type\\n        list {\\n          categoryId\\n          categoryAbbr\\n          title\\n          src\\n          __typename\\n        }\\n        __typename\\n      }\\n      ... on SearchUserList {\\n        type\\n        ussid\\n        list {\\n          id\\n          name\\n          living\\n          avatar\\n          sex\\n          description\\n          counts {\\n            fan\\n            follow\\n            photo\\n            __typename\\n          }\\n          __typename\\n        }\\n        __typename\\n      }\\n      ... on SearchLivestreamList {\\n        type\\n        lssid\\n        list {\\n          user {\\n            id\\n            avatar\\n            name\\n            __typename\\n          }\\n          poster\\n          coverUrl\\n          caption\\n          id\\n          playUrls {\\n            quality\\n            url\\n            __typename\\n          }\\n          quality\\n          gameInfo {\\n            category\\n            name\\n            pubgSurvival\\n            type\\n            kingHero\\n            __typename\\n          }\\n          hasRedPack\\n          liveGuess\\n          expTag\\n          __typename\\n        }\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"\n}"
headers = {
    "accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Length": "1497",
    "content-type": "application/json",
    "Cookie": "clientid=3; did=web_24020f9721cb3022ac0eeb1f8a1cc8a5; client_key=65890b29; kuaishou.live.bfb1s=477cb0011daca84b36b3a4676857e5a1",
    "Host": "live.kuaishou.com",
    "Origin": "https://live.kuaishou.com",
    "Referer": "https://live.kuaishou.com/search/?keyword=1",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
}

response = requests.request("POST", url, headers=headers, data = payload, verify=False)

print(response.text.encode('utf8'))
