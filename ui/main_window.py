#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import Tk, BOTH, W, N, E, S, Radiobutton, StringVar, Button, Spinbox
from ttk import Frame, Label, Style, Combobox

from util.size import unit_sizes
import widgets
from util import model
from util import directory_util

xsize = 0
zunit = "B"


class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        lbl = Label(self, text="Disc storage analyzer")
        lbl.grid(sticky=W, pady=4, padx=5)
        self.strategy = StringVar()
        self.init_strategy_panel(self.strategy)

        start = model.Directory("/")
        # start = model.Directory("/Users/kamilkalandyk1/Repositories-Private")
        directory_util.build_directories_tree(start, 0, False)
        self.init_root_directory_panel(start)
        self.init_main_panel(start)

        Button(self, text="Analyze", command=self.analyze).grid(row=10, column=2, sticky=N + W)
        # directory_util.build_directories_tree(start, 0, False)
        Label(self, text="Filtering options: ").grid(row=4, column=2)

        Label(self, text="Minimal size object: ").grid(row=5, column=2)
        self.miminal_size = Spinbox(self, from_=0, to=999)
        self.miminal_size.grid(row=5, column=3)

        self.size_unit = StringVar()
        self.size_combo = Combobox(self, textvariable=self.size_unit)
        self.size_combo['values'] = unit_sizes.keys()
        self.size_combo.current(0)
        # self.size_combo['values'] = ["B", "KB", "MB", "GB", "TB"]
        self.size_combo.grid(row=5, column=4)

        self.configure_main_view()

    def configure_main_view(self):
        self.parent.title("Disk storage analyzer")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(3, weight=1)
        # self.columnconfigure(3, pad=7)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(5, pad=7)

    def init_main_panel(self, start):
        self.analis_result = widgets.DirectoryTreeView(self, start)
        self.analis_result.grid(row=1, column=0, columnspan=2, rowspan=10,
                                padx=5, sticky=E + W + S + N)

    def init_root_directory_panel(self, start_directory):
        Label(self, text="Root directory: ").grid(row=2, column=2)
        self.choose_dir_list = widgets.DirectoryList(self, start_directory)
        self.choose_dir_list.grid(row=3, column=2, columnspan=3, sticky=E + W)

    def init_strategy_panel(self, strategy):
        Label(self, text="Analyze strategy: ").grid(row=1, column=2)
        Radiobutton(self, text='Directories', variable=strategy, value='home').grid(row=1, column=3)
        Radiobutton(self, text='File types', variable=strategy, value='office').grid(row=1, column=4)

    def analyze(self):
        new_dir = model.Directory(self.choose_dir_list.current_path())
        directory_util.build_directories_tree(new_dir, 0)
        size = self.miminal_size.get()
        unit = self.size_unit.get()
        print size, unit
        directory_util.filter_structure(lambda x: x.size > (int(size) * unit_sizes[unit]), new_dir)
        self.init_main_panel(new_dir)


def main():
    root = Tk()
    root.geometry("800x600+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
