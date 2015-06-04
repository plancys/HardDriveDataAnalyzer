from Tkinter import StringVar
import os
from ttk import Treeview, Combobox
import re


def generate_label(directory):
    return re.split('/', directory.name)[-1] + " [" + directory.readable_size() + " ]"


def remove_wrong_characters(text):
    return ''.join([i if ord(i) < 128 else '' for i in text])


class DirectoryTreeView(Treeview):
    def __init__(self, root_view, directory):
        Treeview.__init__(self, root_view)
        self.build_view(directory, self)

    def build_view_deep(self, tree_id, tree, subdirectories):
        for directory in subdirectories:
            directory_name = generate_label(directory)
            current_tree_id = tree.insert(tree_id, 'end', text=directory_name)
            if (directory.sub_directories is not None):
                self.build_view_deep(current_tree_id, tree, directory.sub_directories)

    def build_view(self, directory_root, tree):
        root_view_id = tree.insert('', 0, 'directories', text=directory_root.name)
        self.build_view_deep(root_view_id, tree, directory_root.sub_directories)


class SubdirectoriesCombobox(Combobox):
    def __init__(self, root_view, root_directory):
        self.root_value = StringVar()
        Combobox.__init__(self, root_view, textvariable=self.root_value)
        dirs = next(os.walk(root_directory))[1]
        self['values'] = [remove_wrong_characters(text) for text in dirs]