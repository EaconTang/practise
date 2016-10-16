class A(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.ctx = []

    def __repr__(self):
        return 'A("{}", "{}")'.format(self.a, self.b)

    def __str__(self):
        return 'a: {}; b: {}'.format(self.a, self.b)

    def __format__(self, *args, **kwargs):
        pass

    def __enter__(self):
        import socket
        s = socket.socket.connect((a, b))
        self.ctx.append(s)
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ctx.pop().close()
        pass

    def __get__(self, instance, owner):
        pass

    def __getattr__(self, item):
        pass

    def __getattribute__(self, item):
        pass

    # classmethod as a construct
    @classmethod
    def now(cls):
        import time
        t = time.localtime()
        return cls(t.tm_month, t.tm_day)


if __name__ == '__main__':
    s = A('a', 'b')
    print '{}'.format(s)