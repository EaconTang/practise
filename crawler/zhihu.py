# coding=utf-8
import urllib
import re
import os


# 知乎“发现”网址
url = 'http://www.zhihu.com/explore'

page = urllib.urlopen(url)
psrc = page.read()
print 'reading page...'

#print '-------------------------------------------------------------------------------------'

#获取问题链接的相对路径的正则
rexdurl = r'<a class="question_link" target="_blank" href="(.+)">'
re_xdurl = re.compile(rexdurl)

xdurl_list = re.findall(re_xdurl,psrc)

#获取网页标题的函数，用来命名文件
def title_name(url,num):
        #获取title的正则
        ret = r'<title>\n*(.+)\n*</title>'
        re_t = re.compile(ret)

        html = urllib.urlopen(url)

        try:
                name = re.findall(re_t,html.read())
                return name[0]
        except:
                return num


print '%d个网页即将下载...'%len(xdurl_list)


n=1     #找不到title时，用数字命名文件


for i in xdurl_list:    #下载每个链接的网页

        try:
                #补全为完整链接
                jdurl = 'http://zhihu.com' + i
                fname = title_name(jdurl,n)
                urllib.urlretrieve(jdurl,'zhihu/%s.html'%fname)
                print '第%d个网页:%s 下载完成!'%(n,fname)

        except IOError,eio:
                print eio
                print "第%d个网页下载失败！"%i
        finally:
                n += 1

print '完成！'


try:
        cmd1 = 'sz zhihu/*.html'
        os.system(cmd1)
        cmd2 = 'rm zhihu/*.html'
        os.system(cmd2)
except BaseException,e:
        print e
