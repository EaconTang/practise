# coding=utf-8
'''
[OCM-1364]性能测试
'''
import smtplib
import time
import sys
import os

#Step1: 发送邮件，记录邮件发送时间
COUNT = int(sys.argv[1])     #发送的邮件数
INTERVAL = int(sys.argv[2])      #每隔几秒发送，等待邮件收发成功，给时间让工具检测新邮件
SUBJECT = 'CheckmailTest'
HOST = 'smtp.coremail.cn'
SENDER = 'forqa3@coremail.cn'
SENDER_PASSWD = 'forqa2015'
RECEIVER = sys.argv[3]

def sendTime():
    mes_from = 'From: <%s>'%SENDER
    mes_to = 'To: <%s>'%RECEIVER
    mes_sub = 'Subject: %s'%SUBJECT
    mes = mes_from + '\n' + mes_to + '\n' + mes_sub
    time_list = []
    try:
        for i in range(COUNT):
            mailObj = smtplib.SMTP(HOST,25)
            mailObj.login(SENDER, SENDER_PASSWD)
            mailObj.sendmail(SENDER, RECEIVER, mes + str(i))
            time_list.append(float(time.time()))
            print '邮件 %d 发送成功...'%i
            time.sleep(INTERVAL)
        print '发信完毕!'
    except Exception,e:
        print e
        sys.exit()
    finally:
        return time_list

send_time_list = sendTime()
print '【新邮件发出去的时间列表】'
print send_time_list


#Step2：处理日志时间
FILE_RESULT = RECEIVER + '.test_result'
CMD = 'grep \"has new message\"  checkimap.log|grep \"%s\" > %s' %(RECEIVER, FILE_RESULT)

def logTime():
    os.system(CMD)

    try:
        with open(FILE_RESULT) as f:
            log_list = f.readlines()
    except IOError,e:
        print e
        sys.exit()

    time_list = []
    for each in log_list:
        str_time = each.split('[')[1].split(']')[0]
        [strTimeInt,strTimeDec] = str_time.split('.')
        #print strTimeFormat
        time_int = time.mktime(time.strptime(strTimeInt,"%Y-%b-%d %H:%M:%S"))
        time_dec = '0.' + strTimeDec
        time_all = float(time_int) + float(time_dec)
        #print time_all
        time_list.append(time_all)

    for i in range(len(time_list)):
        time_start = send_time_list[0]
        if time_list[i] > time_start:        #截取有效时间（通知时间至少大于本次测试第1封信发出时间）
            time_list = time_list[i:]
            break

    print '日志时间处理完毕...'
    return time_list

notify_time_list = logTime()
print '【检测到新邮件后，发出通知的时间列表】'
print notify_time_list


#Step3：计算时间
if len(send_time_list) != len(notify_time_list):
    if len(notify_time_list) == 0:
        print '检测不到该帐号的新邮件！'
    print '发信数目与发出通知的数目不一致！'
    sys.exit()
    #可能原因：
        # 1）发信间隔不够大，工具检测到多封新邮件时也只发送一次通知
        # 2）邮件收发受网络影响，导致先发送的邮件后到达服务器，此时工具也会检测到多封邮件并只有一次通知
        # 3）可能有其他人往这个邮箱发送了邮件（包括垃圾邮件）

sum_send = sum(send_time_list)
sum_notify = sum(notify_time_list)
print '发信时间总和：' + str(sum_send)
print '通知时间总和：' + str(sum_notify)
avg_time = (sum_notify - sum_send)/COUNT
print '平均每封信，从【邮件发出-到-工具notify】耗时（秒）：' + str(avg_time)



