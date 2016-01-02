"""
generate a specific analyzer
using design pattern: Template Method Pattern
"""
from Inputs import Inputs
from Filters import Filters
from Outputs import Outputs
from Utils import *
import settings


class BaseAnalyzer(object):
    """
    main process flow as logstash:
        1. Inputs
        2. Filters
        3. Outputs
    """
    def __init__(self):
        pass

    def do_input(self):
        raise NotImplementedError

    def do_filter(self):
        raise NotImplementedError

    def do_output(self):
        raise NotImplementedError

    def assist(self):
        pass


class DefaultAnalyzer(BaseAnalyzer):
    def do_input(self):
        inputs = Inputs()
        return inputs.process()

    def do_filter(self, inputs_res):
        filters = Filters(inputs_res)
        return filters.process()

    def do_output(self, filters_res):
        outputs = Outputs(filters_res)
        outputs.process()


if __name__ == '__main__':
    analyzer = DefaultAnalyzer()

    in_res = analyzer.do_input()
    print in_res

    filter_res = analyzer.do_filter(in_res)
    print filter_res

    # analyzer.do_output(filter_res)
