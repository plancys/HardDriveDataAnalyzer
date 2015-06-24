"""
Util for files and directories operations
"""
import os
import logging


def recursive_directory_size(start_path):
    """

    :param start_path: root directory
    :return: Directory with subdirectories tree
    """
    total_size = 0
    for dirpath, _, filenames in os.walk(start_path):
        for file_name in filenames:
            file_path = os.path.join(dirpath, file_name)
            try:
                total_size += os.path.getsize(file_path)
            except OSError:
                logging.debug('Unable to process: %s', file_path)
    return total_size
