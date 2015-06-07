from Tkconstants import END
from Tkinter import StringVar, Listbox
import os
from ttk import Treeview, Combobox
import re


def generate_label(storage_object, remove_path=True):
    directory_name = storage_object.name
    if remove_path:
        directory_name = re.split('/', storage_object.name)[-1]
    return directory_name + " -> [ " + storage_object.readable_size() + " ]"


def remove_wrong_characters(text):
    return ''.join([i if ord(i) < 128 else '' for i in text])


class DirectoryTreeView(Treeview):
    def __init__(self, root_view, directory):
        Treeview.__init__(self, root_view)
        self.build_view(directory, self)
        self.tag_configure('oddrow', background='orange')
        self.tag_configure('evenrow', background='purple')

    def build_view_deep(self, tree_id, tree, parent_directory):
        for directory in self.sort_by_size(parent_directory.sub_directories):
            directory_name = generate_label(directory)
            current_tree_id = tree.insert(tree_id, 'end', text=directory_name)
            self.build_view_deep(current_tree_id, tree, directory)

        for file in self.sort_by_size(parent_directory.files):
            file_name = generate_label(file)
            tree.insert(tree_id, 'end', text=file_name, tags = ('oddrow',))

    @staticmethod
    def sort_by_size(subdirectories):
        return sorted(subdirectories, key=lambda x: x.size, reverse=True)

    def build_view(self, directory_root, tree):
        label = generate_label(directory_root, False)
        root_view_id = tree.insert('', 0, 'directories', text=label)
        self.build_view_deep(root_view_id, tree, directory_root)


class SubdirectoriesCombobox(Combobox):
    def __init__(self, root_view, root_directory):
        self.root_value = StringVar()
        Combobox.__init__(self, root_view, textvariable=self.root_value)
        dirs = next(os.walk(root_directory))[1]
        self['values'] = [remove_wrong_characters(text) for text in dirs]
        self.bind("<<ComboboxSelected>>", self.newselection)

    def newselection(self, event):
        self.value_of_combo = self.get()
        print(self.value_of_combo)

    def text(self):
        return self.value_of_combo


class DirectoryList(Listbox):
    def __init__(self, root, directory_root):
        Listbox.__init__(self, root)
        self.bind('<Double-Button-1>', self.go)
        self.directory_root = directory_root
        self.current_dir = directory_root
        self.init_view()

    def init_view(self):
        self.delete(0, END)
        self.insert(0, "(...)  " + self.current_dir.path())
        for index, directory in enumerate(self.current_dir.sub_directories):
            self.insert(index + 1, directory.name_without_path())

    def go(self, event):
        w = event.widget
        index = int(w.curselection()[0])

        value = w.get(index)
        if index == 0:
            if self.current_dir.parent is not None:
                self.current_dir = self.current_dir.parent
                self.init_view()
        else:
            next_dir = next((x for x in self.current_dir.sub_directories if x.name_without_path() == value), None)
            self.current_dir = next_dir
            self.init_view()

    def current_path(self):
        return self.current_dir.name
