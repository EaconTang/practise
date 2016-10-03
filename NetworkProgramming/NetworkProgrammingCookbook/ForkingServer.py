# -*- coding: utf-8 -*-
import os
import socket
import threading
import SocketServer


SERVER_HOST = "localhost"
SERVER_PORT = 0
BUF_SIZE = 1024
ECHO_MSG = "Hello echo server!"


class ForkingClient(object):
    """A client to test forking server"""
    def __init__(self, ip ,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def run(self):
        current_process_id = os.getpid()
        print "(Client)[PID:{}]Sending echo message to the server: {}".format(current_process_id, ECHO_MSG)
        sent_data_length = self.sock.send(ECHO_MSG)
        print "(Client)[PID:{}]Sent: {} characters so for...".format(current_process_id, sent_data_length)

        response = self.sock.recv(BUF_SIZE)
        print "(Client)[PID:{}]Received: {}".format(current_process_id, response[5:])

    def shutdown(self):
        self.sock.close()


class ForkingServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        current_process_id = os.getpid()
        response = "{}: {}".format(current_process_id, data)
        print "(Server)Sending response [pid: data]: [{}]".format(response)
        self.request.send(response)
        return


class ForkingServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    pass


def main():
    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    print "(Server)[PID:{}]Loop running...".format(os.getpid())

    client_a = ForkingClient(ip, port)
    client_a.run()
    client_b = ForkingClient(ip, port)
    client_b.run()

    server.shutdown()
    client_a.shutdown()
    client_b.shutdown()
    server.socket.close()


if __name__ == '__main__':
    main()