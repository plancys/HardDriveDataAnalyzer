"""
Module with model for Storage application
"""
import re
import abc

from util import size_util


class StorageObject(object):
    """Abstract class for directory and file"""

    def __init__(self, name):
        self.name = name
        self.size = 0

    def readable_size(self):
        """
        :return: return human readable size of file or directory
        """
        return size_util.readable_size(self.size)

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
