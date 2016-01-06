# coding=utf-8
import smtplib
import time
import sys
from SendMailMIME import Mail


def sendTime():
    time_list = []
    try:
        for i in range(COUNT):
            mailObj = smtplib.SMTP(HOST, 25)
            mailObj.login(SENDER, SENDER_PASSWD)  # comment this line to send without login
            # mailObj.sendmail(SENDER,RECEIVER,MES+str(i))
            mailObj.connect()
            for j in range(len(RECEIVER)):
                mailObj.sendmail(SENDER, RECEIVER[j], MES_list[j] + str(i))
                time_list.append(time.time())
            print 'Mail No.%d sent!' % i
            time.sleep(1)
    except Exception, e:
        print e
        sys.exit()
    finally:
        mailObj.quit()
        return time_list

if __name__ == '__main__':
    COUNT = 10  # int(sys.argv[1])
    SUBJECT = 'CM23600'  # sys.argv[2]
    HOST = 'smtp.sina.com'
    SENDER = 'mtqatest@sina.com'
    SENDER_PASSWD = 'cdwysbl'
    RECEIVER = ['mtqatest@163.com', 'mtqatest@outlook.com',
                'mtqatest@qq.com', 'mtqatest2@live.com']

    mes_from = 'From: <%s>' % SENDER
    mes_to = 'To: <%s>' % str(RECEIVER)
    mes_sub = 'Subject: %s' % SUBJECT
    MES = mes_from + '\n' + mes_to + '\n' + mes_sub

    # multi receiver
    MES_list = []
    for i in range(len(RECEIVER)):
        mes = mes_from + '\n' + 'To: <%s>' % RECEIVER[i] + '\n' + mes_sub
        MES_list.append(mes)

    timeCost = sendTime()
    print timeCost

    print 'Finish!'
