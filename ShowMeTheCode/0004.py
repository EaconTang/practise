#coding=utf-8

'''
任一个英文的纯文本文件，统计其中的单词出现的个数。
用split获取单词列表太愚蠢，直接用正则r'\w+'找可以不用考虑太多细节
使用Counter数据结构快多了
'''

import re
from collections import Counter


with open("Scripts4Test.txt") as f:
    text = f.read()
    text_list = re.findall(r'\w+',text)
    print Counter(text_list)


'''
adict = {}

#处理带符号单词之类的
def dealWord(string_text):
    dealtWord = ''
    for each in string_text:
        if each.isalpha():
            dealtWord += each
    return dealtWord


#统计单词次数
def cal(eachword):
    if not adict.has_key(eachword):
        adict[eachword] = 1
    else:
        adict[eachword] += 1

#改用正则筛选含不规则字符的单词
def reg(word):
    matchObj = re.match(r'\W*(\w+)\W*',word)
    if matchObj:
        newword = matchObj.group(1)
        return newword
    else:
        return '0'          #未匹配到一个合法单词返回0

with open('Scripts4Test.txt') as file:
    text =  file.read()

split_text = text.split()        #将所有单词组成一个列表

#使用collections模块的数据结构Counter
import collections
print collections.Counter(split_text)

for each_word in split_text:
        each_word = reg(each_word)
        if each_word != '0':
            cal(each_word)

list1 = adict.items()
print sorted(list1,key=lambda x:(x[1],x[0]),reverse=True)          #使用key参数使之按统计次数由大到小排序
'''
