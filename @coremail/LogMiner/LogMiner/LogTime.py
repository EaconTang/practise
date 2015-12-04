"""
deal with log time;
allow more flexible time specified by user
"""
from re import match
from sys import exit
import datetime
from math import fabs

def convert_to_logfiles(time_period,logfile='rmi_api.log'):
    if not match(r'\d{8}:\d{8}',time_period):
        exit('Wrong format for time period!')

    start,end = time_period.split(':')
    start_date = datetime.datetime.strptime(start,'%Y%m%d').date()
    end_date = datetime.datetime.strptime(end,'%Y%m%d').date()

    time_delta = int(fabs(int((end_date - start_date).days))) + 1
    datetime_list = [start_date + datetime.timedelta(i) for i in range(time_delta)]

    datetime_list = map(lambda x:x.strftime('%Y-%m-%d'),datetime_list)
    print datetime_list
    return map(lambda x:'.'.join([logfile,x]),datetime_list)


if __name__ == '__main__':
    print convert_to_logfiles('20151128:20160101')