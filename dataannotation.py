from tkinter import *
import tkinter
from tkinter import Label, Button, END
from tkinter.tix import Tk, Control, ComboBox
from tkinter.messagebox import showinfo, showwarning, showerror


class DataAnnotation:

    def __init__(self):
        self.top = tkinter.Tk()
        self.top.title("数据标注")
        self.top.geometry('350x350')
        self.top.tk.eval('package require Tix')
        m = PanedWindow(orient=VERTICAL)
        m.pack(fill=BOTH, expand=1)
        top = Label(m, text='top pane')
        m.add(top)
        bottom = Label(m, text='bottom pane')
        m.add(bottom)


    def __call__(self, *args, **kwargs):
        self.top.mainloop()


if __name__ == "__main__":
    da = DataAnnotation()
    da()
