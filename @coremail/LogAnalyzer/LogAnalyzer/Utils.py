# coding=utf-8
"""
Some custom functions and classes
"""
import datetime
import json
from ConfigParser import ConfigParser
from math import fabs
from re import match
from sys import exit

import prettytable


def convert_time_period(time_period, logfile):
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
    datetime_list = [start_date + datetime.timedelta(i) for i in xrange(time_delta)]
    datetime_list = map(lambda x: x.strftime('%Y-%m-%d'), datetime_list)

    file_list = map(lambda x: '.'.join([logfile, x]), datetime_list)
    return str(time_period), file_list


def color_wrap(mes, color):
    """return colored string
    """
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    ENDC = '\033[0m'

    mes = str(mes)
    if color.lower() == 'red':
        return RED + mes + ENDC
    elif color.lower() == 'yellow':
        return YELLOW + mes + ENDC
    elif color.lower() == 'green':
        return GREEN + mes + ENDC
    elif color.lower() == 'blue':
        return BLUE + mes + ENDC
    else:
        exit('Error: unsupport color?')


def log_info():
    """
    a decorator for printing program info
    as a log util
    """
    def _printinfo(f):
        def __printinfo(*args, **kwargs):
            res = None
            print color_wrap('['+time.clock()+']', 'yellow')
            print color_wrap('Start to {0}()...'.format(f.func_name), 'blue')
            try:
                res = f(*args, **kwargs)
                print color_wrap('OK! {0}() finish!'.format(f.func_name), 'green')
            except Exception, e:
                print e.message
                print color_wrap('Fail to {0}()!'.format(f.func_name), 'red')
            finally:
                return res
        return __printinfo
    return _printinfo


def dict_to_json(res, indent=4, sort_by_key=True):
    assert isinstance(res, dict)
    try:
        return json.dumps(res, indent=indent,sort_keys=sort_by_key)
    except:
        exit('[Error]')

def list_to_json(res, indent=2):
    assert isinstance(res, list)
    try:
        return json.dumps(res, indent=indent)
    except:
        exit('[Error]')



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


if __name__ == '__main__':
    pass