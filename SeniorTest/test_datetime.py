import datetime

datetime1 = datetime.datetime.strptime('20151101','%Y%m%d')
datetime2 =  datetime.datetime.strptime('20160110','%Y%m%d')

timedelta = datetime2.date() - datetime1.date()
print timedelta.days

for i in range(timedelta.days):
    print datetime1 + datetime.timedelta(i)