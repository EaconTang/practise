# -*- coding: utf-8 -*-
import os
import socket
import threading
import SocketServer

SERVER_HOST = "localhost"
SERVER_PORT = 0
BUF_SIZE = 1024

def client(ip, port, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    try:
        s.sendall(message)
        response = s.recv(BUF_SIZE)
        print "(Client) Received: {}".format(response)
    finally:
        s.close()


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        current_thread = threading.current_thread()
        response = "{}: {}".format(current_thread.name, data)
        self.request.sendall(response)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == '__main__':
    server = ThreadedTCPServer((SERVER_HOST, SERVER_PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server.daemon = True
    server_thread.start()
    print "(Server) Loop running on thread: {}".format(server_thread.name)

    client(ip, port, "message from client_A...")
    client(ip, port, "message from client_B...")
    client(ip, port, "message from client_C...")

    server.shutdown()