from unittest import TestCase

from logic.model import Directory

__author__ = 'kamilkalandyk1'

path = "/User/bin/some_dir"
file = "file"
storage_object = Directory(path + "/" + file)
storage_object.size = 10


class TestStorageObject(TestCase):
    def test_name_without_path(self):
        self.assertEqual(storage_object.name_without_path(), "file")

    def test_up_path(self):
        self.assertEqual(storage_object.up_path(), path)

    def test_is_file(self):
        self.assertFalse(storage_object.is_file())

    def test_readable_size_in_bytes(self):
        self.assertEqual(storage_object.readable_size(), "10.00 B")

    def test_readable_size_in_kilobytes(self):
        factor = 1000
        storage_object.size *= factor
        self.assertEqual(storage_object.readable_size(), "9.00 KB")
        storage_object.size /= factor

    def test_readable_size_in_megabytes(self):
        factor = 1000 * 1024
        storage_object.size *= factor
        self.assertEqual(storage_object.readable_size(), "9.00 MB")
        storage_object.size /= factor

    def test_readable_size_in_gigabytes(self):
        factor = 1000 * 1024 * 1024
        storage_object.size *= factor
        self.assertEqual(storage_object.readable_size(), "9.00 GB")
        storage_object.size /= factor

    def test_readable_size_in_terabytes(self):
        factor = 1000 * 1024 * 1024 * 1024
        storage_object.size *= factor
        self.assertEqual(storage_object.readable_size(), "9.00 TB")
        storage_object.size /= factor
