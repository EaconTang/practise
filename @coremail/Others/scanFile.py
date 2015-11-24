'''for CM-17375'''
#coding=utf-8
import os,sys,time

def scanFile(rootDir,LIST):
    '''
    traverse filenames under the specific directory, add all to LIST
    if the file is still a directory, then recursively traverse it
    '''
    for eachFile in os.listdir(rootDir):
        #print eachFile
        LIST.append(eachFile)
        #print LIST
        path = os.path.join(rootDir,eachFile)
        if os.path.isdir(path):
            scanFile(path,LIST)


while True:
    LIST = []
    dir = sys.argv[1]	#the directory to be scanned
    scanFile(dir,LIST)
    #print LIST
    for eachFileName in LIST:
    #find if the LIST contains a file named with suffixal ".mtactx"
        suffix = '.mtactx'
        if suffix in eachFileName:
            RET = '有mtactx文件！'
            break
        else:
            RET = '没有mtactx文件！'
            continue

    print RET
    if RET == '有mtactx文件！':
        break
    time.sleep(0.5)