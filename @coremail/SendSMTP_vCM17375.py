import smtplib

COUNT = 1000
SUBJECT = 'Test CM17375'
HOST = 'localhost'
SENDER = 'athena@eacon.cn'
SENDER_PASSWD = '123'
RECEIVER = 'jupiter@eacon.cn'

mes_from = 'From: <%s>'%SENDER
mes_to = 'To: <%s>'%RECEIVER
mes_sub = 'Subject: %s'%SUBJECT
mes_body = 'Test da read context!'
MES = mes_from + '\n' + mes_to + '\n' + mes_sub + '\n\n' + mes_body

try:
    for i in range(COUNT):
        mailObj = smtplib.SMTP(HOST,25)
        mailObj.login(SENDER,SENDER_PASSWD)     # comment this line to send without login
        mailObj.sendmail(SENDER,RECEIVER,MES)
        print 'Mail %4d sent!'%i
except Exception,e:
    print e

print 'Finish!'