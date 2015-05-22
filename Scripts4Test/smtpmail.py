# coding=utf-8
import smtplib

send_address = 'send@tyk.cn'
recv_address = 'recv@tyk.cn'
mes = '''From: From Person <send@tyk.cn>
To: To Person <recv@tyk.cn>
Subject: Test

Body Text.
'''
subject = 'Subject'
smtp_host = 'localhost'

mail1 = smtplib.SMTP(smtp_host)
mail1.sendmail(send_address,recv_address,mes)
print 'Finish!'

