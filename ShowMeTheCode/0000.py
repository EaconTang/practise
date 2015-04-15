#coding=utf-8

'''
将你的 QQ 头像（或者微博头像）右上角加上红色的数字，类似于微信未读信息数量那种提示效果。
使用PIL（Python Image Library), PIL.ImageDraw.Draw.text(xy, text, fill=None, font=None, anchor=None)
'''

from PIL import Image,ImageDraw,ImageFont
from random import randint
'''
def add_avatar(number=str(randint(0,99999)),color=(255,0,0),font='Arial.ttf',size=30):
	try:
		print "haha"
		img = Image.open('test.jpg')
		toDraw = ImageDraw.Draw(img)
		theFont = ImageFont.truetype(font,size)
		toDraw.text((10,10),number,color,theFont)
		img.save('Modified_avatar_%d.jpg'%number)

		img.show()
	except BaseException, e:
		print e

if __name__ == '__main__':
	add_avatar()
'''
original_avatar = 'test.jpg'
saved_avatar = 'new_avatar.png'
windows_font = 'Arial.ttf'
color = (255, 0, 0)

def draw_text(text, fill_color, windows_font):
    try:
        im = Image.open(original_avatar)
        x, y =  im.size
        print "The size of the Image is: "
        print(im.format, im.size, im.mode)
        im.show()
        
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(windows_font, 35)
        draw.text((x-20, 7), text, fill_color, font)
        
        im.save(saved_avatar)
        im.show()

    except:
        print "Unable to load image"

if __name__ == "__main__":
    number = str(raw_input('please input number: '))
    #number = str(4)
    draw_text(number, color, windows_font)