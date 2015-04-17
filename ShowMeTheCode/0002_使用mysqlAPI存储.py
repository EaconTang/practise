#coding=utf-8

import MySQLdb
from JiHuoMa import generateRandomCode


sql1 = 'Create Table Random_Code (id int NOT NULL auto_increment, random_code varchar(30),PRIMARY KEY(id))'
sql2 = 'Insert into RandomCode random_code VALUES %s'

con = MySQLdb.connect("localhost",'root','123','TESTDB')
cur = con.cursor()
try:
    n=200
    while(n>0):
        code = generateRandomCode()
        cur.execute("Insert into RandomCode (random_code) VALUES ('%s')"%code)
        n -= 1
except BaseException,e:
    print e

con.commit()
con.close()
