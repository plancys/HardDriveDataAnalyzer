import re

import size


class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.size = 0
        self.sub_directories = []
        self.parent = parent

    # def __init__(self, name, parent=None):
    #     self.__init__(name)

    def __str__(self):
        return self.print_dir(0)

    def print_dir(self, level):
        return '\t' * level + str(self.name) + ", size=" + str(self.size) + "\n" + '\n'.join(
            [x.print_dir(level + 1) for x in self.sub_directories])

    def print_sub_dirs(self):
        return '\n'.join([str(x) for x in self.sub_directories])

    def readable_size(self):
        return size.readable_size(self.size)

    def name_without_path(self):
        return re.split('/', self.name)[-1]

    def path(self):
        return self.name

    def up_path(self):
        k = self.name.rfind("/")
        return self.name[:k]
