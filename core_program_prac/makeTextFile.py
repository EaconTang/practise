#coding=utf-8

'''
使用文件操作
创建一个新文件并输入内容
'''

import os

while 1:
    file_name = raw_input("Input the file name:")

    if os.path.exists(file_name):
        print "Error:file exist!"
    else:
        break

input_text = []
line_number = 1

print "Input your text line by line('input \"$quit\" to end'):"

while 1:

    line_str = raw_input("Line%d:"%line_number)
    if line_str == "$quit":
        break
    else:
        input_text.append(line_str)
        line_number += 1



this_file = open(file_name,"w")
this_file.writelines(["%s%s"%(each_line,os.linesep) for each_line in input_text])
this_file.close()

print 'Done!'




