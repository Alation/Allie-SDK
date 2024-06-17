"""Test the Alation REST API Virtual Data Source Methods."""

import requests_mock
import unittest
from allie_sdk.methods.virtual_datasource import *

MOCK_VIRTUAL_DATA_SOURCE = AlationVirtualDataSource(
    access_token='test', session=requests.session(), host='https://test.com'
)


class TestVirtualDataSource(unittest.TestCase):

    @requests_mock.Mocker()
    def test_success_post_virtual_datasource_no_query_params(self, m):

        vds_id = 99
        mock_vds_1 = VirtualDataSourceSchema()
        mock_vds_1.key = "99.TestSchema"
        mock_vds_1.title = 'Testing Schema'
        mock_vds_1.description = 'Testing the API'

        mock_vds_2 = VirtualDataSourceTable()
        mock_vds_2.key = '99.TestSchema.TestTable'
        mock_vds_2.title = 'Testing Table'
        mock_vds_2.description = 'Testing Table'
        mock_vds_2.definition_sql = 'select * from TestTable1'
        mock_vds_2.data_location = ""

        mock_vds_3 = VirtualDataSourceColumn()
        mock_vds_3.key = "99.TestSchema.TestTable.Column1"
        mock_vds_3.title = 'Testing Column'
        mock_vds_3.description = 'Testing Column'

        mock_vds_4 = VirtualDataSourceIndex()
        mock_vds_4.key = '99.TestSchema.TestTable.index'
        mock_vds_4.index_type = "PRIMARY"
        mock_vds_4.title = 'Testing Index'
        mock_vds_4.description = 'Testing Index'
        mock_vds_4.column_names = ["Column1"]

        mock_vds_list = [mock_vds_1, mock_vds_2, mock_vds_3, mock_vds_4]

        async_response = {
            "job_name": "MetadataExtraction2336_Virtual_9999"
        }
        job_response = {
            "status": "successful",
            "msg": "Job finished in 1.0 seconds at 2024-06-05 17:25:48.469169+00:00",
            "result": "{\"number_received\": 4, \"updated_objects\": 0, \"error_objects\": [], \"error\": null}"
        }

        m.register_uri('POST', f'/api/v1/bulk_metadata/extraction/{vds_id}', json=async_response)
        m.register_uri('GET','/api/v1/bulk_metadata/job/?name=MetadataExtraction2336_Virtual_9999', json=job_response)
        async_result = MOCK_VIRTUAL_DATA_SOURCE.post_metadata(ds_id=vds_id, vds_objects=mock_vds_list)

        self.assertFalse(async_result)

    @requests_mock.Mocker()
    def test_success_failed_post_virtual_datasource_no_query_params(self, m):

        vds_id = 99
        mock_vds_1 = VirtualDataSourceSchema()
        mock_vds_1.key = "99.TestSchema"
        mock_vds_1.title = 'Testing Schema'
        mock_vds_1.description = 'Testing the API'

        mock_vds_2 = VirtualDataSourceTable()
        mock_vds_2.key = '99.TestSchema.TestTable'
        mock_vds_2.title = 'Testing Table'
        mock_vds_2.description = 'Testing Table'
        mock_vds_2.definition_sql = 'select * from TestTable1'
        mock_vds_2.data_location = ""

        mock_vds_4 = VirtualDataSourceIndex()
        mock_vds_4.key = '99.TestSchema.TestTable.index'
        mock_vds_4.index_type = "PRIMARY"
        mock_vds_4.title = 'Testing Index'
        mock_vds_4.description = 'Testing Index'
        mock_vds_4.column_names = ["Column1"]

        mock_vds_list = [mock_vds_1, mock_vds_2, mock_vds_4]

        async_response = {
            "job_name": "MetadataExtraction2336_Virtual_9999"
        }
        job_response = {
            "status": "successful",
            "msg": "Job finished in 1.0 seconds at 2024-06-05 17:25:48.469169+00:00",
            "result": "{\"number_received\": 4, \"updated_objects\": 0, \"error_objects\": "
                      "[\"Line 0. Key: 99.TestSchema.TestTable.index. Missing table \\\"TestTable\\\" "
                      "for index \\\"index\\\". Make sure that table data uploaded/mentioned before index data\"], "
                      "\"error\": \"1 errors were ignored\"}"
        }

        m.register_uri('POST', f'/api/v1/bulk_metadata/extraction/{vds_id}', json=async_response)
        m.register_uri('GET','/api/v1/bulk_metadata/job/?name=MetadataExtraction2336_Virtual_9999', json=job_response)
        async_result = MOCK_VIRTUAL_DATA_SOURCE.post_metadata(ds_id=vds_id, vds_objects=mock_vds_list)

        self.assertFalse(async_result)

    @requests_mock.Mocker()
    def test_success_post_virtual_datasource_with_query_params(self, m):
        vds_id = 99
        mock_vds_1 = VirtualDataSourceSchema()
        mock_vds_1.key = "99.TestSchema"
        mock_vds_1.title = 'Testing Schema'
        mock_vds_1.description = 'Testing the API'

        mock_vds_2 = VirtualDataSourceTable()
        mock_vds_2.key = '99.TestSchema.TestTable'
        mock_vds_2.title = 'Testing Table'
        mock_vds_2.description = 'Testing Table'
        mock_vds_2.definition_sql = 'select * from TestTable1'
        mock_vds_2.data_location = ""

        mock_vds_3 = VirtualDataSourceColumn()
        mock_vds_3.key = "99.TestSchema.TestTable.Column1"
        mock_vds_3.title = 'Testing Column'
        mock_vds_3.description = 'Testing Column'

        mock_vds_4 = VirtualDataSourceIndex()
        mock_vds_4.key = '99.TestSchema.TestTable.index'
        mock_vds_4.index_type = "PRIMARY"
        mock_vds_4.title = 'Testing Index'
        mock_vds_4.description = 'Testing Index'
        mock_vds_4.column_names = ["Column1"]

        mock_vds_list = [mock_vds_1, mock_vds_2, mock_vds_3, mock_vds_4]

        mock_params = VirtualDataSourceParams()
        mock_params.set_title_descs = "true"
        mock_params.remove_not_seen = "false"

        async_response = {
            "job_name": "MetadataExtraction2336_Virtual_9999"
        }
        job_response = {
            "status": "successful",
            "msg": "Job finished in 1.0 seconds at 2024-06-05 17:25:48.469169+00:00",
            "result": "{\"number_received\": 4, \"updated_objects\": 0, \"error_objects\": [], \"error\": null}"
        }

        m.register_uri('POST', '/api/v1/bulk_metadata/extraction/99?set_title_descs=true&remove_not_seen=false',
                       json=async_response)
        m.register_uri('GET','/api/v1/bulk_metadata/job/?name=MetadataExtraction2336_Virtual_9999', json=job_response)
        async_result = MOCK_VIRTUAL_DATA_SOURCE.post_metadata(ds_id=vds_id,
                                                              vds_objects=mock_vds_list,
                                                              query_params=mock_params)

        self.assertFalse(async_result)

if __name__ == '__main__':
    unittest.main()
