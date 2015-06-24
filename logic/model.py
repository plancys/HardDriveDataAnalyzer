"""
Module with model for Storage application
"""
import re
import abc
import operator

UNIT_SIZES = {"B": 1,
              "KB": 1024,
              "MB": 1024 * 1024,
              "GB": 1024 * 1024 * 1024,
              "TB": 1024 * 1024 * 1024 * 1024}

# Strategies
FILE_STRATEGY = 'file'
DIRECTORY_STRATEGY = 'directory'


class StorageObject(object):
    """Abstract class for directory and file"""

    def __init__(self, name):
        self.name = name
        self.size = 0

    def name_without_path(self):
        """

        :return: return name without path
        """
        return re.split('/', self.name)[-1]

    def up_path(self):
        """

        :return: returns parent path
        """
        last_slash = self.name.rfind("/")
        return self.name[:last_slash]

    @abc.abstractmethod
    def is_file(self):
        """

        :return: return whether it is file or not
        """
        return

    def readable_size(self):
        """

        :param size_in_bytes: number of bytes
        :return: well formatted size
        """
        reversed_sorted_unit = sorted(UNIT_SIZES.items(), key=operator.itemgetter(1), reverse=True)
        for (key, value) in reversed_sorted_unit:
            if value < self.size:
                return self.get_formatted_size(value, key)
        return self.get_formatted_size(1, "B")

    def get_formatted_size(self, unit_divider, unit):
        """
        :param number: size in bytes
        :param unit_divider: unit divider
        :param unit:
        :return: formatted size string
        """
        return str(format(self.size / unit_divider, '.2f')) + " " + unit


class Directory(StorageObject):
    """Model class for directory."""

    def __init__(self, name, parent=None):
        StorageObject.__init__(self, name)
        self.sub_directories = []
        self.files = []
        self.parent = parent

    def is_file(self):
        return False


class File(StorageObject):
    """Model class for file."""

    def __init__(self, name, file_size=0):
        StorageObject.__init__(self, name)
        if file_size > 0:
            self.size = file_size
        if "." not in self.name_without_path():
            self.extension = None
        else:
            self.extension = re.split(r'\.', self.name)[-1]

    def is_file(self):
        """

        :return: returns whether it is a file
        """
        return True


class FilterCriteria(object):
    """Model class for filter criterias."""

    def __init__(self, minimal_size=0, size_unit=None):
        self.minimal_size = minimal_size
        self.size_unit = size_unit

    def is_any_filter_apply(self):
        """
        :return: return whether any filter is applied
        """
        return self.minimal_size != 0 and self.size_unit
