"""
Custom widgets module
"""
from Tkconstants import END
from Tkinter import Listbox
from ttk import Treeview
import re

from util.directory_util import get_subdirectories_list
from logic.model import Directory


def generate_label(storage_object, remove_path=True):
    """

    :param storage_object:  file or directory
    :param remove_path: write with path or not
    :return: well formatted string with file/directory label
    """
    directory_name = storage_object.name
    if remove_path:
        directory_name = re.split('/', storage_object.name)[-1]
    return directory_name + " -> [ " + storage_object.readable_size() + " ]"


def remove_wrong_characters(text):
    """

    :param text: file/directory name
    :return: remove non-ascii characters
    """
    return ''.join([i if ord(i) < 128 else '' for i in text])


class DirectoryTreeView(Treeview):  # pylint: disable=too-many-ancestors
    """
    widgets for main view - Tree view with files and directories
    """

    def __init__(self, root_view, root_model):
        Treeview.__init__(self, root_view)
        if isinstance(root_model, Directory):
            self.build_view(root_model)
            self.tag_configure('oddrow', background='orange')
            self.tag_configure('evenrow', background='purple')
        else:
            self.build_view_for_file_types(root_model)

    def build_view_deep(self, tree_id, directory):
        """

        :param tree_id: parent tree view item id
        :param directory:
        :return: start tree view initialisation
        """
        for directory in self.sort_by_size(directory.sub_directories):
            directory_name = generate_label(directory)
            current_tree_id = self.insert(tree_id, 'end', text=directory_name)
            self.build_view_deep(current_tree_id, directory)

        for file_name in self.sort_by_size(directory.files):
            file_name = generate_label(file_name)
            self.insert(tree_id, 'end', text=file_name, tags=('oddrow',))

    @staticmethod
    def sort_by_size(subdirectories):
        """
        :param subdirectories:
        :return: subdirectories sorted by size
        """
        return sorted(subdirectories, key=lambda x: x.size, reverse=True)

    def build_view(self, directory_root):
        """

        :param directory_root:
        :return: build view in self
        """
        label = generate_label(directory_root, False)
        root_view_id = self.insert('', 0, 'directories', text=label)
        self.build_view_deep(root_view_id, directory_root)

    def build_view_for_file_types(self, files_per_file_type):
        """

        :param files_per_file_type: file types map
        :return: build file type view
        """
        root_view_id = self.insert('', 0, 'files', text="File types")
        for filetype in files_per_file_type:
            type_view_id = self.insert(root_view_id, 'end', text=filetype)
            for file_name in files_per_file_type[filetype]:
                file_name_label = file_name.name + ' ' + file_name.readable_size()
                self.insert(type_view_id, 'end', text=file_name_label)


class DirectoryList(Listbox):  # pylint: disable=too-many-ancestors
    """
    Directory list with enter end exit directories feature
    """

    def __init__(self, root, directory_root):
        Listbox.__init__(self, root)
        self.bind('<Double-Button-1>', self.go_to_directory)
        self.directory_root = directory_root
        self.current_dir = directory_root
        self.init_view()

    def init_view(self):
        """

        :return: init view
        """
        self.delete(0, END)
        self.insert(0, "(...)  " + self.current_dir.name)
        subdirectories = self.current_dir.sub_directories
        self.refresh_subdirectories(subdirectories)
        for index, directory in enumerate(subdirectories):
            self.insert(index + 1, directory.name_without_path())

    def refresh_subdirectories(self, subdirectories):
        """

        :param subdirectories: current subdirectories
        :return: decorated subdirectories - added subdirectories if any exist
        """
        actual_subdirectories_names = get_subdirectories_list(self.current_dir)
        if not subdirectories and actual_subdirectories_names:
            # subdirectories = actual_subdirectories_names
            for subdirectory_name in actual_subdirectories_names:
                new_directory = Directory(self.current_dir.name + "/" + subdirectory_name)
                new_directory.parent = self.current_dir
                subdirectories.append(new_directory)
            self.current_dir.sub_directories = subdirectories

    def go_to_directory(self, event):
        """
        :param event:
        :return: after double click goes to double clicked directory

        """
        widget = event.widget
        index = int(widget.curselection()[0])

        value = widget.get(index)
        if index == 0:
            # go to upstream directory
            if self.current_dir.parent is not None:
                self.current_dir = self.current_dir.parent
                self.init_view()
        else:
            current_directory = (x for x in self.current_dir.sub_directories
                                 if x.name_without_path() == value)
            next_dir = next(current_directory, None)
            self.current_dir = next_dir
            self.init_view()

    def current_path(self):
        """

        :return: current path on this widget
        """
        return self.current_dir.name
