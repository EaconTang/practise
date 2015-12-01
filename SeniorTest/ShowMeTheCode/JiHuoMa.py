#coding=utf-8
'''
0001_生成激活码.py 的copy
做为 Apple Store App 独立开发者，你要搞限时促销，为你的应用生成激活码（或者优惠券），使用 Python 如何生成 200 个激活码（或者优惠券）
'''

import random

def generateRandomCode():
    string_all = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    def randomChar():
        return string_all[random.randint(0,61)]         #利用randint生成随机下标来生成随机码
    n=16
    randomCode = ''
    while(n>0):
        randomCode += randomChar()
        n -= 1
        if(n == 12 or n == 8 or n == 4):
            randomCode += '-'
    return randomCode


if __name__=='__main__':
    n = 200
    while(n>0):
        print generateRandomCode()
        n -= 1