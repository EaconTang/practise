#coding=utf-8
'''
将 0001 题生成的 200 个激活码（或者优惠券）保存到 MySQL 关系型数据库中。
MySQL API的使用步骤：connect(host,user,pwd,dbname)->cursor()->cursor.execute(sql)->commit()->close()
'''

import MySQLdb
from Scripts4Test.ShowMeTheCode.JiHuoMa import generateRandomCode      #导入生成激活码的方法

sql1 = 'Create Database DB4CODE'    #创建数据库DB4CODE
sql2 = 'use DB4CODE'
sql3 = 'Create Table Random_Code (id int NOT NULL auto_increment, code varchar(30),PRIMARY KEY(id))'    #创建表Random_Code


try:
    con = MySQLdb.connect("localhost",'root','123')     #连接root用户，密码123
    cur = con.cursor()
    cur.execute(sql1)
    cur.execute(sql2)
    cur.execute(sql3)
    con.commit()
    con.close()

    con2 = MySQLdb.connect("localhost",'root','123','DB4CODE')     #连接该数据库
    cur2 = con2.cursor()

    n=200
    while(n>0):
        code = generateRandomCode()
        cur2.execute("Insert into Random_Code (code) VALUES ('%s')"%code)  #插入200个数据
        n -= 1

    con2.commit()
    con2.close()

except BaseException,e:
    print e

