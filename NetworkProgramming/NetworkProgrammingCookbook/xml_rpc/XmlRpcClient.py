# -*- coding: utf-8 -*-
import xmlrpclib

def run_client(host, port, username, passowrd):
    server = xmlrpclib.ServerProxy("http://{}:{}@{}:{}".format(username, passowrd, host, port))
    msg = "hello server..."
    print "sending msg to server: {}".format(msg)
    print "Got reply: {}".format(server.echo(msg))


if __name__ == '__main__':
    run_client()