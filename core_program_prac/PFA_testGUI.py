__author__ = 'eacon'

from Tkinter import Button,Tk
from functools import partial

root = Tk()

baseTk = partial(Button,root,bg='blue',fg='white')

bt1 = baseTk(text='Button1')
bt2 = baseTk(text='Button2')
bt3 = baseTk(text='Quit',command=root.quit,bg='red')

bt1.pack()
bt2.pack()
bt3.pack()

root.title('PFA_test!')

root.mainloop()