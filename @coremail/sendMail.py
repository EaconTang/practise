# coding=utf-8
import smtplib
import time
import sys
from SendMailMIME import Mail


COUNT = 2   #int(sys.argv[1])	#投递邮件次数
#SUBJECT = 'Test'  #sys.argv[2]		#邮件主题
#SHARE = 'test@eacon.cn'		#发送人接收人共用的邮件用户
HOST = 'localhost'
SENDER = 'qctest@dm109.icoremail.net'
RECEIVER = 'mtqatest@163.com'
MES = '''From: qctest <qctest@dm109.icoremail.net>
To: mtqatest <mtqatest@163.com>
Subject: TEST'''

mailObj = smtplib.SMTP(HOST)
mailObj.login('qctest@dm109.icoremail.net','123')

time.

for i in range(COUNT):
    #SUBJECT = 'Test' + str(i)
    mailObj.sendmail(SENDER,RECEIVER,MES+str(i))	
    print 'Mail No.%d sent!'%i
        #time.sleep(1)


print 'Finish!'