#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import os
import sys
import urllib2
from multiprocessing import Pool


COUNT = int(sys.argv[1])    #单进程请求次数
THREAD = int(sys.argv[2])   #进程数

#测试帐号列表
emailList = ['mtqatest@163.com','mtqatest@qq.com','wpstest123@hotmail.com','wpsmailtest@kingsoft.com']


def getDeviceId(count):
    pidOutput = ''          
    for i in range(count):
        email = emailList[(i%(len(emailList)))]
        res = urllib2.urlopen('https://223.252.214.184/maweb/api/account/getDeviceId?email=%s'%email)
        resOutput = '【'+str(res.getcode())+'】' + res.read() + '['+email+']'
        #print resOutput
        pidOutput += resOutput + '\n'
    
    filename = str(os.getpid()) + '.pid'       #保存每个进程的输出结果到文件，文件名为进程名.pid
    with open(filename,'w+') as f:
        f.write(pidOutput)

    print '子进程:',os.getpid(),'完成！'


timeStart = time.time()

print '父进程 %s.' % os.getpid()
p = Pool(THREAD)
for i in range(THREAD):
    p.apply_async(getDeviceId, args=(COUNT,))
print '并发所有子进程中...'
#p.close()
p.join()
print '并发完成！'

timeEnd = time.time()

print '【总共耗时（秒）：',str(timeEnd-timeStart),'】',time.ctime(timeStart),' ~ ',time.ctime(timeEnd)

#汇总所有线程输出文件
with open('FinalResult.txt','a+') as f:
    allFile = os.listdir(os.getcwd())
    text = ''
    for each in allFile:
        if each.endswith('.pid'):
            f_each = open(each,'r+')
            text += f_each.read()
            f_each.close()
    f.write(text)

print '所有输出已保存到文件：[FinalResult.txt]'

