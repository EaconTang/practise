#coding=utf-8
from SendMailMIME import SendQuick,Mail

local_MAIL = 'athena@greece.eu'
cm_MAIL = 'forqa4@coremail.cn'
qq_MAIL = 'mtqatest2@qq.com'
outlook_MAIL = 'mtqatest@outlook.com'
tom_MAIL = 'mtqatest@tom.com'
netease_163 = 'mtqatest@163.com'
netease_126 = 'mtqatest@126.com'
sina_MAIL = 'ios4wpstest@sina.com'
_21_MAIL = 'ioswpstest123@21cn.com'


s1 = SendQuick(cm_MAIL,'forqa2015')
#s1.sendDefault('mtqatest@163.com',10,10)
s1.sendSpecific('ios4wpstest@sina.com','checkmail','body',2,10)


# s2 = Mail('smtp.126.com',25,'mtqatest@126.com','mailtech')
# s2.setSender('mtqatest@126.com')
# s2.setReceiver('mtqatest@163.com')
# s2.sendMultipart()

