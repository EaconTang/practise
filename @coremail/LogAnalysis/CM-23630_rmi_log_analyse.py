#coding=utf-8
'''
for
CM-23630[系统支持--rmi错误分类统计]
日志分析工具
'''
from optparse import OptionParser
import os
import time,datetime
#print datetime.date.today()

#dfault setting
CONFIG = '/home/LogAnalysis/config.py'
LOG = '/home/coremail/logs/rmi_api.log'
RESULT_FOLDER = '/home/LogAnalysis/results/'

parser = OptionParser()
parser.add_option('-l','--log',dest='LOG_FILE',
                  help='specify a log file, defaults to "/home/coremail/logs/rmi_api.log"',
                  default=LOG)
parser.add_option('-r','--result',dest='RESULT_FILE',
                  help='specify the file to save the result, defaults to "rmi_exception_result.%Datetime of log%".' +
                       'It would be saved under the folder "/home/LogAnalysis/results/"',)
parser.add_option('-c','--config',dest='CONFIG_FILE',
                  help='specify a config file, defaults to "config.py"',
                  default=CONFIG)


print parser.print_help()
