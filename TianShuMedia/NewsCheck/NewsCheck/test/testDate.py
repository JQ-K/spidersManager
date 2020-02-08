import datetime
import time

# def getEtime():
#     today = datetime.date.today()
#     tomorrow = today + datetime.timedelta(days=1)
#     return str(tomorrow)
#
# a = getEtime()
# print(a)


# a = datetime.datetime.now()
# print(a)
#
# b = time.time()
# print(b)
# print(type(b))
# c = int(time.time())
# print(c)
# print(type(c))


# a1 = "2020-01-27 11:40:00"
# # 先转换为时间数组
# timeArray = time.strptime(a1, "%Y-%m-%d %H:%M:%S")
#
# # 转换为时间戳
# timeStamp = int(time.mktime(timeArray))
# print(timeStamp)


# def strToTimeStamp(timeStr):
#     try:
#         # 先转换为时间数组
#         timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")
#         # 转换为时间戳
#         timeStamp = int(time.mktime(timeArray))
#         return timeStamp
#     except:
#         logger.info('str to timestamp error:' + timeStr)
#         return None
#
#
# print(strToTimeStamp(a1))
# print(int(time.time()))

# a = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(1580198666111/1000)))
# print(a)
#
#
# def timeStampToStr(timeStamp):
#     return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(str(timeStamp)[0:10])))
#
# print(timeStampToStr(1580198666111))


# def strToTimeStamp(timeStr):
#     try:
#         # 先转换为时间数组
#         timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")
#         # 转换为时间戳
#         timeStamp = int(time.mktime(timeArray))
#         return timeStamp
#     except:
#         return None
#
#
# a1 = "2020-01-27 11:40:00"
# print(strToTimeStamp(a1))

# filepath = '/Users/macbookpro/PycharmProjects/spidersManager/TianShuMedia/NewsCheck/2020-01-28.txt'
# c = filepath.split('/')[-1]
# print(c)

# import datetime
# def getYesterday():
#     today=datetime.date.today()
#     oneday=datetime.timedelta(days=1)
#     yesterday=today-oneday
#     return yesterday.strftime('%Y-%m-%d')
#
# y = getYesterday()
# print(y)
# print(type(y))

# def getCountStr(cnt):
#     if cnt.find('w') < 0:
#         return cnt
#     d = float(cnt.strip().replace('w', '')) * 10000
#     return str(int(d))
#
# cnt='2344'
# print(getCountStr(cnt))

def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=0)
    yesterday = today - oneday
    return yesterday.strftime('%Y-%m-%d')

a = getYesterday()
print(a)


