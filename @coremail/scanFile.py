#coding=utf-8
import os,sys,time

def scanFile(rootDir):
    #递归遍历指定目录下的所有文件名，并将其添加到LIST的文件名大列表中
    for eachFile in os.listdir(rootDir):
        #print eachFile
        LIST.append(eachFile)
        #print LIST
        if os.path.isdir(eachFile):
            path = os.path.join(rootDir,eachFile)
            scanFile(path)

while True:
    LIST = []
    dir = sys.argv[1]	
    scanFile(dir)
    #print LIST

    for eachFileName in LIST:
    #查找该文件名列表中是否含有.mtactx后缀的文件名
        suffix = '.mtactx'
        if suffix in eachFileName:
            RET = '有mtactx文件！'
            break
        else:
            RET = '没有mtactx文件！'
            continue
    print RET

    time.sleep(1)