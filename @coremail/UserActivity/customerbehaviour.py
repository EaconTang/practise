import sys
import commands
import re


def get_cmd_res(date):
    cmd = '/home/coremail/bin/sautil --select-log ajx.t --field="count(*),uid" --group=uid --date=' + date
    status,output = commands.getstatusoutput(cmd)
    if status != 0:
        sys.exit('Send cmd fail!')
    return output


def readMessage(date):
    cmd_readMessage_counts = '/home/coremail/bin/sautil --select-log ajx.t --field="n,uid" --date=' + str(date) + \
                             ' --regex-pattern="readMessage"|wc -l'
    cmd_readMessage_users = '/home/coremail/bin/sautil --select-log ajx.t --field="n,uid" --date=' + str(date) + \
                             ' --regex-pattern="readMessage" --group=uid|wc -l'
    status1,readMessage_counts = commands.getstatusoutput(cmd_readMessage_counts)
    status2,readMessage_users = commands.getstatusoutput(cmd_readMessage_users)
    if status1 != 0 or status2 != 0:
        sys.exit('Send cmd fail!')
    return readMessage_counts,readMessage_users


def user_count(res):
    counts_str = re.compile('count\(\*\)=(\d+)').findall(res)
    counts = map(int,counts_str)
    users = re.compile('uid=(.*)').findall(res)
    assert len(users) == len(counts)
    return sum(counts),len(users),zip(counts,users)


def get_user_count():
    cmd = '/home/coremail/bin/userutil --select-user|wc -l'
    status,output = commands.getstatusoutput(cmd)
    if status != 0:
        sys.exit(status=status)
    return int(output)


#########################
if __name__ == '__main__':
    # check args
    if len(sys.argv) == 1:
        mes = '[Error]:Wrong usage!' \
              '\n' \
              'For example: \n' \
              '\tpython customerbehaviour.py 20151128\n' \
              '\tpython customerbehaviour.py 20151128:20151130 20'
        sys.exit(mes)

    log_date = sys.argv[1]
    if re.match(r'^\d{8}$',log_date) or re.match(r'^\d{8}:\d{8}$',log_date):
        pass
    else:
        sys.exit('[Error]:Error format for date! Correct foramt for example: \n\t20151128\n\t20151128:20160102')

    # all wmsvr calls counts
    res = get_cmd_res(log_date)
    counts_total, users_number, count_user_list = user_count(res)

    # readMessage calls counts
    readMessage_counts,readMessage_users = readMessage(log_date)

    user_all = get_user_count()
    behaviour_rate = format(float(users_number)/user_all,'.2%')
    readMessage_rate = format(float(readMessage_users)/user_all,'.2%')

    # output
    print '########################################'
    print 'Totally',user_all,'users exist until now!'

    print '\nDateTime:',log_date

    print '\nAll customer behaviour(wmsvr call) amount to:',counts_total
    print 'Totally',users_number,'(',behaviour_rate,') users do have behaviours!'

    print '\n[wmsvr.mbox:readMessage] amount to:',readMessage_counts
    print 'Totally',readMessage_users,'(',readMessage_rate,') users do readMessage!'

    # exit unless specify a number to sort TOP users by wmsvr call times
    if len(sys.argv) == 3:
        TOP = int(sys.argv[2])
    else:
        sys.exit()

    if not 0 < TOP <= users_number:
        sys.exit('[Error]:Wrong number for top users! Maybe too lage or to small?')

    # sort_result = sorted(count_user_list)
    count_user_list.sort(reverse=True)

    print '\nFor top',TOP,'users(sort by all behaviours):'
    for count,user in count_user_list[:TOP]:
        print user.rjust(40),' : ',count