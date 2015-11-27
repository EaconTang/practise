#coding=utf-8
import commands
import re
import sys
from multiprocessing import Pool
import gevent

# cmd_get_activity = ""
# /sautil userinfo --ud-keys=activity --diag tyk1@dm137.icoremail.net
# /userutil --get-user-attr ceshizhy2015@139.com "activity"
# a = os.popen("./sautil userinfo --ud-keys=activity --diag tyk1@dm137.icoremail.net").readlines()[-1].strip()
# (status,out) = commands.getstatusoutput("./sautil userinfo --ud-keys=activity --diag tyk1@dm137.icoremail.net")

def get_user_list():
    status,out = commands.getstatusoutput("/home/coremail/bin/userutil --select-user")
    if status != 0:
        sys.exit('Unable to export the user list!')
    else:
        return out.split('\n')

def get_rates(userAtDomain):
    '''
    :param userAtDomain:
    :return:
    '''
    cmd = "/home/coremail/bin/sautil userinfo --ud-keys=activity --diag {0}".format(userAtDomain)
    (status,output) = commands.getstatusoutput(cmd)

    if status != 0:
        print 'Error!',output
        return

    pattern = r".*activity : {history_rate=(\d+), rate={.*=(\d+)}}.*"
    reg = re.compile(pattern,re.S)
    m = reg.match(output)

    history_rate = 0
    rate = 0
    if m:
       history_rate = int(m.group(1))
       rate = int(m.group(2))

    return (history_rate,rate)

def current_rate(user):
    rates = get_rates(user)
    return rates[1]

def history_rate(user):
    rates = get_rates(user)
    return rates[0]

def save_rate(user,save_dict):
    assert isinstance(save_dict,dict)
    print '查询用户：',user,'...'
    save_dict.__setitem__(user,current_rate(user))

if __name__ == '__main__':
    # main flow
    TOP = int(sys.argv[1])

    print '从UD获取用户列表...'
    user_list = get_user_list()
    rate_dict = {}
    print '获取成功！全站用户数：',len(user_list)
    print '开始查询活跃度...'

    greenlet_list = []
    for each_user in user_list:
        greenlet_list.append(gevent.spawn(save_rate,each_user,rate_dict))
    gevent.joinall(greenlet_list)

    print len(rate_dict)
    user_sortBy_rate = sorted(rate_dict.iteritems(),key=lambda x:x[1],reverse=True)
    print '查询完毕！活跃度最高的前',TOP,'位用户如下：'
    for each in user_sortBy_rate[:TOP]:
        print '【用户】',each[0],' : ',
        print '【活跃度】',each[1]
