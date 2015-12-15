#coding=utf-8
'''
for
CM-23630[系统支持--rmi错误分类统计]
日志分析工具
'''
import os
import datetime
from functions import MyConfigParser
from functions import grep_lines,option_parser
import json
import prettytable


#dfault setting
CONFIG_DEFAULT = os.path.join(os.getcwd(),'rmi_exceptions.cf')
LOG_DEFAULT = '/home/coremail/logs/rmi_api.log'                                 #rmi_api.log.2015-11-11
RESULT_PREFIX = 'rmi_result.'
RESULT_FOLDER = os.path.join(os.getcwd(),'results')


# step 1: load option args parser and default config
parser = option_parser(LOG_DEFAULT, CONFIG_DEFAULT, RESULT_FOLDER)
#(options,args) = parser.parse_args()
test_args = ['-f','rmi_api.log.2015-11-11','-r','test.today','-s']
(options,args) = parser.parse_args(test_args)
cf = options.CONFIG_FILE if options.CONFIG_FILE else CONFIG_DEFAULT
log = options.LOG_FILE if options.LOG_FILE else LOG_DEFAULT
result_file = options.RESULT_FILE if options.RESULT_FILE else RESULT_PREFIX


# step 2: load config file
config = MyConfigParser()
config.read(cf)
section_list = sorted(config.sections())


# step 3: traverse section_lsit and options_lsit, find the exception lines that match(or not) pattern
print '正在处理log...'
res_lines = {}
res_count = {}
omit_lines = {}
omit_lines_count = {}
omit_lines_list = []        #no remove-duplicate operation, not equals to len(omit_lines)
with open(log) as f_obj:
    file_lines_all = f_obj.readlines()
    res_count['/All'] = len(file_lines_all)     #[/All] is the root
    for each in file_lines_all:
        each.strip('\n')
    for each_section in section_list:
        # find if this section has parent, if yes, grep from parent file_lines
        if res_lines.has_key(each_section):
            file_lines = res_lines[each_section]
        else:
            file_lines = file_lines_all
        kv_list = config.items(each_section)
        for k,v in kv_list:
            match_lines = grep_lines(v,file_lines)
            key = each_section + '/' + k
            res_lines[key] = match_lines
        # find those omit errors
        # file_line == parent_lines
        child_lines = []
        for each_option in config.options(each_section):
            each_option = each_section + '/' + each_option
            child_lines += res_lines[each_option]
        #remove duplicates
        child_lines_set = set(child_lines)
        file_lines_set = set(file_lines)
        omit_part = list(child_lines_set^file_lines_set)
        if len(omit_part) != 0:
            omit_key = each_section + '/(OMIT)'
            omit_lines[omit_key] = omit_part
            omit_lines_count[omit_key] = len(file_lines) - len(child_lines)

#count lines
for k,v in res_lines.iteritems():
    res_count[k] = len(v)
res_count = dict(omit_lines_count,**res_count)


# step 4: save exception lines and count into file
ptable = prettytable.PrettyTable(['Type','Count'])
ptable.align['Type'] = "l"
for each_res in res_count.iteritems():
    ptable.add_row([each_res[0],each_res[1]])
ptable_sortByType = ptable.get_string(sortby='Type')
ptable_sortByCount = ptable.get_string(sortby='Count',reversesort=True)
print '处理完毕!\n以下是统计数目：'
print ptable_sortByType
print ptable_sortByCount


if options.RESULT_FILE:
    res_file = str(options.RESULT_FILE)
elif str(options.LOG_FILE).endswith('log'):
    res_file = RESULT_PREFIX + str(datetime.date.today())
else:
    res_file = RESULT_PREFIX + str(options.LOG_FILE).split('log.')[1]

omit_exceptions_json = json.dumps(omit_lines['/All/Exception/(OMIT)'],indent=2)
file_to_save = os.path.join(RESULT_FOLDER,res_file)
with open(file_to_save,'w') as f:
    f.write('###########################################\n')
    f.write(str(ptable_sortByType) + '\n')
    f.write(str(ptable_sortByCount) + '\n')
    f.write(omit_exceptions_json + '\n')

print '具体结果已经写入文件{0}'.format(file_to_save)