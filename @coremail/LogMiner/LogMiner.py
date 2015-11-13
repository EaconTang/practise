#coding=utf-8
'''
for
CM-23630[系统支持--rmi错误分类统计]
日志分析工具
'''
from optparse import OptionParser
import os
import datetime
from ConfigParser import ConfigParser
from functions import grep_wc,option_parser
import json


#dfault setting
CONFIG_DEFAULT = '/home/coremail/logs/LogMiner/Exceptions_Main.cfg'
LOG_DEFAULT = '/home/coremail/logs/rmi_api.log'                                 #rmi_api.log.2015-11-11
RESULT_PREFIX = 'rmi_exception_result.'
RESULT_FOLDER = os.path.join(os.getcwd(),'results')


# step 1: load option args parser
parser = option_parser(LOG_DEFAULT,CONFIG_DEFAULT,RESULT_PREFIX,RESULT_FOLDER)
#(options,args) = parser.parse_args()
test_args = ['-l','rmi_api.log.2015-11-11','-c','Exceptions_Main.cfg','-r','test.today']
(options,args) = parser.parse_args(test_args)



# step 2: load config file
config = ConfigParser()
config.read(options.CONFIG_FILE)
section_list = config.sections()



# step 3: traverse sections, calculate all the exceptions times
res_dict = {}
with open(options.LOG_FILE) as f_obj:
    file_lines = f_obj.readlines()
    for each_section in section_list:
        name = config.get(each_section,'name')
        pattern = config.get(each_section,'pattern')
        count = grep_wc(pattern,file_lines)
        res_dict[name] = count



# step 4: print and generate the report file
res_json = json.dumps(res_dict,indent=2)
print res_json

if options.RESULT_FILE:
    res_file = str(options.RESULT_FILE)
elif str(options.LOG_FILE).endswith('log'):
    res_file = RESULT_PREFIX + str(datetime.date.today())
else:
    res_file = RESULT_PREFIX + str(options.LOG_FILE).split('log.')[1]

with open(os.path.join(RESULT_FOLDER,res_file),'a+') as f:
    f.write('###########################################\n')
    f.write(res_json)
    f.write('\n')


print 'Done!'





