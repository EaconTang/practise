# coding=utf-8
'''
有个目录，里面是你自己写过的程序，统计一下你写过多少行代码。包括空行和注释，但是要分别列出来。
'''
import os,re


#识别.py后缀的文件
def pyFile(file_name):
    matchObj = re.match(r'.+\.py$',file_name)
    if matchObj:
        return True
    else:
        return False

dirlist = os.listdir(os.getcwd())  #获取当前目录下的文件列表
py_list = filter(pyFile, dirlist)  #过滤出python文件

code_line = 0
space_line = 0
comment_line = 0

for each_file in py_list:       #遍历pyhton文件，用正则检查它是什么行
    with open(each_file) as fileObj:
        for each_line in fileObj.readlines():
            if re.match(r'^#.*',each_line):
                comment_line += 1
            elif re.match(r'\n',each_line):
                space_line += 1
            else:
                code_line += 1

print '代码行数:',code_line
print '空行:',space_line
print '注释:',comment_line