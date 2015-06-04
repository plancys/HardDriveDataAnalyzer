import os
import logging


def get_recursive_directory_size_in_bytes(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.path.getsize(fp)
            except OSError:
                logging.debug('Unable to process: %s', fp)
    return total_size


def readable_size(bytes):
    kilobyte = 1000.0
    megabyte = kilobyte * 1024.0
    gigabytes = megabyte * 1024.0
    if bytes > gigabytes:
        return get_formatted_number(bytes, gigabytes, "GB")
    elif bytes > megabyte:
        return get_formatted_number(bytes, megabyte, "MB")
    elif bytes > kilobyte:
        return get_formatted_number(bytes, kilobyte, "KB")
    else:
        return get_formatted_number(bytes, 1, "B")


def get_formatted_number(number, divider, scale):
    return str(format(number / divider, '.2f')) + " " + scale


def print_directory_size(directory):
    size = get_recursive_directory_size_in_bytes(directory)
    return directory, readable_size(size)
