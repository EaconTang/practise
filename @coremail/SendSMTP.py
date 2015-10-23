# coding=utf-8
import smtplib
import time
import sys
from SendMailMIME import Mail

COUNT = 100   #int(sys.argv[1])
SUBJECT = 'Test'  #sys.argv[2]
HOST = '192.168.200.209'
SENDER = 'jesus@eacon.cn'
SENDER_PASSWD = '123'
RECEIVER = ['athena@eacon.cn']

mes_from = 'From: <%s>'%SENDER
mes_to = 'To: <%s>'%str(RECEIVER)
mes_sub = 'Subject: %s'%SUBJECT
MES = mes_from + '\n' + mes_to + '\n' + mes_sub

#multi receiver
MES_list = []
for i in range(len(RECEIVER)):
    mes = mes_from + '\n' + 'To: <%s>'%RECEIVER[i] + '\n' + mes_sub
    MES_list.append(mes)

try:
    for i in range(COUNT):
        mailObj = smtplib.SMTP(HOST,25)
        mailObj.login(SENDER,SENDER_PASSWD)     # comment this line to send without login
        #mailObj.sendmail(SENDER,RECEIVER,MES+str(i))
        for j in range(len(RECEIVER)):
            mailObj.sendmail(SENDER,RECEIVER[j],MES_list[j]+str(i))
        print 'Mail No.%d sent!'%i
except Exception,e:
    print e

print 'Finish!'