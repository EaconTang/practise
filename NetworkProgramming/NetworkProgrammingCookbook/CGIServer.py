# -*- coding: utf-8 -*-
import os
import cgi
import BaseHTTPServer
import CGIHTTPServer
import cgitb
cgitb.enable()

def web_server(port):
    server = BaseHTTPServer.HTTPServer
    handler = CGIHTTPServer.CGIHTTPRequestHandler
    server_addr = ("", port)
    handler.cgi_directories = ["/cgi-bin",]
    httpd = server(server_addr, handler)
    print "Starting web server with CGI support on port: {}...".format(port)
    httpd.serve_forever()


if __name__ == '__main__':
    web_server(7777)