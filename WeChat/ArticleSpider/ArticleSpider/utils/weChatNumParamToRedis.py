__author__ = 'zlx'
# -*- coding: utf-8 -*-

"""
-------------------------------------------------------------------------------
Function:   using for get wechat param

-------------------------------------------------------------------------------
"""
import datetime
import string,re,time
from loguru import logger
from pykafka import KafkaClient
from redis import Redis
import os
import pymysql
from apscheduler.schedulers.blocking import BlockingScheduler
from scrapy.utils.project import get_project_settings
import sys

filePath='D:/fiddler_outfile/'

class WeChatParams:
    def __init__(self):
        settings = get_project_settings()
        #配置redis
        self.redis_host = settings.get('REDIS_HOST')
        self.redis_port = settings.get('REDIS_PORT')
        self.redis_wechat_numParams = settings.get('REDIS_WECHAT_NUMPARAMS')
        self.red = Redis(host=self.redis_host, port=self.redis_port)
        logger.info('RedisConn:host = %s,port = %s' % (self.redis_host, self.redis_port))
        #配置mysql
        self.mysql_host = settings.get('MYSQL_HOST')
        self.mysql_user = settings.get('MYSQL_USER')
        self.mysql_password = settings.get('MYSQL_PASSWORD')
        self.mysql_database = settings.get('MYSQL_DATABASE_WECHAT')
        self.table_name=settings.get('MYSQL_WECHAT_ACCOUNT_INFO_TABLENAME')
        logger.info(
            'MySQLConn:host = %s,user = %s,db = %s' % (self.mysql_host, self.mysql_user, self.mysql_database))
        self.conn = pymysql.connect(host=self.mysql_host, user=self.mysql_user, password=self.mysql_password,
                                        database=self.mysql_database, port=3306, charset="utf8")

         # 配置kafka连接信息
        self.kafka_hosts = settings.get('KAFKA_HOSTS')
        self.zookeeper_hosts=settings.get('ZOOKEEPER_HOSTS')
        self.kafka_topic = settings.get('KAFKA_TOPIC_WECHAT')
        self.reset_offset_on_start = settings.get('RESET_OFFSET_ON_START')
        logger.info('reset_offset_on_start:%d,1表示true,0表示false' % self.reset_offset_on_start)
        logger.info('kafka info, hosts:{},zookeeper_hosts:{}, topic:{}'.format(self.kafka_hosts,self.zookeeper_hosts, self.kafka_topic))
        self.kafkaClient = KafkaClient(hosts=self.kafka_hosts,zookeeper_hosts=self.zookeeper_hosts, broker_version='0.10.1.0')

    #从数据库中找出biz，并把biz传送给kafka
    def getAllAccountFromMySQL(self,col):
        bizList=[]
        sql="select {} from {}".format(col,self.table_name)
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                # print("row")
                # print(row)
                curId = row[0]
                # click_rank=row[1]
                bizList.append(curId)
        except Exception as e:
            bizList = []
            raise e
        cursor.close()

        return bizList


    def close(self):
        try:
            self.conn.close()
        except:
            print('close connection error')


    def bizsToKafka(self,biz_list):
        #根据按键精灵的点击顺序，对biz_list进行排序，这样可以保证先打开的微信公众号先发送给kafka进行处理

        topics = self.kafkaClient.topics
        # print(topics)
        topic = topics[self.kafka_topic]
        logger.info(topic)
        written_msgs = 0
        # one_biz_dict={}
        with topic.get_producer() as producer:
            for onebiz in biz_list:
                content='{"__biz":'+'"'+str(onebiz)+'"}'+'\n'
                # one_biz_dict["__biz"]=str(onebiz)
                producer.produce(bytes(content, encoding='utf-8'))
                written_msgs += 1
            if written_msgs  == 172:
              logger.info("written_msgs: %d" % written_msgs)
        logger.info("written_msgs: %d" % written_msgs)


    def get_match(self,data):
        #data是一个文件中的全部数据，for line in data :对每一行进行分析，这一行符合条件即存储到redis中
        param_dict={}
        reg_str=''r"Request url: mp.weixin.qq.com/mp/getappmsgext(.+)"''
        for i in range(len(data)):
             reg_match = re.findall(reg_str, data[i])
             if reg_match:
                 url=reg_match[0][1:]
                 headers=''.join(data[i+3:i+15])
                 body=data[i+15][14:]
                 print(body)

                 paramlist=body.split("&")
                 for one in paramlist:
                    #获取第一个=的位置
                    index=one.index('=')
                    key=one[:index]
                    value=one[index+1:]
                    # print(key,':',value)
                    param_dict[key]=value
                 sn= param_dict.get("sn","")
                 # print(headers)
                 print(body)
                 self.red.hmset(self.redis_wechat_numParams,{sn:body})  #一篇文章一个body，如何定位一篇文章
                 logger.info("发送一个参数成功")




    def change_txt(self):
        print('开始change_txt')
        f=open(filePath+'Sessions.txt','r',encoding='gbk',errors='ignore')
        data=f.readlines()
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
        os.remove(filePath+'Sessions.txt')



    def get_key(self):
        #第一步要先检查文件夹中是否含有指定文件，如果没有则不执行脚本
        session_fname='Sessions.txt'
        try:
            # files=os.listdir(filePath)
            # if session_fname in files:
            #     self.change_txt()
                f=open(filePath+'New_Sessions.txt','r',encoding='utf-8',errors='ignore')
                data=f.readlines()
                # print(data)
                self.get_match(data)
                #文件中数据已经处理，则把文件删除，删除该路径下的所有文件
                f.close()
                # os.remove(filePath+'New_Sessions.txt')

        except Exception as e:
            logger.warning('wechatParamToRedis Error :{}'.format(str(e)))

    def start_process(self,name):
        handle = win32process.CreateProcess(name, '', None, None, 0,win32process.CREATE_NO_WINDOW, None, None, win32process.STARTUPINFO()) # 创建进程获得句柄
        return handle


