# coding=utf-8
"""
/home/coremail/bin/sautil callapi "{cmd:303,attrs:activity,filter:[{name:user_id,op:7,val:['u1','u2']}]}"
活跃度计算策略：
1.扫描日志customerbehavior.log，得到各用户在日志中出现的次数statUser.get(uid)；
2.出现次数最高的用户=logMaxCount;
3.每个用户的活跃度：rateVal = statUser.get(uid)/logMaxCount * 100000
4.用户最终活跃度为：(rateValue + historyRate*0.8) /（2 * 100000）;
5.rateVal将值保留在historyRate供下次计算使用；
"""
import commands
import re
import sys


def get_cmd_res():
    cmd = '/home/coremail/bin/sautil callapi "{cmd:303,attrs:[provider_id,org_id,user_id,activity],filter:[],limit:-1}"'
    status, output = commands.getstatusoutput(cmd)

    if status != 0:
        sys.exit(output)

    return output


def find_provider_id(output):
    return re.compile(r'provider_id: \[WST:(\d+)\]').findall(output)[0]


def find_org_id(output):
    return re.compile(r'org_id: \[WST:(.+)\]').findall(output)[0]


def find_user_id(output):
    return re.compile(r'user_id: \[WST:(.+)\]').findall(output)[0]


def find_history_rate(output):
    pattern = re.compile(r'history_rate: \[INT:(\d+)\]')
    history_rate = pattern.findall(output)
    if history_rate:
        return int(history_rate[0])
    return 0


def find_rate(output):
    pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}: \[INT:(\d+)\]')
    rate = pattern.findall(output)
    if rate:
        return int(rate[0])
    return 0


def compute_final_rate(history_rate,rate):
    return float(history_rate*0.8 + rate)/200000


def split_map(output):
    assert isinstance(output, str)
    map_list = output.split('[MAP:(size=4):...]:')
    map_list.pop(0)
    return map_list


def get_tdn(provider,org,user):
    return '/'.join([provider,org,user])


def get_userAtDomain(org,user):
    # specially, default org 'a' for name: dm137.icoremail.net
    if org == 'a':
        org = 'dm137.icoremail.net'
    return '@'.join([user,org])


def compute_inactivity(final_rate_list):
    return [each for each in final_rate_list if each ==0]


def get_all_users_cout():
    cmd = '/home/coremail/bin/userutil --select-user|wc -l'
    output = commands.getoutput(cmd)
    return int(output)


######################
output = get_cmd_res()
map_list = split_map(output)
wright_len = len(map_list)

if len(sys.argv) == 1:
    TOP = 10
elif len(sys.argv) == 2:
    TOP = int(sys.argv[1])
    if not 0 < TOP <= wright_len:
        sys.exit('Wrong args for top numnbers!')
else:
    sys.exit('Wrong arguments!')

provider_id_list = map(find_provider_id,map_list)
assert len(provider_id_list) == wright_len

org_id_list = map(find_org_id,map_list)
assert len(org_id_list) == wright_len

user_id_list = map(find_user_id,map_list)
assert len(user_id_list) == wright_len

# tdn_list = map(get_tdn,provider_id_list,org_id_list,user_id_list)

userAtDomain_list = map(get_userAtDomain,org_id_list,user_id_list)
assert len(userAtDomain_list) == wright_len

history_rate_list = map(find_history_rate,map_list)
rate_list = map(find_rate,map_list)
assert len(history_rate_list) == len(rate_list) == wright_len
final_rate_list = map(compute_final_rate,history_rate_list,rate_list)

# result_list = zip(userAtDomain_list,final_rate_list)
# result_list = zip(userAtDomain_list,final_rate_list,history_rate_list,rate_list)
# sort_result_list = sorted(result_list,key=lambda x:x[1],reverse=True)
result_list = zip(final_rate_list,history_rate_list,rate_list,userAtDomain_list)
result_list.sort(reverse=True)

inactivities = compute_inactivity(final_rate_list)
activities_scale = format((wright_len - len(inactivities))/float(wright_len),'.2%')

# display
if wright_len != get_all_users_cout():
    print get_all_users_cout(),'system users exist!'
print wright_len,'uers are involved!'
print 'About',activities_scale,'activity users(those whose rate is nonzero)!'
print 'For top',TOP,'users:'
for final_rate,history_rate,rate,userAtDomain in result_list[:TOP]:
    print userAtDomain.rjust(40),' : ',str(final_rate).ljust(10),
    print '[ history_rate:',str(history_rate).rjust(6),',','rate:',str(rate).rjust(6),']'




