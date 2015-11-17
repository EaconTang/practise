# coding=utf-8
'''
all the functions you need
'''

import ConfigParser
from optparse import OptionParser
import ast
import sys


def option_parser(log, config, res_prefix, res_folder):
    '''
    give optional arguments while execute the program
    :param log: specify default (log)file to deal with
    :param config: specify default "xxx.ini" format configuration
    :param res_prefix: prefix of the filename which save the result
    :param res_folder: folder path where all the results would be saved under
    :return: a option parser
    '''
    usage = "usage: python %prog [-f value] [-c value] [-r value] [-s] [-v] [-h]"
    parser = OptionParser(usage)
    parser.add_option('-f', '--file', dest='LOG_FILE',
                      help='specify a log file, defaults to "/home/coremail/logs/rmi_api.log"',
                      default=log)
    parser.add_option('-c', '--config', dest='CONFIG_FILE',
                      help='specify a config file, defaults to "rmi_exceptions.cf"',
                      default=config)
    parser.add_option('-r', '--result', dest='RESULT_FILE',
                      help='specify the file to save the result, defaults to "{0}%Datetime%".\
                    It would be saved under the folder "{1}"'.format(res_prefix, res_folder))
    parser.add_option('-s','--save',dest='SAVE_RESULT',
                      help='use this flag not to save the results to the file',
                      action='store_true',default=False)
    parser.add_option('-v','--version',
                      help='use this flag to see program info',
                      action='store_true',default=False)
    return parser


def grep_lines(pattern, file_lines):
    '''
    simulate linux command 'grep "xxx"'
    :param pattern: 'grep' pattern in linux command(regrex and woldcard unsupported);
        this pattern could be <string> or <list>(which means multi grep)
    :param file_lines: text to be search; <list> format, each element as a line in text
    :return: all lines that match pattern, type <list>
    '''
    lines = []
    # pattern = eval(pattern)        #out of security concern
    pattern = ast.literal_eval(pattern)
    if isinstance(pattern, str):
        lines = [each_line.strip('\n') for each_line in file_lines if pattern in each_line]
    elif isinstance(pattern, list):
        lines = [each_line.strip('\n') for each_line in file_lines if all(map(lambda x: x in each_line, pattern))]
    else:
        sys.exit('Error: wrong format in config file, some values are neither list nor string?')
    return lines


def grep_lines_count(pattern, file_lines):
    '''
    simulate linux command 'grep "xxx"|wc -l'
    :param pattern: 'grep' pattern in linux command(regrex and woldcard unsupported);
        this pattern could be <string> or <list>(which means multi grep)
    :param file_lines: text to be search; <list> format, each element as a line in text
    :return: line-count of the 'grep' result, type <int>
    '''
    return len(grep_lines(pattern, file_lines))


def color_wrap(mes, color):
    '''
    return colored string
    '''
    BLUE   = '\033[0;34m'
    GREEN  = '\033[0;32m'
    RED    = '\033[0;31m'
    YELLOW = '\033[1;33m'
    ENDC   = '\033[0m'
    mes    = str(mes)
    if color == 'red':
        return RED + mes + ENDC
    elif color == 'yellow':
        return YELLOW + mes + ENDC
    elif color == 'green':
        return GREEN + mes + ENDC
    elif color == 'blue':
        return BLUE + mes + ENDC
    else:
        sys.exit('Error: unsupport color?')


def diff_result(old, new):
    pass


class MyConfigParser(ConfigParser.ConfigParser):
    '''
    overrides or add some methods
    '''

    def optionxform(self, optionstr):
        '''
        overrides method optionsxform(), make options case-sensitive
        use "SafeConfigParser().optionxform = str" is also fine
        '''
        return optionstr

    def getstring(self, section, option, raw=False, vars=None):
        '''define method getstring(), strip the '"' if the value contains double quote'''
        value = self.get(section, option)
        return value.lstrip('"').rstrip('"')

    def getlist(self, section, option, raw=False, vars=None):
        string_list = eval(self.get(section, option))
        assert isinstance(string_list, list) is True
        res_list = [each.lsplit('"').split('"') for each in string_list]
        return res_list


if __name__ == '__main__':
    pattern = str('"ab"')
    file_lines = ['abc', 'taest', 'ab', 'a', 'b', 'ba', 'ababababab']
    print grep_lines(pattern, file_lines)
