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
from functions import grep_wc,option_parser,color_wrap
import json,yaml


#dfault setting
CONFIG_DEFAULT = os.path.join(os.getcwd(),'Exceptions_all.cf')
LOG_DEFAULT = '/home/coremail/logs/rmi_api.log'                                 #rmi_api.log.2015-11-11
RESULT_PREFIX = 'rmi_exception_result_detail.'
RESULT_FOLDER = os.path.join(os.getcwd(),'results')


# step 1: load option args parser and default config
parser = option_parser(LOG_DEFAULT,CONFIG_DEFAULT,RESULT_PREFIX,RESULT_FOLDER)
#(options,args) = parser.parse_args()
test_args = ['-l','rmi_api.log.2015-11-11','-r','test.today']
(options,args) = parser.parse_args(test_args)
cf = options.CONFIG_FILE if options.CONFIG_FILE else CONFIG_DEFAULT
log = options.LOG_FILE if options.LOG_FILE else LOG_DEFAULT
result_file = options.RESULT_FILE if options.RESULT_FILE else RESULT_PREFIX
print cf
print log
print result_file


# step 2: load config file
config = ConfigParser()
config.read(cf)
section_list = config.sections()

# step 3: traverse config dict,  count the exception times
res_dict = {}
with open(log) as f_obj:
    file_lines = f_obj.readlines()
    for each_section in section_list:
        print each_section
        # count all the children
        kv_lsit = config.items(each_section)
        for k,v in kv_lsit:
            print k,'=',v
            count = grep_wc(v,file_lines)
            k_name = each_section + '/' + k
            res_dict[k_name] = count



print res_dict
res_list = sorted(res_dict.iteritems(),key=lambda x:x[0])
print json.dumps(res_dict,indent=2)

for each in res_list:
    print color_wrap(each[0],'red'),' : ',color_wrap(each[1],'green')







