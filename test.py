import tkinter
from tkinter import Label, Button, END
from tkinter.tix import Tk, Control, ComboBox
from tkinter.messagebox import showinfo, showwarning, showerror
from functools import partial
from tkinter import filedialog
from tkinter import *
import jieba
import jieba.posseg as pseg
from timeit import timeit
'''
seg_list = jieba.cut("我:来到北京清华大学“这里，有好多-朋友”", cut_all=False)
print("Default Mode: " + "\ ".join(seg_list))

words = pseg.cut("我:来到北京清华大学“这里，有好多-朋友”")
for word, flag in words:
    print("%s %s" % (word, flag))

result = jieba.tokenize("净投放2000亿元农产品多数飘绿，审核门槛在提高，我:来到北京清华大学“这里，有好多-朋友")
for tk in result:
    print("word %s\t\t start:%d\t\t end:%d" % (tk[0],tk[1],tk[2]))
'''


def find(string, text):
    if string.find(text) > -1:
        pass


def re_find(string, text):
    if re.match(text, string):
        pass


def best_find(string, text):
    if text in string:
        pass

#re.search('www', 'www.runoobk.com').span()
print(timeit("find(string, text)", "from __main__ import find; string='lookforme'; text='look'"))
print(timeit("re_find(string, text)", "from __main__ import re_find; string='lookforme'; text='look'"))
print(timeit("best_find(string, text)", "from __main__ import best_find; string='lookforme'; text='look'"))


text = "标普500指数上涨1.2% 能源股集体表现强劲0.1124元/吨"
start = text.find('500指数上涨1.2% 能')
end = start + len('500指数上涨1.2% 能')

print(str(start) + '-' + str(end))