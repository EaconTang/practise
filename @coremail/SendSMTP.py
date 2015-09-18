#coding=utf-8
from SendMailMIME import SendSMTP,Mail

s1 = SendSMTP('mtqatest@126.com','mailtech')
#s1.sendDefault('mtqatest@163.com',10,10)
s1.sendSpecific('mtqatest@163.com','诸葛村夫','sanguo',2,10)

# s2 = Mail('smtp.126.com',25,'mtqatest@126.com','mailtech')
# s2.setSender('mtqatest@126.com')
# s2.setReceiver('mtqatest@163.com')
# s2.sendMultipart()

