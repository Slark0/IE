import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import *

# 导入tkinter模块的所有内容

root = Tk()

input = Entry(root)
input.pack(padx=200,pady=200)

input.delete(0, END)    #先清空按照索引
input.insert(0,"请输入内容...")

root.mainloop()





