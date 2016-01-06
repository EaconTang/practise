import unittest
from SendMailMIME import SendQuick


class TestSendmail(unittest.TestCase):
    def test_sendmailMIME(self):
        """
        """
        cm_MAIL = 'forqa2@coremail.cn'
        qq_MAIL = 'mtqatest@qq.com'
        outlook_MAIL = 'mtqatest@outlook.com'
        tom_MAIL = 'mtqatest@tom.com'
        netease_163 = 'mtqatest@163.com'
        netease_126 = 'mtqatest@126.com'
        sina_MAIL = 'mtqatest@sina.com'
        _21_MAIL = 'ioswpstest123@21cn.com'
        s = SendQuick(cm_MAIL, 'Forqa2015')
        s.sendSpecific(cm_MAIL, 'checkmail', 'body', 2, 0)


if __name__ == '__main__':
    pass
