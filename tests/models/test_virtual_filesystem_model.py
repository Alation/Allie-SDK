"""Test the Alation REST API Virtual File System Models."""

import unittest
from allie_sdk.models.virtual_filesystem_model import *


class TestVirtualFileSystemeModels(unittest.TestCase):

    def test_virtual_file_system_model_item(self):

        vfs_response = {
            "path": "/docs",
            "name": "readme.md",
            "is_directory": False,
            "size_in_bytes": 988,
            "ts_last_modified": "2024-06-20T18:26:54.663432Z",
            "ts_last_accessed": "2024-06-20T18:26:54.663432Z",
            "owner": "admin",
            "group": "root",
            "permission_bits": 755,
            "storage_type": 0
        }
        vfs = VirtualFileSystemItem.from_api_response(vfs_response)

        vfs_model = VirtualFileSystemItem(
            path="/docs",
            name="readme.md",
            is_directory=False,
            size_in_bytes=988,
            ts_last_modified="2024-06-20T18:26:54.663432Z",
            ts_last_accessed="2024-06-20T18:26:54.663432Z",
            owner="admin",
            group="root",
            permission_bits=755,
            storage_type=0
        )

        self.assertEqual(vfs, vfs_model)


if __name__ == '__main__':
    unittest.main()