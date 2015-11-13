#coding=utf-8
'''
all the functions you need
'''

def option_parser(log, config, res_prefix, res_folder):
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-l','--log',dest='LOG_FILE',
                    help='specify a log file, defaults to "/home/coremail/logs/rmi_api.log"',
                    default=log)
    parser.add_option('-c','--config',dest='CONFIG_FILE',
                    help='specify a config file, defaults to "Exceptions_Main.cf"',
                    default=config)
    parser.add_option('-r','--result',dest='RESULT_FILE',
                    help='specify the file to save the result, defaults to "{0}%Datetime%".\
                    It would be saved under the folder "{1}"'.format(res_prefix,res_folder))
    return parser


def grep_wc(pattern,file_lines):
    return sum(1 for each_line in file_lines if pattern in each_line)



def color_wrap(mes,color):
    BLUE          = '\033[0;34m'
    GREEN         = '\033[0;32m'
    RED           = '\033[0;31m'
    YELLOW        = '\033[1;33m'
    ENDC          = '\033[0m'
    mes = str(mes)
    if color == 'red':
        return RED + mes + ENDC
    elif color == 'yellow':
        return YELLOW + mes + ENDC
    elif color == 'green':
        return GREEN + mes + ENDC
    elif color == 'blue':
        return BLUE + mes +ENDC


if __name__ == '__main__':
    print color_wrap('test','red')