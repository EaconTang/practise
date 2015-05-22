# coding=utf-8
import smtplib

send_address = 'tyingk@163.com'
recv_address = 'yktang@coremail.cn'
mes = '''
Subject: subject
Body Text.'''
subject = 'Subject'
smtp_host = 'localhost'

mail1 = smtplib.SMTP('localhost')
#mail1.sendmail(send_address,recv_address,mes)
print 'Finish mail1'

mail2 = smtplib.SMTP()
mail2.connect('smtp.163.com',25)
mail2.login('tyingk@163.com','')
#mail2.sendmail(send_address,recv_address,mes)    #coremail会判断出163的域名与ip不符，因而拒收
print 'Finish mail2'

mail3 = smtplib.SMTP()
mail3.connect('smtp.coremail.cn',25)
mail3.login('yktang@coremail.cn','')
mail3.sendmail('yktang@coremail.cn','',mes)   #163则没有判断
print 'Finish mail3'