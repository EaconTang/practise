# coding=utf-8
"""
all the functions needed by log_miner.py
"""

import ConfigParser
from optparse import OptionParser
import ast
import sys
import prettytable


def option_parser():
    """
    give optional arguments while execute the program
    :return: a option parser
    """
    usage = "usage: python %prog [-f value] [-c value] [-t] [-T value] [-o] [-O value] [-y]"
    parser = OptionParser(usage)
    parser.add_option('-f', '--file', dest='FILE',
                      help='specify a log file to be scan, defaults to today\'s rmi_api.log')
    parser.add_option('-c', '--config', dest='CONFIG',
                      help='specify a config file to be load,defaults to ~/LogMiner/conf/rmi_exceptions.cf')
    parser.add_option('-t','--tabulate',dest='TABULATE_SAVE',
                      help='use this flag to save the results to the file,defaults to under "~/LogMiner/results"',
                      action='store_true',default=False)
    parser.add_option('-T','--tabulate-file', dest='TABULATE',
                      help='specify a file to save the tabulate table,defaults to "rmi_api_error.tabulate"')
    parser.add_option('-o','--omit',dest='OMIT_SAVE',
                      help='use this flag to save the omit info that were not classified.' +
                        'It would be saved under "~/LogMiner/results"',
                      action='store_true',default=False)
    parser.add_option('-O','--omit-file', dest='OMIT',
                      help='specific a filename to save the omit info,defaults to "rmi_api.omit.{LogDate}"')
    parser.add_option('-y','--yesterday-log', dest='YESTERDAY_LOG',
                      help='plus this flag to specify yesterday\'s log file, based on the file specify by \'-f\'',
                      action='store_true',default=False)
    parser.add_option('-D',dest='DOMAIN_RATIO',
                      help='use this flag to calculate domain success ratio',
                      action='store_true',default=False)
    parser.add_option('--datetime',dest='DATETIME',
                      help='specify a time period as format "YYYYMMDD:YYYYMMDD"')
    return parser


def grep_lines(pattern, file_lines,do_eval=True):
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
        pattern = ast.literal_eval(pattern)
    if isinstance(pattern, str) or isinstance(pattern, unicode):
        lines = [each_line.rstrip('\n') for each_line in file_lines if pattern in each_line]
    elif isinstance(pattern, list):
        lines = [each_line.rstrip('\n') for each_line in file_lines if all(map(lambda x: x in each_line, pattern))]
    elif isinstance(pattern,tuple):
        lines = [each_line.rstrip('\n') for each_line in file_lines if any(map(lambda x: x in each_line, pattern))]
    else:
        sys.exit('Error: wrong format in config file, some values are neither list nor string?')
    return lines

def grep_lines_from_file(pattern,file_name,do_eval):
    """
    grep from the specified file name
    """
    with open(file_name,'w+') as f_obj:
        return grep_lines(pattern,f_obj.readlines(),do_eval)

def grep_lines_count(pattern, file_lines,do_eval=True):
    """
    simulate linux command 'grep "xxx"|wc -l'
    """
    return len(grep_lines(pattern, file_lines,do_eval))


def wipe_exception(full_type):
    """exceptions' full type name for short
    """
    assert isinstance(full_type,str) is True
    if full_type.startswith('/All/Exception/') and full_type.endswith('(OMIT)') == False:
        return full_type[15:]
    elif full_type.startswith('/All/') and full_type.endswith('(OMIT)') == False:
        return full_type[5:]
    else:
        return None


def color_wrap(mes, color):
    """return colored string
    """
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


def memo(f):
    cache = {}
    pass


def compute_domain_ratio(config,res_count):
    """
    compute ratio of each domain's connect success and accountProcess success
    :return a result dict,key=domain,value=ratios
    """
    res = {}
    domain_list = config.options('/All/Exception/server fail')

    server_fail = {}
    account_process = {}
    account_process_OK = {}
    for each in domain_list:
        server_fail[each] = res_count['/'.join(['/All/Exception/server fail',each])]
        account_process[each] = res_count['/'.join(['/All/Normal/AccountProcessed',each])]
        account_process_OK[each] = res_count['/'.join(['/All/Normal/AccountProcessed/_OK',each])]

    for each in domain_list:
        try:
            connect_success_ratio = format(account_process[each]/float(account_process[each] + server_fail[each]),'.2%')
            account_process_OK_ratio = format(account_process_OK[each]/float(account_process[each]),'.2%')
        except ZeroDivisionError,e:
            connect_success_ratio = account_process_OK_ratio = None
        # print '\n======',each,'======'
        # print '服务器连接成功率：',connect_success_ratio,
        #
        # print '代收成功率：',account_process_OK_ratio

        res[each] = str(connect_success_ratio).ljust(6) + ' ' + str(account_process_OK_ratio).rjust(6)

    return res


def write_target_file(from_tabulate,target_file):
    """
    write tabulate to target file;do check on table title's differ
    :param from_tabulate: a tabulate,just one title row and one data row
    :param target_file: a file maybe contain some tabulate data
    """
    with open(target_file, 'a+') as f:
        # major row to insert: result of this time
        to_write = from_tabulate.get_row_data(1) + '\n'

        target_file_lines = open(target_file).readlines()
        target_file_titles = grep_lines('LogDate', target_file_lines, False)
        if target_file_lines == []:
            # means a new file
            to_write = from_tabulate.get_title_with_bar() + '\n' + to_write
            f.write(to_write)
        elif target_file_titles != [] and from_tabulate.get_row_data(0) != target_file_titles[-1]:
            print target_file_titles
            print from_tabulate.get_row_data(0)
            print target_file_titles[-1]
            # means config updated
            to_write = '\n###############config file is updated##############\n\n' + \
                       from_tabulate.get_title_with_bar() + '\n' + \
                       to_write
            f.write(to_write)
        else:
            # just add it
            f.write(to_write)

        print '本次统计已经写入汇总文件表：{0}'.format(target_file)


class MyConfigParser(ConfigParser.ConfigParser):

    def optionxform(self, optionstr):
        """
        overrides method optionsxform(), make options case-sensitive
        use "SafeConfigParser().optionxform = str" is also fine
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
        assert isinstance(row_number,int)
        return table_string_list[row_number]

    def get_title_with_bar(self):
        """
        return the table title with the border and '\n'(DEFAULT style)
        """
        self.set_style(prettytable.DEFAULT)
        table_string_list = self.get_string().split('\n')
        return '\n'.join([table_string_list[0],table_string_list[1],table_string_list[2]])


if __name__ == '__main__':
    f_lines = ["a","b","c","ab"]
    p1 = '"a"'
    p2 = '["a","b"]'
    p3 = '("a","b")'
    print grep_lines(p1,f_lines)
    print grep_lines(p2,f_lines)
    print grep_lines(p3,f_lines)
