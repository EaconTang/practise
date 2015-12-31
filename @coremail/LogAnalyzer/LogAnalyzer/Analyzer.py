"""
generate a specific analyzer
using design pattern: Template Method Pattern and Factory Method Pattern
"""
from Inputs import Config
from Utils import *
import setting


class BaseAnalyzer(object):
    """
    main process flow as logstash:
        1. Inputs
        2. filter
        3. Outputs
    """

    def __init__(self):
        pass

    def get_input(self):
        raise NotImplementedError

    def filter(self):
        raise NotImplementedError

    def show_output(self):
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

    def show_output(self):

        pass

if __name__ == '__main__':
    analyzer = DefaultAnalyzer()
    analyzer.get_input()
    analyzer.filter()
    analyzer.show_output()
