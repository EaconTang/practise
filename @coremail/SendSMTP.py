# coding=utf-8
import smtplib
import time
import sys
from SendMailMIME import Mail

COUNT = 10   #int(sys.argv[1])
SUBJECT = 'CheckmailTest'  #sys.argv[2]
HOST = 'smtp.coremail.cn'
SENDER = 'forqa3@coremail.cn'
SENDER_PASSWD = 'forqa2015'
RECEIVER = ['ioswpstest123@163.com','autotest0123@163.com',
             'ioswpstest123@126.com','autotest0123@126.com',
             'wpstest123@yeah.net','wang_qian1111@163.com',
             'mtqatest@sina.com','ceshizu123456@sina.com',
             'ios8wpstest@sina.com','ios4wpstest@sina.com',
             'bjwpstest123@hotmail.com','wpstest666@outlook.com',
             'ioswpstest123@21cn.com','ioswpstest123@tom.com',
              'wpstest1234@yahoo.com','ioswpstest123@foxmail.com',
             '920330270@qq.com','1537453223@qq.com']


mes_from = 'From: <%s>'%SENDER
mes_to = 'To: <%s>'%str(RECEIVER)
mes_sub = 'Subject: %s'%SUBJECT
MES = mes_from + '\n' + mes_to + '\n' + mes_sub

#multi receiver
MES_list = []
for i in range(len(RECEIVER)):
    mes = mes_from + '\n' + 'To: <%s>'%RECEIVER[i] + '\n' + mes_sub
    MES_list.append(mes)

def sendTime():
    time_list = []
    try:
        for i in range(COUNT):
            mailObj = smtplib.SMTP(HOST,25)
            mailObj.login(SENDER,SENDER_PASSWD)     # comment this line to send without login
            #mailObj.sendmail(SENDER,RECEIVER,MES+str(i))
            for j in range(len(RECEIVER)):
                mailObj.sendmail(SENDER,RECEIVER[j],MES_list[j]+str(i))
                time_list.append(time.time())
            print 'Mail No.%d sent!'%i
            time.sleep(10)
    except Exception,e:
        print e
        sys.exit()
    finally:
        mailObj.quit()
        return time_list

timeCost = sendTime()
print timeCost

print 'Finish!'