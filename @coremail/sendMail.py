#coding=utf-8
from SendMailMIME import SendQuick,Mail

local_MAIL = 'athena@greece.eu'
cm_MAIL = 'forqa4@coremail.cn'
qq_MAIL = 'mtqatest@qq.com'
outlook_MAIL = 'mtqatest@outlook.com'

s1 = SendQuick(qq_MAIL,'cdwysbl')
#s1.sendDefault('mtqatest@163.com',10,10)
s1.sendSpecific(cm_MAIL,'诸葛村夫','sanguo',10,0.1)


# s2 = Mail('smtp.126.com',25,'mtqatest@126.com','mailtech')
# s2.setSender('mtqatest@126.com')
# s2.setReceiver('mtqatest@163.com')
# s2.sendMultipart()

