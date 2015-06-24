"""
Module responsible for presenting data (UI)
"""
from Tkinter import BOTH, W, N, E, S, Radiobutton, StringVar, Button, Spinbox
from ttk import Frame, Label, Combobox

from ui import widgets
from logic.model import FilterCriteria, UNIT_SIZES, DIRECTORY_STRATEGY
from logic.model import FILE_STRATEGY
from logic.anayzer import analyze_path, generate_initial_hierarchy


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
        start = generate_initial_hierarchy("/")
        # init directory browser
        Label(self, text="Root directory: ").grid(row=2, column=2 + 2)
        self.choose_dir_list = widgets.DirectoryList(self, start)
        self.choose_dir_list.grid(row=3, column=2 + 2, columnspan=3, sticky=E + W)

        self.init_main_panel(start)
        self.init_filtering_by_size_panel()
        self.configure_main_view()
        Button(self, text="Analyze",
               command=self.start_disk_check).grid(row=7, column=2 + 2,
                                                   columnspan=3, sticky=N + W + E)

    def init_filtering_by_size_panel(self):
        """
        :return: init panel for filtering by size settings
        """
        Label(self, text="Filtering options: ").grid(row=4, column=2 + 2)
        Label(self, text="Minimal size object: ").grid(row=5, column=2 + 2)
        Spinbox(self, from_=0, to=999,
                textvariable=self.minimal_size_var).grid(row=5, column=3 + 2)
        combo = Combobox(self, textvariable=self.size_unit_var)
        combo['values'] = UNIT_SIZES.keys()
        combo.current(0)
        combo.grid(row=5, column=4 + 2)

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
        result_view = widgets.DirectoryTreeView(self, root_directory)
        result_view.grid(
            row=1, column=0, columnspan=4, rowspan=10, padx=5, sticky=E + W + S + N)

    def init_strategy_panel(self, strategy):
        """
        :param strategy: reference to strategy of analysis
        :return: configure analysis result view
        """
        strategy.set(DIRECTORY_STRATEGY)
        Label(self, text="Analyze strategy: ").grid(row=1, column=2 + 2)
        Radiobutton(self, text='Directories',
                    variable=strategy, value=DIRECTORY_STRATEGY).grid(row=1, column=3 + 2)
        Radiobutton(self, text='File types',
                    variable=strategy, value=FILE_STRATEGY).grid(row=1, column=4 + 2)

    def start_disk_check(self):
        """
        :return: check particular path after clicking analysis button
        """
        filter_criteria = FilterCriteria(
            self.minimal_size_var.get(),
            self.size_unit_var.get()
        )
        analis_path = self.choose_dir_list.current_path()
        result = analyze_path(self.strategy.get(), analis_path, filter_criteria)
        self.init_main_panel(result)
