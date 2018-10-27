import tkinter
from tkinter import Label, Button, END
from tkinter import ttk
from tkinter.tix import Tk, Control, ComboBox
from tkinter.messagebox import showinfo, showwarning, showerror
from functools import partial
from tkinter import filedialog
from tkinter import *


class DataAnnotation:

    def __init__(self):
        self.__top = tkinter.Tk()
        root = self.__top
        root.geometry('600x450')
        root.tk.eval('package require Tix')
        root.title("Data Annotation")
        self.__root_path = str(sys.path[0])

        # init a menubar
        self.__menu = Menu(root)
        main_menu = self.__menu
        self.__filemenu = Menu(main_menu, tearoff=FALSE)
        file_menu = self.__filemenu
        file_menu.add_command(label='Open', command=self.openfile_handler)
        self.__news_file = None  # the news text filename
        file_menu.add_command(label='Load', command=self.loadfile_handler)
        self.__data_file = None  # the annotated text filename
        file_menu.add_command(label='Exit', command=self.exit_handler)
        main_menu.add_cascade(label='File', menu=file_menu)

        # init the main window
        # init a news text panedwindow
        self.__textpane = PanedWindow(root, orient=HORIZONTAL, showhandle=FALSE, sashrelief=SUNKEN, width=50)
        text_pane = self.__textpane
        text_pane.pack(fill=BOTH, expand=True)
        self.__scrollbar = Scrollbar(text_pane)
        #self.__text = Text(text_pane, height=30, width=15)
        self.__text = Text(text_pane, width=50)
        text = self.__text
        scrollbar = self.__scrollbar
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.pack(side=LEFT, fill=Y)
        scrollbar.config(command=text.yview)
        text.config(yscrollcommand=scrollbar.set)
        self.__quote = "Please open the news text or load the annotated news text first!\n"
        text.insert(END, self.__quote)
        text_pane.add(text)

        # init a operation panedwindow
        self.__op_pane = PanedWindow(root, orient=VERTICAL, showhandle=FALSE, sashrelief=SUNKEN, width=20)
        op_pane = self.__op_pane
        text_pane.add(op_pane, width=20)
        self.__op_frame = Frame(op_pane, width=20)
        op_frame = self.__op_frame
        self.__add_an_event_button = Button(op_frame, text='add an event', width=15, command=self.add_an_event_handler).pack(side=TOP)
        self.__edit_an_event_button = Button(op_frame, text='edit an event', width=15, command=self.edit_an_event_handler).pack(side=TOP)
        self.__remove_an_event_button = Button(op_frame, text='remove an event', width=15, command=self.remove_an_event_handler).pack(side=TOP)
        op_frame.pack()

        '''
        op_pane.add(self.__add_an_event_button, width=10)
        op_pane.add(self.__edit_an_event_button, width=10)
        op_pane.add(self.__remove_an_event_button, width=10)
        '''

        # init the event list window
        self.__event_list_pane = PanedWindow(root, orient=VERTICAL, showhandle=FALSE, sashrelief=SUNKEN)
        event_list_pane = self.__event_list_pane
        text_pane.add(event_list_pane)
        self.__event_treeview = ttk.Treeview(event_list_pane, columns=['1', '2', '3'], show='headings')
        event_treeview = self.__event_treeview
        event_treeview.column('1', width=100, anchor='center')
        event_treeview.column('2', width=100, anchor='center')
        event_treeview.column('3', width=100, anchor='center')
        event_treeview.heading('1', text='ID')
        event_treeview.heading('2', text='Type')
        event_treeview.heading('3', text='Tips')
        event_treeview.pack(fill=BOTH, expand=True)

        root.config(menu=main_menu)
        root.mainloop()

    def openfile_handler(self):
        self.__news_file = filedialog.askopenfilename(filetypes=[('DATA', '.data')], title='请选择新闻文本')

    def loadfile_handler(self):
        self.__data_file = filedialog.askopenfilename(filetypes=[('XML', '.xml')], title='请选择数据标注文件')

    def exit_handler(self):
        self.__top.quit()

    def add_an_event_handler(self):
        print('add an event!')
        pass

    def edit_an_event_handler(self):
        print('edit an event')
        pass

    def remove_an_event_handler(self):
        print('remove an event')
        pass

    def __call__(self, *args, **kwargs):
        pass


if __name__ == "__main__":
    da = DataAnnotation()
    da()
