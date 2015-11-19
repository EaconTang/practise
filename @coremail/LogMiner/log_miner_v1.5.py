#coding=utf-8
'''
for
CM-23630[系统支持--rmi错误分类统计]
日志分析工具
'''
import os
import datetime
from functions import *
import json
import prettytable

############################################
# step 1: load option args parser and config

# default setting
CONFIG = os.path.join(os.getcwd(),'conf','rmi_exceptions.cf')
YESTERDAY = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
LOG = '/home/coremail/logs/rmi_api.log.{0}'.format(YESTERDAY)
RESULT_FOLDER = os.path.join(os.getcwd(),'results')
OMIT = os.path.join(RESULT_FOLDER,'rmi_api.omit')
TABULATE = os.path.join(RESULT_FOLDER,'rmi_api_error.tabulate')

# load arg-parser
parser = option_parser()
(options,args) = parser.parse_args()
cf = options.CONFIG if options.CONFIG else CONFIG
log = options.FILE if options.FILE else LOG
omit_file = options.OMIT if options.OMIT else OMIT           # program would add file date as suffix
tabulate_file = options.TABULATE if options.TABULATE else TABULATE

# load config
config = MyConfigParser()
config.read(cf)
section_list = sorted(config.sections())


###############################################################
# step 2: traverse section_lsit and options_lsit;
# find and count the exception lines that match(or not) pattern
print '正在处理log...'
res_lines = {}
res_count = {}
omit_lines = {}
omit_lines_count = {}
omit_lines_list = []          # no remove-duplication operation

with open(log) as f_obj:
    file_lines_all = f_obj.readlines()
    # [/All] is the root
    res_count['/All'] = len(file_lines_all)
    file_lines_all_strip = [each.rstrip('\n') for each in file_lines_all]

    for each_section in section_list:
        # find if this section has parent, if yes, grep from parent file_lines
        if res_lines.has_key(each_section):
            file_lines = res_lines[each_section]
        else:
            file_lines = file_lines_all_strip
        kv_list = config.items(each_section)
        # traverse the options and values under the section
        for k,v in kv_list:
            match_lines = grep_lines(v,file_lines)
            key = each_section + '/' + k
            res_lines[key] = match_lines

        # find those omit errors; those who has no omit part would not be count its '0'
        child_lines = []                                    # file_line == parent_lines
        for each_option in config.options(each_section):
            each_option = each_section + '/' + each_option
            child_lines += res_lines[each_option]
        # remove duplicates
        child_lines_set = set(child_lines)
        file_lines_set = set(file_lines)
        omit_part = list(child_lines_set^file_lines_set)

        if len(omit_part) != 0:
            omit_key = each_section + '/(OMIT)'
            omit_lines[omit_key] = omit_part
            omit_lines_count[omit_key] = len(file_lines) - len(child_lines)

# now count the lines
for k,v in res_lines.iteritems():
    res_count[k] = len(v)
res_count = dict(omit_lines_count,**res_count)


################################
# step 3: print and save results
ptable = prettytable.PrettyTable(['Type','Count'])
ptable.align['Type'] = "l"
for each_res in res_count.iteritems():
    ptable.add_row([each_res[0],each_res[1]])

ptable_sortByType = ptable.get_string(sortby='Type')
ptable_sortByCount = ptable.get_string(sortby='Count',reversesort=True)
print '处理完毕!\n以下是统计数目：'
print ptable_sortByType
print ptable_sortByCount

file_date = ''           # date of the log_file, also used below in tabulate table
if 'log' in log and not log.endswith('log'):
    file_date = str(log.split('.log.')[1])
else:
    file_date = str(datetime.date.today())

# save all omit info if this flag is used
if options.OMIT_SAVE:
    omit_file += '.' + file_date
    omit_exceptions_json = json.dumps(omit_lines['/All/Exception/(OMIT)'],indent=2)
    with open(omit_file,'w') as f:
        write_info = str(ptable_sortByType) + '\n'
        write_info += str(ptable_sortByCount) + '\n'
        write_info += '###########################################\n'
        write_info += '未统计的错误信息如下：\n'
        write_info += omit_exceptions_json + '\n'
        f.write(write_info)
    print '未统计的错误信息已经写入文件{0}'.format(omit_file)


################################
# tabulate table;
# excenptions' short name;
# omit part uncontained;
# automatically check the config
if options.TABULATE_SAVE:
    # insert the title
    res_count_tabulate = {}
    for key in res_count.keys():
        exception_short = wipe_exception(key)
        if exception_short:
            res_count_tabulate[exception_short] = res_count[key]
    table_title = ['LogDate']
    keys_sort = sorted(res_count_tabulate.keys())
    table_title.extend(keys_sort)
    table_title.append('WriteTime')
    tabulate_table = MyTable(table_title)

    # insert thr result of this time
    table_row = []
    table_row.append(file_date)
    for key in keys_sort:
        table_row.append(res_count_tabulate[key])
    table_row.append(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    tabulate_table.add_row(table_row)

    # write into file
    with open(tabulate_file,'a+') as f:
        # major row to insert: result of this time
        to_write = tabulate_table.get_row_data(1)+ '\n'
        
        tabulate_file_lines = open(tabulate_file).readlines()
        tabulate_file_titles = grep_lines('LogDate',tabulate_file_lines,False)
        if tabulate_file_lines == []:
            # means a new file
            to_write = tabulate_table.get_title_with_bar() + '\n' + to_write
            f.write(to_write)
        elif tabulate_file_titles != [] and tabulate_table.get_row_data(0) != tabulate_file_titles[-1]:
            # means config updated
            to_write = '\n###############config file is updated##############\n\n' + \
                       tabulate_table.get_title_with_bar() + '\n' + \
                       to_write
            f.write(to_write)
        else:
            # just add it
            f.write(to_write)

        print '本次统计已经写入汇总文件表：{0}'.format(tabulate_file)
