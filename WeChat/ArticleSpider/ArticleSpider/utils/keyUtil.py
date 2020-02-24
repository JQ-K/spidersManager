__author__ = 'zlx'

"""
-------------------------------------------------------------------------------
Function:   using for get wechat key
-------------------------------------------------------------------------------
"""

import string,re,ftplib,time
import requests,pymysql


filePath='D:/fiddler_outfile/'

def get_match(param,data):
    reg_match=""
    if param=="key":
        reg_match=''r"window.key = params(.+)"''
    if param=="uin":
        reg_match=''r"window.uin = params(.+)"''
    for line in data:
        reg_key = re.findall(reg_match, line)
        if reg_key:
            result=reg_key[0].replace(param,"").replace("[]","").replace("|| ","").replace('"','').replace(' ','')[:-1]
            if result!="":
               return result


def get_key():
    # window.key
    change_txt()
    f=open(filePath+'New_Response.txt','r',encoding='utf-8',errors='ignore')
    data=f.readlines()
    key=get_match("key",data)
    # print(key)
    uin=get_match("uin",data)
    # print(uin)
    return key,uin


def change_txt():
    f=open(filePath+'Response.txt','r',encoding='gbk',errors='ignore')
    data=f.readlines()
    new_data=[]
    file_write_new=open(filePath+'New_Response.txt','wb')
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

if __name__=="__main__":

    key,uin=get_key()
    print(key,uin)