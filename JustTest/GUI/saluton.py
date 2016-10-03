from Tkinter import *

saluton = Tk()
saluton.geometry("400x200")

label1 = Label(saluton, text="Saluton!")
label1.pack(expand=1)

button1 = Button(saluton, text="Quit", fg="red", command=saluton.quit)
button1.config(fg="red", bg="blue")
button1.pack(expand=1)

button2 = Button(saluton, text="Help")
button2.pack(expand=1)

mainloop()
