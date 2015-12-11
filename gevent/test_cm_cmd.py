import gevent
import commands


def get_all_user(fail_dict,task_id):
    cmd = '/home/coremail/bin/userutil --select-user'
    status,output = commands.getstatusoutput(cmd)
    if status != 0:
        assert isinstance(fail_dict,dict)
        fail_info = [status,output]
        fail_dict.__setitem__(task_id,fail_info)
        print 'task',task_id,'finished abortively!'
        return
    print 'task',task_id,'finished successfully!'
    return


fail_dict = {}
tasks = [gevent.spawn(get_all_user,(fail_dict,i,)) for i in xrange(10)]
gevent.joinall(tasks)

print fail_dict