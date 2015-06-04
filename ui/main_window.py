#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import Tk, BOTH, W, N, E, S, Radiobutton, StringVar, Button
from ttk import Frame, Label, Style

import widgets
from util import model
from util import directory_util


class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.init_frame()
        lbl = Label(self, text="Disc storage analyzer")
        lbl.grid(sticky=W, pady=4, padx=5)
        self.init_result_view()
        self.init_left_menu()

    def init_left_menu(self):
        strategy = StringVar()
        Label(self, text="Analyze strategy: ").grid(row=1, column=2)
        Radiobutton(self, text='Directories', variable=strategy, value='home').grid(row=1, column=3)
        Radiobutton(self, text='File types', variable=strategy, value='office').grid(row=1, column=4)
        Label(self, text="Root directory: ").grid(row=2, column=2)
        widgets.SubdirectoriesCombobox(self, "/").grid(row=2, column=3, columnspan=2)
        Button(self, text="Analyze").grid(row=3, column=2)

    def init_result_view(self):
        start = model.Directory("/Users/kamilkalandyk1/Pictures")
        directory_util.build_directories_tree(start, 0)
        analis_result = widgets.DirectoryTreeView(self, start)
        analis_result.grid(row=1, column=0, columnspan=2, rowspan=4,
                           padx=5, sticky=E + W + S + N)

    def init_frame(self):
        self.parent.title("Disk storage analyzer")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, pad=7)


def main():
    root = Tk()
    root.geometry("800x600+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
