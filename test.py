import tkinter
from tkinter import Label, Button, END
from tkinter.tix import Tk, Control, ComboBox
from tkinter.messagebox import showinfo, showwarning, showerror
from functools import partial
from tkinter import filedialog
from tkinter import *


L = [1, 2]
M = L
L.append(3)
L[0] = 9
print(L, M)
print("-------------------")
L = [1, 2]
M = L
L += [3, 4]
print(L, M)
