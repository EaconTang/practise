# -*- coding: utf-8 -*-
import socket
import sys

BUF_RECV = 20480


def echo_client(host, port):
    """
    Simple echo client
    :param host:
    :param port:
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        while True:
            msg = str(raw_input("Input the message to be sent: "))
            s.sendall(msg)
            data = s.recv(BUF_RECV)
            print "received: {}".format(data)
    except KeyboardInterrupt as k_err:
        print k_err
        sys.exit("Quit from keyboard interrupt...")
    finally:
        s.close()


if __name__ == '__main__':
    echo_client("localhost", 6667)
