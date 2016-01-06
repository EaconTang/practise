# coding=utf-8
from SendMailMIME import SendQuick

local_MAIL = 'athena@greece.eu'
cm_MAIL = 'forqa2@coremail.cn'
qq_MAIL = 'mtqatest@qq.com'
outlook_MAIL = 'mtqatest@outlook.com'
tom_MAIL = 'mtqatest@tom.com'
netease_163 = 'mtqatest@163.com'
netease_126 = 'mtqatest@126.com'
sina_MAIL = 'mtqatest@sina.com'
_21_MAIL = 'ioswpstest123@21cn.com'

if __name__ == '__main__':
    s1 = SendQuick(cm_MAIL, 'Forqa2015')
    s1.sendSpecific(cm_MAIL, 'checkmail', 'body', 2, 0)
