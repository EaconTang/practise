# coding=utf-8
'''
all the functions neededby log_miner.py
'''

import ConfigParser
import ast
import sys
from optparse import OptionParser

import prettytable


def option_parser():
    '''
    give optional arguments while execute the program
    :return: a option parser
    '''
    usage = "usage: python %prog [-f value] [-c value] [-t] [--tabulate-file value] [-o] [--omit-file value]"
    parser = OptionParser(usage)
    parser.add_option('-f', '--file', dest='FILE',
                      help='specify a log file to be scan, defaults to yesterday\'s rmi_api.log')
    parser.add_option('-c', '--config', dest='CONFIG',
                      help='specify a config file to be load,defaults to ~/LogMiner/conf/rmi_exceptions.cf')
    parser.add_option('-t',dest='TABULATE_SAVE',
                      help='use this flag to save the results to the file,defaults to under "~/LogMiner/results"',
                      action='store_true',default=False)
    parser.add_option('--tabulate-file', dest='TABULATE',
                      help='specify a file to save the tabulate table')
    parser.add_option('-o',dest='OMIT_SAVE',
                      help='use this flag to save the omit info that were not classified.' +\
                        'It would be saved under "~/LogMiner/results"',
                      action='store_true',default=False)
    parser.add_option('--omit-file', dest='OMIT',
                      help='specific a filename to save the omit info')
    return parser


def grep_lines(pattern, file_lines,do_eval=True):
    '''
    simulate linux command 'grep "xxx"'
    :param pattern: 'grep' pattern in linux command(regrex and woldcard unsupported);
        this pattern could be <string> or <list>(which means multi grep)
    :param file_lines: text to be search; <list> format, each element as a line in text;
        each_line should be right striped '\n'
    :param do_eval: eval() the pattern(to wipe off the double quote)
    :return: all lines that match pattern, type <list>
    '''
    # pattern = eval(pattern)        # out of security concern
    if do_eval:
        pattern = ast.literal_eval(pattern)
    if isinstance(pattern, str) or isinstance(pattern, unicode):
        lines = [each_line.rstrip('\n') for each_line in file_lines if pattern in each_line]
    elif isinstance(pattern, list):
        lines = [each_line.rstrip('\n') for each_line in file_lines if all(map(lambda x: x in each_line, pattern))]
    else:
        sys.exit('Error: wrong format in config file, some values are neither list nor string?')
    return lines

def grep_lines_from_file(pattern,file_name,do_eval):
    '''
    grep from the specified file name
    '''
    with open(file_name,'w+') as f_obj:
        return grep_lines(pattern,f_obj.readlines(),do_eval)

def grep_lines_count(pattern, file_lines,do_eval=True):
    '''
    simulate linux command 'grep "xxx"|wc -l'
    '''
    return len(grep_lines(pattern, file_lines,do_eval))


def wipe_exception(full_type):
    '''exceptions' full type name for short
    '''
    assert isinstance(full_type,str) is True
    if full_type.startswith('/All/Exception/') and full_type.endswith('(OMIT)') == False:
        return full_type[15:]
    elif full_type.startswith('/All/') and full_type.endswith('(OMIT)') == False:
        return full_type[5:]
    else:
        return None


def color_wrap(mes, color):
    '''return colored string
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


class MyConfigParser(ConfigParser.ConfigParser):

    def optionxform(self, optionstr):
        '''
        overrides method optionsxform(), make options case-sensitive
        use "SafeConfigParser().optionxform = str" is also fine
        '''
        return optionstr

    def getstring(self, section, option, raw=False, vars=None):
        '''
        define method getstring(), strip the '"' if the value contains double quote
        '''
        value = self.get(section, option)
        return value.lstrip('"').rstrip('"')

    def getlist(self, section, option, raw=False, vars=None):
        string_list = eval(self.get(section, option))
        assert isinstance(string_list, list) is True
        res_list = [each.lsplit('"').split('"') for each in string_list]
        return res_list


class MyTable(prettytable.PrettyTable):

    def get_row_data(self, row_number):
        '''
        return the data row specified,without the border and '\n';
        no.0 is the title,no.1 is the first value row
        '''
        self.set_style(prettytable.MSWORD_FRIENDLY)
        table_string_list = self.get_string().split('\n')
        assert isinstance(row_number,int)
        return table_string_list[row_number]

    def get_title_with_bar(self):
        '''
        return the table title with the border and '\n'(DEFAULT style)
        '''
        self.set_style(prettytable.DEFAULT)
        table_string_list = self.get_string().split('\n')
        return '\n'.join([table_string_list[0],table_string_list[1],table_string_list[2]])


if __name__ == '__main__':
    table = MyTable(['a','b'])
    table.add_row([1,2])
    table.add_row([3,4])
    print table
    print 'haha'
    print table.get_title()
    print table.get_row_data(1)
