"""
generate a specific analyzer
using design pattern: Template Method Pattern and Factory Method Pattern
"""
import Config


class Analyzer(object):
    """
    main process flow as logstash:
        1. Input
        2. filter
        3. Output
    """

    def __init__(self, optargs):
        """
        :param optargs: args define by user in command mode
        """
        self.optargs = optargs

    def get_input(self):
        raise NotImplementedError

    def filter(self):
        raise NotImplementedError

    def output(self):
        raise NotImplementedError

    def assist(self):
        pass


class


if __name__ == '__main__':
    pass
