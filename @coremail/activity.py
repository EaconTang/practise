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
    cmd = '/home/coremail/bin/sautil callapi "{cmd:303,attrs:[provider_id,org_id,user_id,activity],filter:[]}]}"'
    status, output = commands.getstatusoutput(cmd)

    if status != 0:
        sys.exit(output)

    return output


def find_provider_id(output):
    return re.findall(r'provider_id: \[WST:(\d+)\]', output)


def find_org_id(output):
    return re.findall(r'org_id: \[WST:(.+)\]', output)


def find_user_id(output):
    return re.findall(r'user_id: \[WST:(.+)\]', output)


def find_history_rate(output):
    return re.findall(r'history_rate: \[INT:(\d+)\]', output)


def find_rate(output):
    return re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}: \[INT:0\]', output)
