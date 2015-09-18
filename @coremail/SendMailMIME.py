# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from email.Utils import formatdate
import sys


class SendSMTP:
    '''快速发送邮件'''

    def __init__(self, user, psw, host='localhost', port=25):
        self.user = user
        self.psw = psw
        mp = MailParser(user)
        (self.host, self.port) = mp.getServer()

    def sendDefault(self, receiver, count=2, interval=10):
        '''发送默认邮件，只需要指定接收邮箱'''
        self.sendSpecific(receiver, '我是主题', '我是正文', count, interval)

    def sendSpecific(self, receiver, subject, body, count, interval):
        self.receiver = receiver
        self.subject = subject
        self.body = body
        self.count = count
        self.interval = interval

        m = Mail(self.host, self.port, self.user, self.psw)
        m.setSubject(self.subject)
        m.setBody(self.body)
        m.setSender(self.user)
        m.setReceiver(self.receiver)
        m.setCount(self.count)
        m.setInterval(self.interval)
        m.send()


class MailParser:
    '''统一处理各个邮件域名的smtp服务器地址等信息'''

    def __init__(self, username):
        self.username = username

    def getServer(self):
        try:
            splited = str(self.username).split('@')
            suffix = splited[1]
            if suffix == 'qq.com':
                return ('smtp.qq.com', 25)
            elif suffix == '163.com':
                return ('smtp.163.com', 25)
            elif suffix == '126.com':
                return ('smtp.126.com', 25)
            elif suffix == 'sina.com':
                return ('smtp.sina.com', 25)
            elif suffix == '139.com':
                return ('smtp.139.com', 25)
            elif suffix == 'yahoo.com':
                return ('smtp.mail.yahoo.com', 25)
            elif suffix == 'outlook.com':
                return ('smtp-mail.outlook.com', 25)
            elif suffix == 'hotmail.com':
                return ('smtp.live.com', 25)
            elif suffix == 'coremail.cn':
                return ('smtp.coremail.cn', 25)
            # else:
            #     raise UnsupportMail('UnsupportMail:' + self.username)
#         except UnsupportMail, e:
#             print e.args
#         except BaseException, e:
#             print e
#
#
# class UnsupportMail(RuntimeError):
#     def __init__(self, args):
#         self.args = ''.join(args)


class Mail:
    '''封装邮件发送常用操作的自定义API'''

    def __init__(self, host, port, username, password):
        self.setServer(host, port)
        self.username = username
        self.password = password

    def setServer(self, host, port):
        self.host = host
        self.port = port
        self.server = (self.host, self.port)

    def login(self, username, password):
        self.username = username
        self.password = password

    def setSender(self, sender):
        self.sender = sender

    def setReceiver(self, toList):
        self.receiver = toList

    def setSubject(self, subject='TEST'):
        self.subject = subject

    def setBody(self, body=''):
        try:
            with open(body, 'rb') as fp:
                # self.body = MIMEText(fp.read())
                self.body = fp.read()
        except:
            self.body = body

    def setAttach(self, attchFile):
        try:
            with open(attchFile, 'rb') as f:
                self.attch = MIMEText(f.read())
        except:
            self.attch = attchFile

    def setCount(self, count):
        self.count = count

    # return a specific format time
    def splitTime(self, ctime):
        self.time = []
        self.time = ctime.split(" ")
        return self.time[3]

    def setInterval(self, interval):
        self.interval = interval

    def send(self):
        count = self.count
        for i in range(count):
            # self.msg = MIMEMultipart()
            self.msg = MIMEText(self.body, 'plain', "utf-8")
            # self.msg['Body'] = self.body
            self.msg['From'] = self.sender
            self.msg['To'] = self.receiver
            self.msg['Subject'] = '[' + self.splitTime(time.ctime()) + ']' + self.subject + '(' + str(i) + ')'
            self.msg['Accept-Language'] = "zh-CN"
            self.msg['Accept-Charset'] = "ISO-8859-1,utf-8"

            print '**********To Send:**********'
            print self.msg.as_string()
            # s = smtplib.SMTP(self.server)
            s = smtplib.SMTP()
            s.connect(self.host, self.port)
            s.login(self.username, self.password)
            s.sendmail(self.sender, self.receiver, self.msg.as_string())
            s.quit()
            print '**********Mail ' + str(i) + ' Finish!**********'

            print 'sleeping...'
            time.sleep(self.interval)

    def sendMultipart(self):
        # todo
        pass


if __name__ == '__main__':
    pass
