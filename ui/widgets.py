from ttk import Treeview
import re


class DirectoryTreeView(Treeview):
    def __init__(self, root_view, directory):
        Treeview.__init__(self, root_view)
        self.build_view(directory, self)

    def build_view_deep(self, tree_id, tree, subdirectories):
        for directory in subdirectories:
            print directory
            directory_name = re.split('/', directory.name)[-1] + " [" + directory.readable_size() + " ]"
            current_tree_id = tree.insert(tree_id, 'end', text=directory_name)
            if (directory.sub_directories is not None):
                self.build_view_deep(current_tree_id, tree, directory.sub_directories)

    def build_view(self, directory_root, tree):
        root_view_id = tree.insert('', 0, 'directories', text=directory_root.name)
        self.build_view_deep(root_view_id, tree, directory_root.sub_directories)
