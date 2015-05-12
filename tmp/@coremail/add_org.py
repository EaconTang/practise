#!/bin/usr/python
#-*- coding:UTF-8 -*-
import os
import string

#定义添加一级部门的函数
def add_primary(org_id,unit_id,unit_name,n):
        for i in range(1,int(n)+1):
                cmd = '/home/coremail/bin/sautil add ou \"org_id=%s&org_unit_id=%s%d&org_unit_name=%s%d\"'%(org_id,unit_id,i,unit_name,i)
                os.system(cmd)
                #print 'add org unit a/a%d success!'%i        #XT3以下版本请撤销本行注释

#定义添加次级部门的函数，参数包括（组织id，上级部门id，部门id,部门名称,添加数量）
def add_sub(org_id,parent_unit,unit_id,unit_name,n):
        for i in range(1,int(n)+1):
                cmd = '/home/coremail/bin/sautil add ou \"org_id=%s&parent_org_unit_id=%s&org_unit_id=%s%d&org_unit_name=%s%d\"'%(org_id,parent_unit+str(1),unit_id,i,unit_name,i)
                os.system(cmd)
                #print 'add org unit a/%s%d success'%(unit,i)    #XT3以下版本请撤销本行注释

#输入非法数据时的一个提示
def tip():
        return int(raw_input('你的输入太任性啦～再给你一次机会:'))


#定义一个部门层级的元组
t = (' ','a','b','c','d','e','f','g','h','i','j')

org = str(raw_input('先输入组织的id(标识)吧［默认组织请输入‘a’］:'))
hier = int(raw_input('添加几级部门啊（别超过10级哟）:'))
while (hier not in range(1,11)):
       hier = tip()

if hier ==1 :
    uid = str(raw_input('命名它们的名字:'))
    num = int(raw_input('总共添加多少个部门啊:'))
    add_primary(org,uid,uid.upper(),str(num))
else:
#先添加一级部门
    print '创建多级部门，脚本自动命名...'
    num = int(raw_input('1级部门要添加几个啊:'))
    while num < 1:
        num = tip()
    add_primary(org,'a','A',str(num))
#再依次添加次级部门
    for h in range(2,hier+1):
            num = int(raw_input('%d级部门要添加几个啊（在%d级部门的%s下添加哟）：'%(h,h-1,t[h-1]+str(1))))
            while num < 1:
                    num = tip()
            add_sub(org,t[h-1],t[h],t[h].upper(),str(num))


print '居然成功了!'