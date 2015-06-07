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
        lbl = Label(self, text="Disc storage analyzer")
        lbl.grid(sticky=W, pady=4, padx=5)
        strategy = StringVar()
        Label(self, text="Analyze strategy: ").grid(row=1, column=2)
        Radiobutton(self, text='Directories', variable=strategy, value='home').grid(row=1, column=3)
        Radiobutton(self, text='File types', variable=strategy, value='office').grid(row=1, column=4)
        Label(self, text="Root directory: ").grid(row=2, column=2)
        self.combo = widgets.SubdirectoriesCombobox(self, "/")
        self.combo.grid(row=3, column=3, columnspan=2)
        Button(self, text="Analyze", command=self.analyze).grid(row=4, column=2, sticky=N + W)

        start = model.Directory("/Users/kamilkalandyk1/Repositories-Private")
        # start = model.Directory("/bin")
        # start = model.Directory("/Users/kamilkalandyk1/Pictures")
        directory_util.build_directories_tree(start, 0, False)
        self.analis_result = widgets.DirectoryTreeView(self, start)
        self.analis_result.grid(row=1, column=0, columnspan=2, rowspan=4,
                                padx=5, sticky=E + W + S + N)

        directory_util.build_directories_tree(start, 0, False)

        # list.insert(0, "(..) " + start.path())
        # for index, directory in enumerate(start.sub_directories):
        #     list.insert(index + 1, directory.name_without_path())
        self.choose_dir_list = widgets.DirectoryList(self, start)
        self.choose_dir_list.grid(row=3, column=2, columnspan=3, sticky=E + W)

        self.parent.title("Disk storage analyzer")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, pad=7)

    def analyze(self):
        new_dir = model.Directory(self.choose_dir_list.current_path())
        directory_util.build_directories_tree(new_dir, 0)
        self.analis_result = widgets.DirectoryTreeView(self, new_dir)
        self.analis_result.grid(row=1, column=0, columnspan=2, rowspan=4,
                                padx=5, sticky=E + W + S + N)


def main():
    root = Tk()
    root.geometry("800x600+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
