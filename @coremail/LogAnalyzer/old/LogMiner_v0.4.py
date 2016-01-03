#coding=utf-8
'''
for
CM-23630[系统支持--rmi错误分类统计]
日志分析工具
'''
from optparse import OptionParser
import os
import datetime
from functions import MyConfigParser
from functions import grep_lines,option_parser
import json
import prettytable

#dfault setting
CONFIG_DEFAULT = os.path.join(os.getcwd(),'Exceptions_all.cf')
LOG_DEFAULT = '/home/coremail/logs/rmi_api.log'                                 #rmi_api.log
RESULT_PREFIX = 'rmi_exception_result_detail.'
RESULT_FOLDER = os.path.join(os.getcwd(),'results')


# step 1: load option args parser and default config
parser = option_parser(LOG_DEFAULT, CONFIG_DEFAULT, RESULT_FOLDER)
#(options,args) = parser.parse_args()
test_args = ['-l','rmi_api.log','-r','test.today']
(options,args) = parser.parse_args(test_args)
cf = options.CONFIG_FILE if options.CONFIG_FILE else CONFIG_DEFAULT
log = options.LOG_FILE if options.LOG_FILE else LOG_DEFAULT
result_file = options.RESULT_FILE if options.RESULT_FILE else RESULT_PREFIX


# step 2: load config file
config = MyConfigParser()
config.read(cf)
section_list = config.sections()



# step 3: traverse section_lsit and options_lsit, find the exception lines that match pattern
print '正在处理log...'
res_lines = {}
res_count = {}
with open(log) as f_obj:
    file_lines = f_obj.readlines()
    for each_section in section_list:
        # count all the children
        kv_lsit = config.items(each_section)
        for k,v in kv_lsit:
            match_lines = grep_lines(v,file_lines)
            k_name = each_section + '/' + k
            res_lines[k_name] = match_lines

#print res_lines
# res_lines_sorted = sorted(res_lines.iteritems(),key=lambda x:x[0])
# for each in res_lines_sorted:
#     print color_wrap(each[0],'red') + ' : ' + color_wrap(each[1],'green')

for k,v in res_lines.iteritems():
    res_count[k] = len(v)

# commented, replaced by prettytable-sort
# res_count_sorted = sorted(res_count.iteritems(),key=lambda x:x[0])
# for each in res_count_sorted:
#     print color_wrap(each[0],'red'),' : ',color_wrap(each[1],'green')

# step 4: save exception lines and count into file

ptable = prettytable.PrettyTable(['Error Type','Count'])
ptable.align['Error Type'] = "l"
for each_res in res_count.iteritems():
    ptable.add_row([each_res[0],each_res[1]])
ptable_str = ptable.get_string(sortby='Error Type',reversesort=True)
print '处理完毕，以下是error统计数目：'
print ptable_str

if options.RESULT_FILE:
    res_file = str(options.RESULT_FILE)
elif str(options.LOG_FILE).endswith('log'):
    res_file = RESULT_PREFIX + str(datetime.date.today())
else:
    res_file = RESULT_PREFIX + str(options.LOG_FILE).split('log.')[1]

res_lines_json = json.dumps(res_lines,indent=4)
file_to_save = os.path.join(RESULT_FOLDER,res_file)
with open(file_to_save,'a+') as f:
    f.write('###########################################\n')
    f.write(str(ptable_str) + '\n')
    f.write(res_lines_json)
    f.write('\n')

print '具体结果已经写入文件{0}'.format(file_to_save)