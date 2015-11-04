# coding=utf-8
'''
[OCM-1364]性能测试脚本v0.2
单线程，多账号
'''
import smtplib
import time
import sys
import os

COUNT = int(sys.argv[1])  # 发送的邮件数
INTERVAL = int(sys.argv[2])  # 每隔几秒发送，等待邮件收发成功，给时间让工具检测新邮件
LOG_FILE = sys.argv[3]  # 工具生成的notify日志文件
SUBJECT = 'CheckmailTest_1102'
HOST = 'smtp.163.com'
SENDER = 'mtqatest@163.com'
SENDER_PASSWD = 'cdwysbl'

# 主要针对不同域名的帐号进行测试
RECEIVERS = ['ioswpstest123@21cn.com',
             'ios4wpstest@sina.com',
             '1537453223@qq.com',
             'ioswpstest123@163.com',
             'wpstest123@yeah.net',
             'wpstest666@outlook.com']


##########Step1: 发送邮件，记录邮件发送时间##########
# noinspection PyPep8Naming
def sendTime():
    mes_from = 'From: <%s>' % SENDER
    mes_to = 'To: <%s>' % str(RECEIVERS)
    mes_sub = 'Subject: %s' % SUBJECT
    mes = mes_from + '\n' + mes_to + '\n' + mes_sub
    time_list = []

    try:
        for i in range(COUNT):
            smtpObj = smtplib.SMTP(HOST, 25)
            smtpObj.login(SENDER, SENDER_PASSWD)
            smtpObj.sendmail(SENDER, RECEIVERS, mes + str(i))
            time_list.append(float(time.time()))
            print '邮件 %d 发送成功...' % i
            time.sleep(INTERVAL)
        print '发信完毕!'
    except Exception, e:
        print e
    finally:
        return time_list


send_time_list = sendTime()
print '【新邮件发出去的时间列表】'
send_time_list_local = map(time.ctime, send_time_list)
print send_time_list_local



##########Step2：处理指定帐号的日志时间##########
def logTime(receiver):
    USER_RESULT = receiver + '.checkimap_log'  # 保存每个帐号的notify日志
    CMD = 'grep \"has new message\" {0}|grep \"{1}\" > {2}'.format(LOG_FILE, receiver, USER_RESULT)
    os.system(CMD)

    try:
        with open(USER_RESULT) as f:
            log_list = f.readlines()
    except IOError, e:
        print e

    time_list_all = []          # 该帐号的所有notify时间记录（时间戳）
    time_list_all_local = []    # 该帐号的所有notify时间记录
    time_list = []              # 本次notify的时间列表（时间戳）
    time_list_local = []        # 本次notify的时间列表
    for each in log_list:
        str_time = each.split('[')[1].split(']')[0]
        time_list_all_local.append(str_time)
        [strTimeInt, strTimeDec] = str_time.split('.')
        time_int = time.mktime(time.strptime(strTimeInt, "%Y-%b-%d %H:%M:%S"))
        time_dec = '0.' + strTimeDec
        time_all = float(time_int) + float(time_dec)
        time_list_all.append(time_all)

    time_start = send_time_list[0]  #截取时间（通知时间至少大于本次测试第1封信发出时间）
    time_list = filter(lambda a: a > time_start, time_list_all)

    time_list_local = map(time.ctime, time_list)

    return time_list, time_list_local, time_list_all_local



##########Step3：计算时间##########
FINAL_RESULT = []
SUCCESS_LIST = []
for each in RECEIVERS:
    notify_time_list, notify_time_list_local, notifytime_all = logTime(each)
    prefix = '帐号【%s】' % each
    print prefix + '#################################################################'
    print '【所有notify时间】'
    print notifytime_all
    print '【本次测试的notify时间列表】'
    print notify_time_list_local

    # 验证notify时间列表有效性
    # 失效的可能原因包括：
    # 1）发信间隔不够大，工具检测到多封新邮件时也只发送一次通知
    # 2）邮件收发受网络影响，导致先发送的邮件后到达服务器，此时工具也会检测到多封邮件并只有一次通知
    # 3）可能有其他人往这个邮箱发送了邮件（包括垃圾邮件）
    if len(send_time_list) != len(notify_time_list):
        print prefix + '发信数目与发出通知的数目不一致！'
        if len(notify_time_list) == 0:
            print prefix + '根本检测不到新邮件！'
        continue  # 计算下一个帐号的时间

    if not all(map(lambda x, y: x < y, send_time_list, notify_time_list)):
        continue
    # if False in map(lambda x, y: x < y, send_time_list, notify_time_list):
    #     continue

    sum_send = sum(send_time_list)
    sum_notify = sum(notify_time_list)
    print '发信时间总和：' + str(sum_send)
    print '通知时间总和：' + str(sum_notify)
    avg_time = (sum_notify - sum_send) / COUNT
    result = prefix + '平均耗时（秒）：' + str(avg_time)
    print result

    FINAL_RESULT.append(result)  # 最终保存到文件的测试结果
    SUCCESS_LIST.append(each)  # 测试结果有效的帐号列表



##########保存本次结果##########
FILE_SAVE = 'final_result.txt'
try:
    with open(FILE_SAVE, 'a+') as f:
        result_log = '#########################################################################################\n'
        result_log += '【发信数】：{0}，【间隔】：{1}\n【账号数】：{2}，【有效账号数】：{3}\n'.format(
            COUNT, INTERVAL, len(RECEIVERS), len(SUCCESS_LIST))
        result_log += '【发信时间列表】：' + str(send_time_list_local) + '\n'
        result_log += '【测试帐号列表】：' + str(RECEIVERS) + '\n'
        result_log += '【有效帐号列表】：' + str(SUCCESS_LIST) + '\n'
        result_log += '【结果如下】：\n'
        result_log += '\n\n'.join(FINAL_RESULT) + '\n'
        f.write(result_log)
except IOError, e:
    print e
    sys.exit()

##########累积分析测试结果##########
