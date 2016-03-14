# coding=utf-8
import smtplib
import time
from email.mime.text import MIMEText


class SendQuick:
    '''快速发送邮件'''

    def __init__(self, user, psw, host='localhost', port=25):
        self.user = user
        self.psw = psw
        mp = MailParser(user)
        self.host, self.port = mp.getServer()

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
        splited = str(self.username).split('@')
        suffix = splited[1]
        common_list = ['qq.com', '163.com', '126.com', 'sina.com', '139.com', 'coremail.cn']
        outlook_list = ['outlook.com', 'hotmail.com', 'live.com', 'live.cn']
        if suffix in common_list:
            return ('smtp.' + suffix, 25)
        elif suffix in outlook_list:
            return ('smtp-mail.outlook.com', 25)
        elif suffix == 'yahoo.com':
            return ('smtp.mail.yahoo.com', 25)
        else:
            return ('localhost', 25)


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

            try:
                s = smtplib.SMTP()
                s.connect(self.host, self.port)
                s.login(self.username, self.password)
                s.sendmail(self.sender, self.receiver, self.msg.as_string())
            except Exception, e:
                print "Send failed!",
                print e
            finally:
                s.quit()

            print '**********Mail ' + str(i) + ' Finish!**********'
            if i != count - 1:
                print 'sleeping...'
                time.sleep(self.interval)

    def sendMultipart(self):
        # todo
        pass


if __name__ == '__main__':
    pass
