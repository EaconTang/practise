#coding=utf-8

'''
使用json模块处理json文件
编码为json：dumps(obj,sort_keys,indent,separators,skipkeys)
将json解码：loads(obj)
'''
import json

json_text = '[1,{"d":2,"c":[4,5,6]},7,8,9]'

text = json.loads(json_text)

print json.dumps(text,sort_keys=True)