if __name__=="__main__":
    #该脚本每天执行一次


    print(datetime.datetime.now())
    sched = BlockingScheduler()

    wechatParams=WeChatParams()
    # #将biz_list传送给kafaka等待消费
    # biz_list=wechatParams.getAllAccountFromMySQL('biz')
    # wechatParams.close() #里面有个数据库的连接需要关闭
    # logger.info('biz_list:{}'.format(''.join(biz_list)))
    # # biz_list=['MzAxMTM3OTI4Mw==','']
    # wechatParams.bizsToKafka(biz_list)
    wechatParams.get_key()
    '''
    备注：1、按键精灵脚本中指定微信安装位置为：ADDRESS = "D:\Program Files (x86)\Tencent\WeChat\WeChat.exe"，
          当按键精灵脚本挪到别处使用，需要相同的安装位置
          2、打开微信公众号页面时，微信公众号排列为5*3
          3、
    '''
    name='D:/anjianjingling/kol/anjian2014/anjian.exe'
    # r_v = os.system(main)
    import win32process
    import win32event
    #开启按键精灵，按键精灵每30秒点一个公众号，每点3个等待1分钟，在这一分钟内，通过get_key() 向redis发送一次参数
    # handle=wechatParams.start_process(name)
    #开启定时脚本，向redis传送参数
    # time.sleep(3)
    # current_time =datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # current_time_add=(datetime.datetime.now()+datetime.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
    # sched.add_job(wechatParams.get_key,'interval', minutes=2, start_date=current_time,end_date=current_time_add)
    # sched.start()
    #
    # print(datetime.datetime.now())
    #结束进程
    # win32process.TerminateProcess(handle[0], 0)                       # 终止进程
    # win32event.WaitForSingleObject(handle[0], -1)                      # 等待进程结束


    # #每隔一天 执行抓包程序
    # sched.add_job(everyday_crawler_job, 'interval', days=1)
    # # sched.add_job(os.system(main),'interval', minutes=2,start_date='2020-02-24 9:50:00',end_date='2020-02-24 10:06:00')
    # sched.add_job(wechatParams.get_key(), 'interval', minutes=2,start_date='2020-02-24 9:51:00',end_date='2020-02-24 10:07:00')
    # #每天早上八点半和十二点半各执行一次抓包程序
    # sched.add_job(os.system(main), 'cron', hour='9', minute='30')  #这个脚本在某个时刻开始一直运行着，内部每运行15个会等待1分钟
    # # sched.add_job(wechatParams.get_key(), 'cron', hour='9', minute='31,33,35,37,39,41,43,45')  #2s，每15个大约只需要2s
    # sched.start()
