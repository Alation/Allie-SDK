"""Test the Alation REST API Virtual Data Source Methods."""

import requests_mock
import unittest
from allie_sdk.methods.virtual_filesystem import *

MOCK_VIRTUAL_DATA_SOURCE = AlationVirtualFileSystem(
    access_token='test', session=requests.session(), host='https://test.com'
)


class TestVirtualFileSystem(unittest.TestCase):

    @requests_mock.Mocker()
    def test_success_post_virtual_filesystem(self, m):
        vfs_id = 42
        mock_vfs_1 = VirtualFileSystemItem(path="/", name="var", is_directory=True, size_in_bytes=988,
                                           ts_last_modified="2024-06-20T18:26:54.663432Z",
                                           ts_last_accessed="2024-06-20T18:26:54.663432Z", owner="admin", group="root",
                                           permission_bits=755)
        mock_vfs_2 = VirtualFileSystemItem(path="/var", name="Radek File", is_directory=False, size_in_bytes=99,
                                           ts_last_modified="2024-06-20T18:26:54.663432Z",
                                           ts_last_accessed="2024-06-20T18:26:54.663432Z", owner="admin", group="root",
                                           permission_bits=755, storage_type=0)
        mock_vfs_3 = VirtualFileSystemItem(path="/var", name="File 2", is_directory=False, size_in_bytes=653,
                                           ts_last_modified="2024-06-20T18:26:54.663432Z",
                                           ts_last_accessed="2024-06-20T18:26:54.663432Z", owner="admin", group="root",
                                           permission_bits=755, storage_type=0)
        mock_vfs_list = [mock_vfs_1, mock_vfs_2, mock_vfs_3]

        async_response = {'job': {'id': 14391, 'url': '/api/job/14391/', 'errors_url': '/api/job_error/?job_id=14391'}}

        job_response = {
            "status": "successful",
            "msg": "Job finished in 0.359308 seconds at 2024-06-05 17:25:48.469169+00:00",
            "result": "['Uploaded 3 directories and files.']"
        }

        m.register_uri('POST', f'/api/v1/bulk_metadata/file_upload/{vfs_id}/', json=async_response)
        m.register_uri('GET','/api/v1/bulk_metadata/job/?id=14391', json=job_response)
        async_result = MOCK_VIRTUAL_DATA_SOURCE.post_metadata(fs_id=vfs_id, vfs_objects=mock_vfs_list)

        self.assertFalse(async_result)

    @requests_mock.Mocker()
    def test_failed_post_virtual_filesystem(self, m):
        vfs_id = 42
        mock_vfs_1 = VirtualFileSystemItem(path="/", name="var", is_directory=True, size_in_bytes=988,
                                           ts_last_modified="2024-06-20T18:26:54.663432Z",
                                           ts_last_accessed="2024-06-20T18:26:54.663432Z", owner="admin", group="root",
                                           permission_bits=755)
        mock_vfs_2 = VirtualFileSystemItem(path="/var", name="Radek File", is_directory=False, size_in_bytes=99,
                                           ts_last_modified="2024-06-20T18:26:54.663432Z",
                                           ts_last_accessed="2024-06-20T18:26:54.663432Z", owner="admin", group="root",
                                           permission_bits=755, storage_type=0)

        mock_vfs_list = [mock_vfs_1, mock_vfs_2]

        async_response = {'job': {'id': 14391, 'url': '/api/job/14391/', 'errors_url': '/api/job_error/?job_id=14391'}}

        job_response = {
            "status": "successful",
            "msg": "Job finished in 0.359308 seconds at 2024-06-05 17:25:48.469169+00:00",
            "result": "['Uploaded 3 directories and files.']"
        }

        m.register_uri('POST', f'/api/v1/bulk_metadata/file_upload/{vfs_id}/', json=async_response)
        m.register_uri('GET','/api/v1/bulk_metadata/job/?id=14391', json=job_response)
        async_result = MOCK_VIRTUAL_DATA_SOURCE.post_metadata(fs_id=vfs_id, vfs_objects=mock_vfs_list)

        self.assertFalse(async_result)

if __name__ == '__main__':
    unittest.main()