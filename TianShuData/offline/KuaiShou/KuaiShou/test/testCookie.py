import redis
import random
conn = redis.Redis(host='zqhd5', port=6379)
cookies_list = conn.zrevrange('tianshu_did', 0, -1)
oneCookieList = bytes.decode(random.choice(cookies_list)).strip().split(';')
print(oneCookieList)

cookies_all = {}
# cookies_all['kuaishou.live.bfb1s'] = '3e261140b0cf7444a0ba411c6f227d88'
for coo in oneCookieList:
    parts = coo.split('=')
    print(parts)
    if len(parts) == 2:
        print(parts[0])
        print(parts[1])
        cookies_all[parts[0]] = parts[1]

print(cookies_all)

