import logging
import os

from util import size
from model import Directory, File


def build_directories_tree(directory, level, compute_size=True):
    try:
        current_subdirectories = get_subdirectories_list(directory)
        current_files_names = get_files_list(directory)
    except StopIteration:
        logging.error('Unable to process: %s', directory.name)
        return
    add_files_to_directory(current_files_names, directory)
    if 5 <= level or not current_subdirectories:
        if compute_size:
            directory.size = size.get_recursive_directory_size_in_bytes(directory.name)
    else:
        for subdirectory in current_subdirectories:
            process_subdirectory(directory, level, subdirectory, compute_size)


def add_files_to_directory(current_files_names, directory):
    for file_name in current_files_names:
        current_file = File(directory.name + '/' + file_name)
        try:
            current_file.size = os.path.getsize(current_file.name)
            directory.files.append(current_file)
        except OSError:
            logging.error("Unable to check %s file size. %s", current_file.name, OSError)


def get_subdirectories_list(directory):
    return next(os.walk(directory.name))[1]


def get_files_list(directory):
    return next(os.walk(directory.name))[2]


def process_subdirectory(directory, level, subdirectory, compute_size=True):
    parent_directory_name = directory.name
    if not parent_directory_name.endswith('/'):
        parent_directory_name += '/'
    new_directory = Directory(parent_directory_name + subdirectory, directory)
    directory.sub_directories.append(new_directory)
    build_directories_tree(new_directory, level + 1, compute_size)
    directory.size += new_directory.size


def filter_structure(filter_func, root_directory):
    filtered_subdirectories = [x for x in root_directory.sub_directories if filter_func(x)]
    filtered_files = [x for x in root_directory.files if filter_func(x)]
    root_directory.sub_directories = filtered_subdirectories
    root_directory.files = filtered_files
    for directory in root_directory.sub_directories:
        filter_structure(filter_func, directory)
