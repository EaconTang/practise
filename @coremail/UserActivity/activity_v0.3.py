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
import mysql.connector


def get_user_rs(psw='4178591731'):
    """
    :return: result set form DB, [[provider_id,org_id,user_id],...]
    """
    try:
        conn = mysql.connector.connect(user='coremail', password=psw, port=3308, database='cmxt')
        cursor = conn.cursor()
        sql = '''SELECT provider_id,org_id,user_id FROM cm_user_info'''
        cursor.execute(sql)
        rs = cursor.fetchall()
        rs = map(lambda x:[str(each) for each in x],rs)     # convert <unicode> to <str>, <tuple> to <list>
        return rs
    except BaseException, e:
        sys.exit(e.message)


def get_provider_id_list(rs):
    assert isinstance(rs, list)
    # return set([each[0] for each in rs])
    return set(zip(*rs)[0])


def get_org_id_list(rs, provider):
    return set([each[1] for each in rs if each[0] == provider])


def get_user_id_list(rs, provider_id, org_id):
    """
    sorted by default order in database
    """
    return [u for p,o,u in rs if o == org_id and p == provider_id]


def get_users_rate(provider_id, org_id, user_id_list):

    print 'Ready to query rates for users :',user_id_list,' In org: ',org_id,'...\n'

    # cmd's return also sorted by default order in database
    cmd = '/home/coremail/bin/sautil callapi "{cmd:303,attrs:activity,filter:[' \
          '{name:provider_id,op:7,val:%s},' \
          '{name:org_id,op:7,val:%s},' \
          '{name:user_id,op:7,val:%s}' \
          ']}"'%(provider_id, org_id, user_id_list)

    status, output = commands.getstatusoutput(cmd)
    if status != 0:
        print status,
        sys.exit(' Error when sending commands to server!')

    history_rate_list = re.findall(r"history_rate: \[INT:(\d+)\]", output)
    rate_list = re.findall(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}: \[INT:(\d+)\]", output)

    # check return value; if not equal, means NULL value exist(maybe new registered user?)
    if not len(user_id_list) == len(rate_list) == len(history_rate_list):
        print 'Error when batch querying on activity! The length between user_id and rate is not equal!'
        return []

    history_rate_list = map(int, history_rate_list)
    rate_list = map(int, rate_list)

    return rate_list

    # user_rates_list = zip(history_rate_list, rate_list)
    # final_rate_list = map(lambda x: (x[0] * 0.8 + x[1]) / 200000, user_rates_list)
    #
    # return final_rate_list  # one to one with


if __name__ == '__main__':

    TOP = int(sys.argv[1])

    rate_dict = {}
    tdn_rate_list = []
    rs = get_user_rs()
    for provider in get_provider_id_list(rs):
        for org in get_org_id_list(rs, provider):
            user_id_list = get_user_id_list(rs,provider, org)
            final_rate_list = get_users_rate(provider, org, user_id_list)
            tdn_list = map(lambda x: '/'.join([provider, org, x]), user_id_list)
            zipped_list = zip(tdn_list, final_rate_list)
            tdn_rate_list.extend(zipped_list)
            for tdn,rate in zipped_list:
                rate_dict[tdn] = rate

    print rate_dict
    tdn_rate_list_sorted = sorted(tdn_rate_list, key=lambda x: x[1], reverse=True)

    print '\n################################\n'
    print 'TOP ',TOP,' users as follows:\n'
    for tdn, rate in tdn_rate_list_sorted[:TOP]:
        print tdn.ljust(40), ' : ', rate
