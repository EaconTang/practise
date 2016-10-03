# -*- coding: utf-8 -*-
import socket
import sys
import argparse


host = "localhost"
data_payload = 2048
backlog = 5

def echo_server(port):
    """
    A simple echo server
    :param port:
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind((host, port))
    s.listen(backlog)
    while True:
        print "serving on {}:{}...".format(host, port)
        conn, addr = s.accept()
        data = conn.recv(data_payload)
        if data:
            print "received[from {}]: {}".format(addr, data)
            conn.send(data)
            print "sent back success"
        else:
            print "nothing received from {}:{}".format(*addr)
        conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    # port = parser.parse_args().port
    echo_server(6668)