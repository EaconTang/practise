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

s1 = SendQuick('mtqatest@sina.com','cdwysbl')
s1.sendSpecific('mtqatest@qq.com','23600','body',10,10)


