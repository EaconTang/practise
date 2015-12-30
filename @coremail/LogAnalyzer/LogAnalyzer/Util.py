# coding=utf-8
"""
custom functions and classes
"""
from ConfigParser import ConfigParser
from ast import literal_eval
import prettytable
from re import match
from sys import exit
import datetime
from math import fabs


def convert_to_logfiles(time_period, logfile):
    """
    deal with log time;
    allow more flexible time specified by user
    """
    if not match(r'\d{8}:\d{8}', time_period):
        exit('Wrong format for time period!')

    start, end = time_period.split(':')
    start_date = datetime.datetime.strptime(start, '%Y%m%d').date()
    end_date = datetime.datetime.strptime(end, '%Y%m%d').date()

    time_delta = int(fabs(int((end_date - start_date).days))) + 1
    datetime_list = [start_date + datetime.timedelta(i) for i in range(time_delta)]

    datetime_list = map(lambda x: x.strftime('%Y-%m-%d'), datetime_list)
    print datetime_list
    return map(lambda x: '.'.join([logfile, x]), datetime_list)


def grep_lines(pattern, file_lines, do_eval=True):
    """
    simulate linux command 'grep "xxx"'
    :param pattern: 'grep' pattern in linux command(regrex and woldcard unsupported);
        this pattern could be <string> or <list>(means 'AND' multi grep) or <tuple>(means 'OR' multi grep)
    :param file_lines: text to be search; <list> format, each element as a line in text;
        each_line should be right striped '\n'
    :param do_eval: eval() the pattern(to wipe off the double quote)
    :return: all lines that match pattern, type <list>
    """
    # pattern = eval(pattern)        # out of security concern
    if do_eval:
        pattern = literal_eval(pattern)
    if isinstance(pattern, str) or isinstance(pattern, unicode):
        lines = [each_line.rstrip('\n') for each_line in file_lines if pattern in each_line]
    elif isinstance(pattern, list):
        lines = [each_line.rstrip('\n') for each_line in file_lines if all(map(lambda x: x in each_line, pattern))]
    elif isinstance(pattern, tuple):
        lines = [each_line.rstrip('\n') for each_line in file_lines if any(map(lambda x: x in each_line, pattern))]
    else:
        exit('Error: wrong format in config file, some values are neither list nor string?')
    return lines


def grep_lines_from_file(pattern, file_name, do_eval):
    """
    grep from the specified file name
    """
    with open(file_name, 'w+') as f_obj:
        return grep_lines(pattern, f_obj.readlines(), do_eval)


def grep_lines_count(pattern, file_lines, do_eval=True):
    """
    simulate linux command 'grep "xxx"|wc -l'
    """
    return len(grep_lines(pattern, file_lines, do_eval))


def wipe_exception(full_type):
    """exceptions' full type name for short
    """
    assert isinstance(full_type, str) is True
    if full_type.startswith('/All/Exception/') and full_type.endswith('(OMIT)') == False:
        return full_type[15:]
    elif full_type.startswith('/All/') and full_type.endswith('(OMIT)') == False:
        return full_type[5:]
    else:
        return None


def color_wrap(mes, color):
    """return colored string
    """
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    ENDC = '\033[0m'

    mes = str(mes)
    if color == 'red':
        return RED + mes + ENDC
    elif color == 'yellow':
        return YELLOW + mes + ENDC
    elif color == 'green':
        return GREEN + mes + ENDC
    elif color == 'blue':
        return BLUE + mes + ENDC
    else:
        exit('Error: unsupport color?')


def printinfo():
    def _printinfo(f):
        def __printinfo(*args, **kwargs):
            try:
                f(*args, **kwargs)
                print 'OK! Finish doing {0}...'.format(f.func_name)
        return __printinfo
    return _printinfo


def write_target_file(from_tabulate, target_file):
    """
    write tabulate to target file;do check on table title's differ
    :param from_tabulate: a tabulate,just one title row and one data row
    :param target_file: a file which maybe contain some tabulate data
    """
    with open(target_file, 'a+') as f:
        # major row to insert: result of this time
        to_write = from_tabulate.get_row_data(1) + '\n'

        target_file_lines = open(target_file).readlines()
        target_file_titles = grep_lines('LogDate', target_file_lines, False)
        if not target_file_lines:
            # means a new file
            to_write = from_tabulate.get_title_with_bar() + '\n' + to_write
            f.write(to_write)
        elif target_file_titles != [] and from_tabulate.get_row_data(0) != target_file_titles[-1]:
            # print target_file_titles
            # print from_tabulate.get_row_data(0)
            # print target_file_titles[-1]
            # means config updated
            to_write = '\n###############config file is updated##############\n\n' + \
                       from_tabulate.get_title_with_bar() + '\n' + \
                       to_write
            f.write(to_write)
        else:
            # just add it
            f.write(to_write)

        # print '本次统计已经写入汇总文件表：{0}'.format(target_file)


class MyConfigParser(ConfigParser):
    def optionxform(self, optionstr):
        """
        overrides method optionsxform(), make options case-sensitive
        use "SafeConfigParser().optionxform = str" is also fine
        :param optionstr:
        """
        return optionstr

    def getstring(self, section, option, raw=False, vars=None):
        """
        define method getstring(), strip the '"' if the value contains double quote
        """
        value = self.get(section, option)
        return value.lstrip('"').rstrip('"')

    def getlist(self, section, option, raw=False, vars=None):
        string_list = eval(self.get(section, option))
        assert isinstance(string_list, list) is True
        res_list = [each.lsplit('"').split('"') for each in string_list]
        return res_list


class MyTable(prettytable.PrettyTable):
    def get_row_data(self, row_number):
        """
        return the data row specified,without the border and '\n';
        no.0 is the title,no.1 is the first value row
        """
        self.set_style(prettytable.MSWORD_FRIENDLY)
        table_string_list = self.get_string().split('\n')
        assert isinstance(row_number, int)
        return table_string_list[row_number]

    def get_title_with_bar(self):
        """
        return the table title with the border and '\n'(DEFAULT style)
        """
        self.set_style(prettytable.DEFAULT)
        table_string_list = self.get_string().split('\n')
        return '\n'.join([table_string_list[0], table_string_list[1], table_string_list[2]])
