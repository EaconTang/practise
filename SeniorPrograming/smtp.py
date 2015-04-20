#!/usr/bin/python
import smtplib

sender = 'send@eacon.cn'
receivers = ['admin@eacon.cn]'
message = '''From:tyk<send@eacon.cn>
To:admin<admin@eacon.cn>
Subject:test

This is a test.
'''

smtp1 = smtplib.SMTP('localhost')
smtp1.sendmail(sender,receivers,message)
print 'success!'
