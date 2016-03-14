# coding:utf-8
__author__ = 'the5fire'
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from os import path


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(self.render('admin'))
        self.wfile.write('\n')
        return

    def render(self, name='index'):
        file_name = '%s.html' % name
        if path.isfile(file_name):
            html = open(file_name, 'r').read()
            return html
        return None


class HandlerA(Handler):
    def do_GET(self, url):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(self.render(url))
        self.wfile.write('\n')
        return

    def render(self, name='index'):
        file_name = '%s.html'%name
        if path.isfile(file_name):
            with open(file_name) as f:
                return f.read()
        return None


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8181), Handler)
    print 'Development server is running at http://127.0.0.1:8181/'
    print 'Starting server...'
    server.serve_forever()
