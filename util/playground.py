# for dirpath, dirs, files in os.walk("/Users/kamilkalandyk1/Repositories-Private/"):
# print dirpath, ":",dirs
import os

from  size import get_recursive_directory_size_in_bytes


class Directory:
    def __init__(self, name):
        self.name = name
        self.size = 0
        self.subDirs = []

    def setSubDirs(self, subDirs):
        self.subDirs = subDirs

    def __str__(self):
        return self.print_dir(0)

    def print_dir(self, level):
        return '\t' * level + str(self.name) + ", size=" + str(self.size) + "\n" + '\n'.join(
            [x.print_dir(level + 1) for x in self.subDirs])

    def printSubDirs(self):
        return '\n'.join([str(x) for x in self.subDirs])


def build_directories_tree(directory, level):
    if 2 <= level:
        directory.size = get_recursive_directory_size_in_bytes(directory.name)
    else:
        current_subdirectories = next(os.walk(directory.name))[1]
        for subdirectory in current_subdirectories:
            process_subdirectory(directory, level, subdirectory)
        files_in_current_dir = next(os.walk(directory.name))[2]
        for file in files_in_current_dir:
            directory.size += os.path.getsize(directory.name + '/' + file)


def process_subdirectory(directory, level, subdirectory):
    new_directory = Directory(directory.name + "/" + subdirectory)
    directory.subDirs.append(new_directory)
    build_directories_tree(new_directory, level + 1)
    directory.size += new_directory.size


start = Directory("/Users/kamilkalandyk1/Repositories-Private")

build_directories_tree(start, 0)
print start
