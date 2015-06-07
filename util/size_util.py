"""
Util for files and directories operations
"""
import os
import logging
import operator

UNIT_SIZES = {"B": 1,
              "KB": 1024,
              "MB": 1024 * 1024,
              "GB": 1024 * 1024 * 1024,
              "TB": 1024 * 1024 * 1024 * 1024}


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


def readable_size(size_in_bytes):
    """

    :param size_in_bytes: number of bytes
    :return: well formatted size
    """
    reversed_sorted_unit = sorted(UNIT_SIZES.items(), key=operator.itemgetter(1), reverse=True)
    for (key, value) in reversed_sorted_unit:
        if value < size_in_bytes:
            return get_formatted_size(size_in_bytes, value, key)
    return get_formatted_size(size_in_bytes, 1, "B")


def get_formatted_size(number, unit_divider, unit):
    """

    :param number: size in bytes
    :param unit_divider: unit divider
    :param unit:
    :return: formatted size string
    """
    return str(format(number / unit_divider, '.2f')) + " " + unit
