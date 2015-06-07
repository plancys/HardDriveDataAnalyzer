"""
Helper module for building directory trees
"""
from collections import defaultdict
import logging
import os

from util.model import Directory, File
from util import size_util


def build_directories_tree(directory, level, compute_size=True):
    """

    :param directory: root directory
    :param level: level of depth
    :param compute_size: decides whether compute size or not
    :return: directory tree in (directory)
    """
    try:
        current_subdirectories = get_subdirectories_list(directory)
        current_files_names = get_files_list(directory)
    except StopIteration:
        logging.error('Unable to process: %s', directory.name)
        return
    add_files_to_directory(current_files_names, directory)
    if 5 <= level or not current_subdirectories:
        if compute_size:
            directory.size = size_util.recursive_directory_size(directory.name)
    else:
        for subdirectory in current_subdirectories:
            process_subdirectory(directory, level, subdirectory, compute_size)


def add_files_to_directory(current_files_names, directory):
    """

    :param current_files_names: list with file names
    :param directory: decorate directory -> add files
    :return: None
    """
    for file_name in current_files_names:
        current_file = File(directory.name + '/' + file_name)
        try:
            current_file.size = os.path.getsize(current_file.name)
            directory.files.append(current_file)
        except OSError:
            logging.error("Unable to check %s file size. %s", current_file.name, OSError)


def get_subdirectories_list(directory):
    """

    :param directory:
    :return: returns subdirectories fo directory
    """
    return next(os.walk(directory.name))[1]


def get_files_list(directory):
    """

    :param directory:
    :return: returns files from directory
    """
    return next(os.walk(directory.name))[2]


def process_subdirectory(directory, level, subdirectory, compute_size=True):
    """

    :param directory: parent directory
    :param level: directory tree current depth level
    :param subdirectory: subdirectory to process
    :param compute_size: decides wheteher to compute sizes or not
    :return:
    """
    parent_directory_name = directory.name
    if not parent_directory_name.endswith('/'):
        parent_directory_name += '/'
    new_directory = Directory(parent_directory_name + subdirectory, directory)
    directory.sub_directories.append(new_directory)
    build_directories_tree(new_directory, level + 1, compute_size)
    directory.size += new_directory.size


def filter_structure(filter_func, root_directory):
    """

    :param filter_func: function which filter directories
    :param root_directory: root directory
    :return: filtered root directory tree
    """
    filtered_subdirectories = [x for x in root_directory.sub_directories if filter_func(x)]
    filtered_files = [x for x in root_directory.files if filter_func(x)]
    root_directory.sub_directories = filtered_subdirectories
    root_directory.files = filtered_files
    for directory in root_directory.sub_directories:
        filter_structure(filter_func, directory)


def filter_filetypes(filter_func, object_types):
    """

    :param filter_func: function to file type filter
    :param object_types: map [extension] -> [file1, file2, ...]
    :return: filtered object_types
    """
    result = defaultdict(list)
    for file_type in object_types:
        filtered = [x for x in object_types[file_type] if filter_func(x)]
        if filtered:
            result[file_type] = filtered
    return result


def build_filetype_analis(root):
    """

    :param root: root directory
    :return: directory tree starting from root
    """
    file_types_map = defaultdict(list)
    for dirpath, _, filenames in os.walk(root.name):
        for file_name in filenames:
            file_path = os.path.join(dirpath, file_name)
            try:
                new_file = File(file_path)
                new_file.size = os.path.getsize(new_file.name)
                if new_file.extension is not None:
                    file_types_map[new_file.extension].append(new_file)
            except OSError:
                logging.debug('Unable to process: %s', file_path)
    return file_types_map
