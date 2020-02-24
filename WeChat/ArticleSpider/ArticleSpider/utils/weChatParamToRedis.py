__author__ = 'zlx'


"""
-------------------------------------------------------------------------------
Function:   using for get wechat param
在windows端设置成定时任务 每点击30个微信公众号 启动一次
-------------------------------------------------------------------------------
"""
import datetime
import string,re,time
from loguru import logger
from redis import Redis
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from scrapy.utils.project import get_project_settings


filePath='D:/fiddler_outfile/'

class WeChatParams:
    def __init__(self):
        settings = get_project_settings()
        self.redis_host = settings.get('REDIS_HOST')
        self.redis_port = settings.get('REDIS_PORT')

        self.redis_wechat_params = settings.get('REDIS_WECHAT_PARAMS')
        self.red = Redis(host=self.redis_host, port=self.redis_port)
        logger.info('RedisConn:host = %s,port = %s' % (self.redis_host, self.redis_port))

    def get_match(self,data):
        #data是一个文件中的全部数据，for line in data :对每一行进行分析，这一行符合条件即存储到redis中
        param_dict={}
        reg_str=''r"Request url: mp.weixin.qq.com/mp/getmasssendmsg(.+)"''
        for line in data:
            reg_match = re.findall(reg_str, line)
            if reg_match:
                result=reg_match[0][1:]  #返回字符串
                list=result.split("&")
                for one in list:
                    #获取第一个=的位置
                    index=one.index('=')
                    key=one[:index]
                    value=one[index+1:]
                    # print(key,':',value)
                    param_dict[key]=value
                biz= param_dict.get("__biz","")
                uin_key=param_dict.get("uin","")+'_'+param_dict.get("key","")
                self.red.hmset(self.redis_wechat_params,{biz:uin_key})
                logger.info("发送一个参数成功")


    def change_txt(self):
        print('开始change_txt')
        f=open(filePath+'Sessions.txt','r',encoding='gbk',errors='ignore')
        data=f.readlines()
        # try:
        #     f =open("D:/1.txt",'r')
        #     f.close()
        # except IOError:
        #     f = open("D:/1.txt",'w')

        file_write_new=open(filePath+'New_Sessions.txt','wb')
        for i in data:
            i=str(i).replace("b'",'').replace("'",'')
            # i.replace('\x00','')
            hope=''.join(list(filter(lambda x: x in string.printable, i)))
            if hope.startswith('#')or not hope.split():
                continue
            file_write_new.write(bytes(hope,encoding='utf-8'))
            # print(bytes(hope,encoding='utf-8'))
        file_write_new.close()
        f.close()


    def get_key(self):
        #第一步要先检查文件夹中是否含有指定文件，如果没有则不执行脚本
        session_fname='Sessions.txt'
        try:
            files=os.listdir(filePath)
            if session_fname in files:
                self.change_txt()
                f=open(filePath+'New_Sessions.txt','r',encoding='utf-8',errors='ignore')
                data=f.readlines()
                # print(data)
                self.get_match(data)
                #文件中数据已经处理，则把文件删除，删除该路径下的所有文件
                files=os.listdir(filePath)  #如果文件夹、文件不存在会报错
                print(files)
                if files:
                    for file in files:
                       os.remove(filePath+file)


        except Exception as e:
            logger.warning('wechatParamToRedis Error :{}'.format(str(e)))



if __name__=="__main__":
    print(datetime.datetime.now())
    wechatParams=WeChatParams()
    #目前测试数据库中116个公众号
    wechatParams.get_key()    #此时运行时间4s,网速不同发送参数所需时间不同
    print(datetime.datetime.now())

    # main = "C:/Users/zlx/Desktop/autoClickWechat.exe"   #按键精灵脚本exe
    '''
    备注：1、按键精灵脚本中指定微信安装位置为：ADDRESS = "D:\Program Files (x86)\Tencent\WeChat\WeChat.exe"，
          当按键精灵脚本挪到别处使用，需要相同的安装位置
          2、打开微信公众号页面时，微信公众号排列为5*3
          3、
    '''
    # r_v = os.system(main)
    # print (r_v ) #os.system() 会保存可执行程序中的打印值和主函数的返回值，且会将执行过程中要打印的内容打印出来
    # sched = BlockingScheduler()
    # #每隔一天 执行抓包程序
    # # sched.add_job(everyday_crawler_job, 'interval', days=1)days
    # # sched.add_job(os.system(main),'interval', minutes=2,start_date='2020-02-24 9:50:00',end_date='2020-02-24 10:06:00')
    # sched.add_job(wechatParams.get_key(), 'interval', minutes=2,start_date='2020-02-24 9:51:00',end_date='2020-02-24 10:07:00')
    # #每天早上八点半和十二点半各执行一次抓包程序
    # # sched.add_job(os.system(main), 'cron', hour='9', minute='30')  #这个脚本在某个时刻开始一直运行着，内部每运行15个会等待1分钟
    # # sched.add_job(wechatParams.get_key(), 'cron', hour='9', minute='31,33,35,37,39,41,43,45')  #2s，每15个大约只需要2s
    # sched.start()
    # #按键精灵也是3分钟执行一次，按键精灵等待的时间，weChatParamToRedis的任务启动
    #
