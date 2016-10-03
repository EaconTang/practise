# coding=utf-8

'''
使用json模块处理json文件
编码为json：dumps(obj,sort_keys,indent,separators,skipkeys)
将json解码：loads(obj)
'''
import json

json_text = '{"d": "$mbox($inp(1))","c":[4,5,6]}'

text = json.loads(json_text)

filetext = json.dumps(text, sort_keys=True)

f = open("Scripts4Test.txt", "w")
f.write(filetext)
f.close()
