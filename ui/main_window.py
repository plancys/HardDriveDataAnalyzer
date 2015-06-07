"""
Module responsible for presenting data (UI)
"""
from Tkinter import Tk, BOTH, W, N, E, S, Radiobutton, StringVar, Button, Spinbox
from ttk import Frame, Label, Combobox

from ui import widgets
from util.size_util import UNIT_SIZES
from util import model
from util import directory_util

FILE_STRATEGY = 'file'
DIRECTORY_STRATEGY = 'directory'


class Application(Frame):  # pylint: disable=too-many-ancestors
    """
        class responsible for glue logic with presenter
    """

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.strategy = StringVar()
        self.minimal_size_var = StringVar()
        self.size_unit_var = StringVar()
        self.init_strategy_panel(self.strategy)
        start = model.Directory("/")
        directory_util.build_directories_tree(start, 0, False)
        # init directory browser
        Label(self, text="Root directory: ").grid(row=2, column=2)
        self.choose_dir_list = widgets.DirectoryList(self, start)
        self.choose_dir_list.grid(row=3, column=2, columnspan=3, sticky=E + W)
        self.init_main_panel(start)
        self.init_filtering_by_size_panel()
        self.configure_main_view()
        Button(self, text="Analyze",
               command=self.start_disk_check).grid(row=7, column=2,
                                                   columnspan=3, sticky=N + W + E)

    def init_filtering_by_size_panel(self):
        """
        :return: init panel for filtering by size settings
        """
        Label(self, text="Filtering options: ").grid(row=4, column=2)
        Label(self, text="Minimal size object: ").grid(row=5, column=2)
        Spinbox(self, from_=0, to=999,
                textvariable=self.minimal_size_var).grid(row=5, column=3)
        combo = Combobox(self, textvariable=self.size_unit_var)
        combo['values'] = UNIT_SIZES.keys()
        combo.current(0)
        combo.grid(row=5, column=4)

    def configure_main_view(self):
        """
        :return: configure analysis result view
        """
        Label(self, text="Disc storage analyzer").grid(
            sticky=W, pady=4, padx=5)
        self.parent.title("Disk storage analyzer")
        self.pack(fill=BOTH, expand=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(5, pad=7)

    def init_main_panel(self, root_directory):
        """
       :return: configure analysis result view
       :param root_directory: root directory
       """
        widgets.DirectoryTreeView(self, root_directory).grid(
            row=1, column=0, columnspan=2, rowspan=10,
            padx=5, sticky=E + W + S + N)

    def init_strategy_panel(self, strategy):
        """
        :param strategy: reference to strategy of analysis
        :return: configure analysis result view
        """
        strategy.set(DIRECTORY_STRATEGY)
        Label(self, text="Analyze strategy: ").grid(row=1, column=2)
        Radiobutton(self, text='Directories',
                    variable=strategy, value=DIRECTORY_STRATEGY).grid(row=1, column=3)
        Radiobutton(self, text='File types',
                    variable=strategy, value=FILE_STRATEGY).grid(row=1, column=4)

    def start_disk_check(self):
        """
        :return: check particular path after clicking analysis button
        """
        print self.minimal_size_var.get()
        new_dir = model.Directory(self.choose_dir_list.current_path())
        if self.strategy.get() == DIRECTORY_STRATEGY:
            self.results_for_directory_strategy(new_dir)
        else:
            self.results_for_file_type_strategy(new_dir)

    def results_for_file_type_strategy(self, root_directory):
        """
        :param root_directory: root directory - start of analysis
        :return: preapre view for files analysis
        """
        result = directory_util.build_filetype_analis(root_directory)
        size = self.minimal_size_var.get()
        unit = self.size_unit_var.get()
        filter_lambda = lambda x: x.size > (int(size) * UNIT_SIZES[unit])
        filtered = directory_util.filter_filetypes(filter_lambda, result)
        self.init_main_panel(filtered)

    def results_for_directory_strategy(self, root_directory):
        """
        :param root_directory: root directory - start of analysis
        :return: prepare view for directory analysis
        """
        directory_util.build_directories_tree(root_directory, 0)
        size = self.minimal_size_var.get()
        unit = self.size_unit_var.get()
        filter_lambda = lambda x: x.size > (int(size) * UNIT_SIZES[unit])
        directory_util.filter_structure(filter_lambda, root_directory)
        self.init_main_panel(root_directory)


def main():
    """

    :return: main loop
    """
    root = Tk()
    root.geometry("800x600+300+300")
    Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()
