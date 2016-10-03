# coding=utf-8
from socket import *

SOCK_TYPE_TCP = (AF_INET, SOCK_STREAM, 0)
HOST_ADDR = ('localhost', 12582)
BUFF_SIZE = 1024

# 初始化
cli_sock = socket(AF_INET, SOCK_STREAM, 0)
cli_sock.connect(HOST_ADDR)

while True:
    data_send = raw_input('Input Data To Send:#')
    if not data_send:
        print 'No data input!Back to input...'
        continue
    cli_sock.send(data_send)
    data_recv = cli_sock.recv(BUFF_SIZE)
    if not data_recv:
        print 'Server Error! No data back...'
        continue
    print 'Data received:', data_recv
