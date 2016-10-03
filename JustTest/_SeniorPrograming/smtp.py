#!/usr/bin/python

sender = 'send@eacon.cn'
receivers = ['admin@eacon.cn]'
             message = '''From:tyk<send@eacon.cn>
To:admin<admin@eacon.cn>
Subject:Scripts4Test

This is a Scripts4Test.
'''

smtp1 = smtplib.SMTP('localhost')
smtp1.sendmail(sender, receivers, message)
print 'success!'
