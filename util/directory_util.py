import logging

__author__ = 'kamilkalandyk1'
import os

from util import size
from model import Directory


def build_directories_tree(directory, level, compute_size=True):
    try:
        current_subdirectories = next(os.walk(directory.name))[1]
    except StopIteration:
        logging.error('Unable to process: %s', directory.name)
        return
    if 5 <= level or not current_subdirectories:
        if compute_size:
            directory.size = size.get_recursive_directory_size_in_bytes(directory.name)
    else:
        for subdirectory in current_subdirectories:
            process_subdirectory(directory, level, subdirectory, compute_size)


def process_subdirectory(directory, level, subdirectory, compute_size=True):
    parent_directory_name = directory.name
    if not parent_directory_name.endswith('/'):
        parent_directory_name += '/'

    new_directory = Directory(parent_directory_name + subdirectory, directory)
    directory.sub_directories.append(new_directory)
    build_directories_tree(new_directory, level + 1, compute_size)
    directory.size += new_directory.size
