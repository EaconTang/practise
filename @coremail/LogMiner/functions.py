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
                    help='specify a config file, defaults to "Exceptions_Main.cfg"',
                    default=config)
    parser.add_option('-r','--result',dest='RESULT_FILE',
                    help='specify the file to save the result, defaults to "{0}%Datetime%".\
                    It would be saved under the folder "{1}"'.format(res_prefix,res_folder))

    return parser

def grep_wc(pattern,file_lines):
    return sum(1 for each_line in file_lines if pattern in each_line)
