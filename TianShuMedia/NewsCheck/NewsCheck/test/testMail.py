import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import pymysql
from loguru import logger

OperationalError = pymysql.OperationalError


def Mailer(to_list,mail_msg=None,subject=None,att_data_list=None):

    mail_host = 'smtp.qq.com'       # 邮箱服务器
    mail_user = '1165098845@qq.com'  # 发件人邮箱密码(当时申请smtp给的口令)
    mail_pwd = 'latkefhdoxnyiffi'   # SMTP密码
    s = smtplib.SMTP_SSL(mail_host, 465,timeout=5)
    s.login(mail_user, mail_pwd)
        #邮件内容
    mail = str(mail_msg)
    msg = MIMEMultipart()
    msgtext = MIMEText(mail.encode('utf8'), _subtype='html', _charset='utf8')
    msg['From'] = mail_user
    msg['Subject'] = subject
    msg['To'] = ",".join(to_list)
    msg.attach(msgtext)
    if att_data_list != None:
        for att_data in att_data_list:
            # open(unipath, 'rb').read()
            att = MIMEText(att_data['data'], 'base64', 'gb2312')
            att["Content-Type"] = 'application/octet-stream'
            att.add_header('Content-Disposition', 'attachment',filename=(att_data['name']+ '.csv'))
            msg.attach(att)
    try:
        s.sendmail(mail_user, to_list, msg.as_string())
        s.close()
        print('发送成功')
    except Exception as e:
        print(e)


def main():
    zyqx_data = 'pulish_date,caiji_cnt,fabu_cnt\n'
    for para in mysqlconn.fetchAll():
        zyqx_data += '{},{},{}\n'.format(para['pulish_date'], para['caiji_cnt'], para['fabu_cnt'])

    piyao_sql = '''
    SELECT a.*, b.fabu_cnt FROM
    (
    SELECT
     DATE_FORMAT(update_time, "%Y-%m-%d") as pulish_date,
     count(*) as caiji_cnt
    FROM
     platform.tmp_content_news
    WHERE
     publish_type = 2 and origin_publish_time is not NULL
    GROUP BY
     DATE_FORMAT(update_time, "%Y-%m-%d")
    ) a,
    (
    SELECT
     DATE_FORMAT(update_time, "%Y-%m-%d") as pulish_date,
     count(*) as fabu_cnt
    FROM
     platform.tmp_content_news
    WHERE
     publish_type = 2 and status=3 and origin_publish_time is not NULL
    GROUP BY
     DATE_FORMAT(update_time, "%Y-%m-%d")
    ) b
     where a.pulish_date = b.pulish_date
     '''
    mysqlconn.query(piyao_sql)
    # result = mysqlconn.fetchAll()
    piyao_data = 'pulish_date,caiji_cnt,fabu_cnt\n'
    for para in mysqlconn.fetchAll():
        piyao_data += '{},{},{}\n'.format(para['pulish_date'], para['caiji_cnt'], para['fabu_cnt'])

    # 多用户使用的list
    to_list = ['daill@8531.cn', '532909655@qq.com', 'zhjj@8531.cn', 'wangjz@8531.cn', 'shentuxm@8531.cn']
    mail_msg = '各位大佬，这是H5整体的采集量和发布量,包括：战役前线 和 辟谣栏目'
    subject = 'H5整体的采集量和发布量'

    att_data_list = [{'name':'战役前线采集量和发布量', 'data':zyqx_data},{'name': '辟谣采集量和发布量', 'data': piyao_data}]

    Mailer(to_list, mail_msg=mail_msg, subject=subject, att_data_list=att_data_list)


if __name__ == '__main__':
    main()
