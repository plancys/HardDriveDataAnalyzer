__author__ = 'kamilkalandyk1'
import os

from util import size
from model import Directory


def build_directories_tree(directory, level):
    if 2 <= level:
        directory.size = size.get_recursive_directory_size_in_bytes(directory.name)
    else:
        current_subdirectories = next(os.walk(directory.name))[1]
        for subdirectory in current_subdirectories:
            process_subdirectory(directory, level, subdirectory)


def process_subdirectory(directory, level, subdirectory):
    new_directory = Directory(directory.name + "/" + subdirectory)
    directory.subDirs.append(new_directory)
    build_directories_tree(new_directory, level + 1)
    directory.size += new_directory.size
