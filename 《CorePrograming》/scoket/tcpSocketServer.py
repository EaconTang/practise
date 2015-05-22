#coding=utf-8
from time import ctime
from socket import *

SOCK_TYPE_TCP = (AF_INET,SOCK_STREAM,0)       #连接类型：TCP
HOST_ADDR = ('',12582)                  #服务器地址
LISTEN_COUNT = 5                        #监听数量，允许同时连接数
BUFF_SIZE = 1024                       #缓冲区大小:1K

#初始化工作
serv_sock = socket(AF_INET,SOCK_STREAM,0)
serv_sock.bind(HOST_ADDR)
serv_sock.listen(LISTEN_COUNT)


while True:
    print 'Waiting to be connected...'

    #收到连接后返回一个客户端连接和客户地址
    cli_sock,cli_addr= serv_sock.accept()
    print 'Connected from:',cli_addr
    while True:
        #接收客户发送的数据
        data_recv = cli_sock.recv(1024)
        if not data_recv:
            print 'No data receive!Back to waiting page...'
            break

        #返回客户一个增加时间戳的数据
        cli_sock.send('[%s]:%s'%(ctime(),data_recv))
        print 'Receive data:',data_recv

    #记得关闭
    cli_sock.close()
serv_sock.close()