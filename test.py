import tkinter
from tkinter import Label, Button, END
from tkinter.tix import Tk, Control, ComboBox
from tkinter.messagebox import showinfo, showwarning, showerror
from functools import partial
from tkinter import filedialog
from tkinter import *
import jieba
import jieba.posseg as pseg
seg_list = jieba.cut("我:来到北京清华大学“这里，有好多-朋友”", cut_all=False)
print("Default Mode: " + "\ ".join(seg_list))

words = pseg.cut("我:来到北京清华大学“这里，有好多-朋友”")
for word, flag in words:
    print("%s %s" % (word, flag))

result = jieba.tokenize("净投放2000亿元农产品多数飘绿，审核门槛在提高，我:来到北京清华大学“这里，有好多-朋友")
for tk in result:
    print("word %s\t\t start:%d\t\t end:%d" % (tk[0],tk[1],tk[2]))