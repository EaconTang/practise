# coding=utf-8

'''
将你的 QQ 头像（或者微博头像）右上角加上红色的数字，类似于微信未读信息数量那种提示效果。
使用PIL（Python Image Library), PIL.ImageDraw.Draw.text(xy, text, fill=None, font=None, anchor=None)
'''

from PIL import Image, ImageDraw, ImageFont
from random import randint


class ModifyAvatar:
    def __init__(self):
        pass

    #打开文件
    def open(self, filename):
        self.Img = Image.open(filename)

    #设置字体位置
    def setLocate(self, a, b):
        self.Locate = (a, b)

    #设置字体内容
    def setText(self, text=randint(0, 9999)):
        self.Text = str(text)

    #设置字体颜色
    def setColor(self, a, b, c):
        self.Color = (a, b, c)

    #设置字体格式
    def setFont(self, font, size):
        self.Font = ImageFont.truetype(font, size)

    #编辑并保存图片
    def draw_save(self):
        toDraw = ImageDraw.Draw(self.Img)
        toDraw.text(self.Locate, self.Text, self.Color, self.Font)  #核心语句
        self.Img.save('%s.jpg' % self.Text)
        print "Done!"


if __name__ == '__main__':
    m1 = ModifyAvatar()
    m1.open('Scripts4Test.jpg')
    m1.setLocate(10, 10)
    m1.setText()
    m1.setColor(255, 0, 0)
    m1.setFont('Arial.ttf', 35)
    m1.draw_save()


