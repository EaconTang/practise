import time
import socket

def test(host, port, timeout):
    while 1:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, int(port)))
        # sock.settimeout(timeout)

        msg = """GET / HTTP1.1 \r\n"""
        sock.send(msg)
        print 'message sent!'
        print time.clock()
        time.sleep(5)
        #
        # recv_value = sock.recv(2048)
        # print 'received: ', str(recv_value)


if __name__ == '__main__':
    test('127.0.0.1', '5993', 60)
