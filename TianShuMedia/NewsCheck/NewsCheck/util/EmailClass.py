# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
import time

from loguru import logger


class EmailClass(object):
    def __init__(self):
        self.curDateTime = str(time.strftime('%Y-%m-%d', time.localtime()))  # 当前日期时间
        self.sender = 'daill@8531.cn'
        self.password = 'dailili1990'
        self.receivers = ['zhjj@8531.cn', 'ywwei@8531.cn', 'dcy@8531.cn', 'daill@8531.cn']
        #self.receivers = ['zhjj@8531.cn', 'daill@8531.cn']
        self.msg_title = '快手号-浙江日报数据-'
        self.sender_server = 'smtp.8531.cn'
        self.From = '戴莉莉'
        self.To = '融媒体数据中心-数据统计'

    '''
    配置邮件内容
    '''
    #@property
    def setMailContent(self, filepath):
        msg = MIMEMultipart()
        msg['From'] = Header(self.From,'utf-8')
        msg['To'] = self.To
        msg['Subject'] = Header('%s%s'%(self.msg_title,self.curDateTime),'utf-8')
        #附件
        att1 = MIMEText(open(filepath, 'rb').read(), 'base64', 'utf-8')
        fileName = filepath.split('/')[-1]
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="{}"'.format(fileName)
        msg.attach(att1)
        return msg


    '''
    发送电子邮件
    '''
    def sendEmail(self,message):
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.sender_server, 25)
            #smtpObj.connect(self.sender_server, 465)
            smtpObj.login(self.sender,self.password)
            smtpObj.sendmail(self.sender,self.receivers , message.as_string())
            smtpObj.quit()
            logger.info("邮件发送成功")
        except smtplib.SMTPException as ex:
            logger.info("Error: 无法发送邮件.%s"%ex)

    #发送调用
    #@property
    def send(self, filepath):
        self.sendEmail(self.setMailContent(filepath))

if __name__=="__main__":
    filepath = '/Users/macbookpro/PycharmProjects/spidersManager/TianShuMedia/NewsCheck/2020-01-28.txt'
    email = EmailClass()
    email.send(filepath)
