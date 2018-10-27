import tkinter
from tkinter import Label, Button, END
from tkinter.tix import Tk, Control, ComboBox
from tkinter.messagebox import showinfo, showwarning, showerror
from functools import partial
from tkinter import filedialog
from tkinter import *

root = Tk()

text = Text(root, width=50, height=40)
text.pack()
text.insert(INSERT, 'I love study')


# 原来的字符串变成'I 插入love study'
mainloop()
