# coding=utf-8
'''
有个目录，里面是你自己写过的程序，统计一下你写过多少行代码。包括空行和注释，但是要分别列出来。
'''

import os
import re


# 识别.py后缀的文件
def pyFile(file_name):
    matchObj = re.match(r'.+\.py$', file_name)
    return matchObj


dirlist = os.listdir(os.getcwd())  # 获取当前目录下的文件列表
py_list = filter(lambda x: re.match(r'.+\.py$', x), dirlist)  # 过滤出python文件,pyFile函数的lambda形式

code_line = 0
space_line = 0
comment_line = 0
trichar = 0

for each_file in py_list:  # 遍历pyhton文件，用正则检查它是什么行
    with open(each_file) as fileObj:
        for n, each_line in enumerate(fileObj.readlines()):  # 用索引的方式，获悉第几行
            if re.match(r'\n', each_line):
                space_line += 1
            elif re.match(r'^#.*', each_line):
                comment_line += 1
            elif re.match(r'\'\'\'', each_line):
                trichar += 1  # 计算行首'''三引号的数量
                odd_line = n  # 保存出现的第奇数个三引号的行数
                comment_line += 1
                # 这里计算两个引号间的行数
                if trichar % 2 == 0:
                    comment_line = n - odd_line + comment_line
            else:
                code_line += 1

print '代码行数:', code_line
print '空行:', space_line
print '注释:', comment_line
