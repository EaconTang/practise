"""
generate a specific analyzer
using design pattern: Template Method Pattern and Factory Method Pattern
"""
from Input import Config
from Util import *
import setting


class BaseAnalyzer(object):
    """
    main process flow as logstash:
        1. Input
        2. filter
        3. Output
    """

    def __init__(self):
        pass

    def get_input(self):
        raise NotImplementedError

    def filter(self):
        raise NotImplementedError

    def output(self):
        raise NotImplementedError

    def assist(self):
        pass


class DefaultAnalyzer(BaseAnalyzer):
    def get_input(self):
        cf = Config()
        var_dict = cf.parse_command_args()
        cf.read_conf_file(var_dict['cf'])

    def filter(self):

        pass

if __name__ == '__main__':
    analyzer = DefaultAnalyzer()
    analyzer.get_input()
    analyzer.filter()
    analyzer.output()
