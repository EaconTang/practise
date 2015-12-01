import sys
import commands
import re


def get_cmd_res(date):
    cmd = '/home/coremail/bin/sautil --select-log ajx.t --field="count(*),uid" --group=uid --date=' + date
    status,output = commands.getstatusoutput(cmd)
    if status != 0:
        sys.exit('Send cmd fail!')
    return output


def user_count(res):
    counts_str = re.compile('count\(\*\)=(\d+)').findall(res)
    counts = map(int,counts_str)
    users = re.compile('uid=(.*)').findall(res)
    assert len(users) == len(counts)
    return sum(counts),len(users),zip(users,counts)


#########################
if not len(sys.argv) == 3:
    mes = 'Wrong usage!' \
          '\n' \
          'For example: \n' \
          'python customerbehaviour.py 20151128 10\n' \
          'python customerbehaviour.py 20151128:20151130 20' \
    sys.exit(mes)

log_date = sys.argv[1]
if not re.match(r'\d{8}',log_date):
    sys.exit('Error format for date! Correct foramt for example: 20151128')

res = get_cmd_res(log_date)
counts_total, users_number, user_count_list = user_count(res)
sort_result = sorted(user_count_list,key=lambda x:x[1],reverse=True)

TOP = int(sys.argv[2])
if not 0 < TOP <= users_number:
    sys.exit('Wrong number for top users! Maybe too lage or to small?')

print 'Totally',users_number,'users do have behaviours!'
print 'Customer behaviour(wmsvr call) amount to:',counts_total
print 'For top',TOP,'users:'
for user,count in sort_result[:TOP]:
    print user.rjust(40),' : ',count