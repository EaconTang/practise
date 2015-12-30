# coding=utf-8
"""

"""
import commands
import sys


def check_queue(user):
    """不断检测user是否进入代收队列；一旦该user进入代收，返回True
    """
    log = 'popweb accounts queued for user: ' % user
    cmd = 'tail /home/coremail/logs/rmi_api.log'
    while 1:
        log_output = commands.getoutput(cmd)
        if log in log_output:
            break
    return True


def jump_queue(user, priority):
    """将某个代收账号user插入代收队列，并指定代收优先级priority
    """
    cmd = '/home/coremail/bin/sautil callapi "{cmd:90,user_at_domain:{0},attrs:{priority:{1}}}"'.format(user, priority)
    status, output = commands.getstatusoutput(cmd)
    if status != 0:
        sys.exit('Failed when execute the system command to jump queue!')


def accoutProcessed_time(user):
    """
    """
    pass


if __name__ == '__main__':
    priorities = ['high', 'normal', 'low', 'background']
    if check_queue('user1@testke.cn'):
        jump_queue('user2@testke.cn', priorities[0])
