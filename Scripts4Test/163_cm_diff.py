# coding=utf-8
import smtplib
import time
import sys

COUNT = int(sys.argv[1])	#投递邮件次数，在python命令执行时作为参数传入

SHARE = 'admin@eaocn.me'

HOST = 'localhost'
SENDER = SHARE
RECEIVER = SHARE
MES = '''From: From Person <admin@eaocn.me>
To: To Person <admin@eaocn.me>
Subject: No.%d

测试一下
'''
for i in range(COUNT):
        mailTest = smtplib.SMTP(HOST)
        mailTest.sendmail(SENDER,RECEIVER,MES%i)
        print 'Mail No.%d sent!'%i
        #time.sleep(1)

print 'Finish!'