# coding=utf-8
import smtplib

HOST = 'localhost'
SENDER = 'send@test.cn'
RECEIVER = 'admin@eacon.me'
MES = '''From: From Person <send@tyk.cn>
To: To Person <admin@eacon.me>
Subject: 测试发送1000次邮件

Body Text.
'''

mailTest = smtplib.SMTP(HOST)
mailTest.connect('smtp.eacon.me', 25)
mailTest.login('admin@eacon.me', '123')
mailTest.sendmail(SENDER, RECEIVER, MES)
print 'Finish!'
