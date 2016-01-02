"""
Outputs:
    1.
"""

class BaseOutputs(object):
    def __init__(self):
        self._vars = {}

    def to_table(self):
        raise NotImplementedError

    def to_file(self):
        raise NotImplementedError

    def to_console(self):
        raise NotImplementedError


class PrettyTableOutputs(BaseOutputs):
    def __init__(self):
        super(TableOutputs, self).__init__()

    def to_table(self):
        pass


class FileOutputs(BaseOutputs):
    def __init__(self):
        super(FileOutputs, self).__init__()

    def to_file(self):
        pass


class ConsoleOutputs(BaseOutputs):
    def __init__(self):
        super(ConsoleOutputs, self).__init__()

    def to_console(self):
        pass


class Outputs(PrettyTableOutputs, ConsoleOutputs, FileOutputs):
    def __init__(self, filters_res):
        super(Outputs, self).__init__()
        self._vars.update(filters_res)

    def process(self):
        pass


if __name__ == '__main__':
    pass