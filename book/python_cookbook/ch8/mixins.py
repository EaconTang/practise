class SetOnceMixin(object):
    __slots__ = ()

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key) + " is already set!")
        return super(SetOnceMixin, self).__setitem__(key, value)


class SetOnceDict(SetOnceMixin, dict):
    pass


if __name__ == '__main__':
    d = SetOnceDict()
    d['a'] = 1
    d['a'] = 2