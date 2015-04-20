#-*- coding:UTF-8 -*-

f = open('test.rtf')
s = f.read()
f.close()
print type(s)   #输出既有文件内容的类型：str（字节串）

uni = s.decode('UTF-8')     #将其转换为unicode字符串

s = uni.encode('UTF-8')         #再编码为u8格式
f = open('test1.rtf','w')       #（新建）打开文件
f.write(s)
f.close()
