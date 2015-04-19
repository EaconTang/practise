#coding=utf-8

'''
任一个英文的纯文本文件，统计其中的单词出现的个数。
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

with open('test.txt') as file:
    text =  file.read()

split_text = text.split()        #将所有单词组成一个列表


for each_word in split_text:
    if each_word.isalpha():
        cal(each_word)
    else:
        each_word = dealWord(each_word)
        cal(each_word)

list1 = adict.items()
print sorted(list1,key=lambda x:(x[1],x[0]),reverse=True)          #使用key参数使之按统计次数由大到小排序
