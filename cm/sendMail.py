# coding=utf-8
import smtplib
import sys

COUNT = int(sys.argv[1])  # 投递邮件次数
SUBJECT = sys.argv[2]  # 邮件主题
SHARE = 'test@eacon.cn'  # 发送人接收人共用的邮件用户
HOST = 'localhost'
SENDER = 'admin@eacon.cn'
RECEIVER = SHARE
MES = '''From: Sender <test@eacon.cn>
To: Receiver <test@eacon.cn>
Subject: %s + %d

''' % SUBJECT

mailObj = smtplib.SMTP(HOST)
mailObj.login('admin@eacon.cn', '123')

for i in range(COUNT):
    mailObj.sendmail(SENDER, RECEIVER, MES + (str)
    i)
    print 'Mail No.%d sent!' % i
    # time.sleep(1)

mailObj.close

print 'Finish!'
