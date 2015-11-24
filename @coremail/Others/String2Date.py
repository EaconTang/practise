import datetime,time

strDate1 = '2015-Oct-27 15:28:11'
strDate2 = '2015-Oct-27 15:26:39'

struct_date1 = time.strptime(strDate1,"%Y-%b-%d %H:%M:%S")
struct_date2 = time.strptime(strDate2,"%Y-%b-%d %H:%M:%S")

print struct_date1
print struct_date2

struct_date1 = time.mktime(struct_date1)
struct_date2 = time.mktime(struct_date2)

print struct_date1
print struct_date2

print struct_date2 + struct_date1
print struct_date1 - struct_date2


def stringTimeDeal
