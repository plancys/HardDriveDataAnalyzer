"""
Test model classes
"""
from unittest import TestCase

from logic.model import Directory

__author__ = 'kamilkalandyk1'

PATH = "/User/bin/some_dir"
FILE_NAME = "file"
STORAGE_OBJECT = Directory(PATH + "/" + FILE_NAME)
STORAGE_OBJECT.size = 10


class TestStorageObject(TestCase):
    """
    Test class for Storage object
    """

    def test_name_without_path(self):
        """

        :return: should pass when domain class return valid value
        """
        self.assertEqual(STORAGE_OBJECT.name_without_path(), "file")

    def test_up_path(self):
        """

        :return: should pass when domain class return valid value
        """
        self.assertEqual(STORAGE_OBJECT.up_path(), PATH)

    def test_is_file(self):
        """

        :return: should pass when domain class return valid value
        """
        self.assertFalse(STORAGE_OBJECT.is_file())

    def test_readable_size_in_bytes(self):
        """

        :return: should pass if size formatted correctly
        """
        self.assertEqual(STORAGE_OBJECT.readable_size(), "10.00 B")

    def test_readable_size_in_kilobytes(self):
        """

        :return: should pass if size formatted correctly
        """
        factor = 1000
        STORAGE_OBJECT.size *= factor
        self.assertEqual(STORAGE_OBJECT.readable_size(), "9.00 KB")
        STORAGE_OBJECT.size /= factor

    def test_readable_size_in_megabytes(self):
        """

        :return: should pass if size formatted correctly
        """
        factor = 1000 * 1024
        STORAGE_OBJECT.size *= factor
        self.assertEqual(STORAGE_OBJECT.readable_size(), "9.00 MB")
        STORAGE_OBJECT.size /= factor

    def test_readable_size_in_gigabytes(self):
        """

        :return: should pass if size formatted correctly
        """
        factor = 1000 * 1024 * 1024
        STORAGE_OBJECT.size *= factor
        self.assertEqual(STORAGE_OBJECT.readable_size(), "9.00 GB")
        STORAGE_OBJECT.size /= factor

    def test_readable_size_in_terabytes(self):
        """

        :return: should pass if size formatted correctly
        """
        factor = 1000 * 1024 * 1024 * 1024
        STORAGE_OBJECT.size *= factor
        self.assertEqual(STORAGE_OBJECT.readable_size(), "9.00 TB")
        STORAGE_OBJECT.size /= factor
