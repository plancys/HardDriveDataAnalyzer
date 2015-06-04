import size


class Directory:
    def __init__(self, name):
        self.name = name
        self.size = 0
        self.sub_directories = []

    def __str__(self):
        return self.print_dir(0)

    def print_dir(self, level):
        return '\t' * level + str(self.name) + ", size=" + str(self.size) + "\n" + '\n'.join(
            [x.print_dir(level + 1) for x in self.sub_directories])

    def print_sub_dirs(self):
        return '\n'.join([str(x) for x in self.sub_directories])

    def readable_size(self):
        return size.readable_size(self.size)
