"""
Module with analysis tools
"""
from logic.model import UNIT_SIZES, Directory, DIRECTORY_STRATEGY
from util import directory_util


def analyze_path(strategy, root_directory_path, filter_data):
    """

    :param strategy: file types / directories
    :param root_directory_path: root of analysis
    :param filter_data: filter criteria
    :return: file types / directories analysed
    """
    if strategy == DIRECTORY_STRATEGY:
        return analyze_directories_in_path(root_directory_path, filter_data)
    else:
        return analyze_file_type_in_path(root_directory_path, filter_data)


def analyze_file_type_in_path(root_directory_path, filter_data):
    """
    :param root_directory: root directory - start of analysis
    :param filter_data: applied filters
    :return: preapre view for files analysis
    """
    root_directory = Directory(root_directory_path)
    result = directory_util.build_filetype_analis(root_directory)
    size = filter_data.minimal_size
    unit = filter_data.size_unit
    filter_lambda = lambda x: x.size > (int(size) * UNIT_SIZES[unit])
    return directory_util.filter_filetypes(filter_lambda, result)


def analyze_directories_in_path(root_directory_path, filter_data):
    """
    :param root_directory_path: root directory - start of analysis
    :param filter_data: applied filters
    :return: properly filtered results from analysis starting from root_directory_path
    """
    root_directory = Directory(root_directory_path)
    directory_util.build_directories_tree(root_directory, 0)
    size = filter_data.minimal_size
    unit = filter_data.size_unit
    filter_lambda = lambda x: x.size > (int(size) * UNIT_SIZES[unit])
    directory_util.filter_structure(filter_lambda, root_directory)
    return root_directory
