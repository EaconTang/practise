# coding=utf-8

'''
使用字典
管理用户名和密码的模拟登录系统
'''

db = {}


def showmenu():
    print '''
        Select your choice:
            (N)ew user;
            (O)ld user;
            (Q)uit;
        '''

    while True:
        choice = raw_input().strip()[0].lower()
        if choice not in 'noq':
            print 'Invalid option,try again:'
        else:
            if choice == 'n':
                newuser()
            elif choice == 'o':
                olduser()
            else:
                break


def newuser():
    print 'Creat your new accout:'
    while True:
        name = raw_input("Input your new name:")
        if name in db:
            print 'Name exists!Please try another one:'
        else:
            pw = raw_input("Input your password:")
            db[name] = pw
            print 'New user is saved!Back to homemenu...'
            break
    showmenu()


def olduser():
    while True:
        name = raw_input("Inout your name:")
        if name not in db:
            print 'No such user exists!Please try again:'
        else:
            pw = db[name]
            input_pw = raw_input("Input your password:")
            if input_pw == pw:
                print 'Login success!Welcome back,%s' % name
                break
            else:
                print 'Error password!Please try again:'
    showmenu()


if __name__ == '__main__':
    showmenu()
