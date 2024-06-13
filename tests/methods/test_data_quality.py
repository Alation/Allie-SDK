"""Test the Alation REST API Data Quality Methods"""

import requests_mock
import unittest
from allie_sdk.methods.data_quality import *

MOCK_DQ = AlationDataQuality(
    access_token='test', session=requests.session(), host='https://test.com'
)


class TestDataQuality(unittest.TestCase):

    @requests_mock.Mocker()
    def test_success_get_data_quality_fields(self, m):

        mock_params = DataQualityFieldParams()
        mock_params.key.add('1.DQ.Test')
        success_response = [
            {
                "key": "1.DQ.Test",
                "name": "Possibly Deleted",
                "description": "Test DQ Field",
                "type": "VARCHAR",
                "ts_created": "2023-07-07T23:30:20.654601Z"
            }
        ]
        success_dq_fields = [DataQualityField.from_api_response(item) for item in success_response]
        m.register_uri('GET', '/integration/v1/data_quality/fields/?key=1.DQ.Test',
                       json=success_response)
        dq_fields = MOCK_DQ.get_data_quality_fields(mock_params)

        self.assertEqual(success_dq_fields, dq_fields)

    @requests_mock.Mocker()
    def test_failed_get_data_quality_fields(self, m):

        failed_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }
        m.register_uri('GET', '/integration/v1/data_quality/fields/', json=failed_response,
                       status_code=403)
        dq_fields = MOCK_DQ.get_data_quality_fields()

        self.assertIsNone(dq_fields)

    @requests_mock.Mocker()
    def test_success_post_data_quality_field(self, m):

        dq_field = DataQualityFieldItem()
        dq_field.field_key = '1.Test.DataQuality'
        dq_field.name = 'Test'
        dq_field.type = 'String'
        dq_field_list = [dq_field]

        async_response = {
            "job_id": 1,
            "href": "/api/v1/bulk_metadata/job/?id=813"
        }
        job_response = {
            "status": "successful",
            "msg": "Job finished in 0.082328 seconds at 2023-11-30 16:52:52.720461+00:00",
            "result": {
                "fields": {
                    "created": {"count": 1, "sample": [{"field_key": "human_name_string_2"}]},
                    "updated": {"count": 0, "sample": []}
                },
                "values": {
                    "created": { "count": 0,"sample": []},
                    "updated": {"count": 0, "sample": []}
                },
                "created_object_attribution": {
                    "success_count": 0, "failure_count": 0,
                    "success_sample": [], "failure_sample": []
                },
                "flag_counts": {"GOOD": 0, "WARNING": 0, "ALERT": 0},
                "total_duration": 0.08337326161563396
            }
        }

        m.register_uri('POST', '/integration/v1/data_quality/', json=async_response)
        m.register_uri('GET', '/api/v1/bulk_metadata/job/?id=1', json=job_response)
        async_result = MOCK_DQ.post_data_quality_fields(dq_field_list)

        self.assertTrue(async_result)

    @requests_mock.Mocker()
    def test_failed_post_data_quality_fields(self, m):

        dq_field = DataQualityFieldItem()
        dq_field.field_key = '1.Test.DataQuality'
        dq_field.name = 'Test'
        dq_field.type = 'String'
        dq_field_list = [dq_field]
        failed_response = {
            "Entry": 1,
            "Message": "field_key is required"
        }
        m.register_uri('POST', '/integration/v1/data_quality/',
                       json=failed_response, status_code=400)
        async_result = MOCK_DQ.post_data_quality_fields(dq_field_list)

        self.assertFalse(async_result)

    @requests_mock.Mocker()
    def test_success_delete_data_quality_fields(self, m):

        dq_field = DataQualityField()
        dq_field.key = '1.Test.DataQuality'
        dq_field_list = [dq_field]

        async_response = {
            "job_id": 1,
            "href": "/api/v1/bulk_metadata/job/?id=814"
        }
        job_response = {
            "status": "successful",
            "msg": "Job finished in 0.10362 seconds at 2023-11-30 17:08:47.859401+00:00",
            "result": {
                "fields": {
                    "deleted": {"count": 1, "sample": [{"field_key": "human_name_string_2"}]},
                    "not_found": {"count": 1, "sample": [{"field_key": "human_name_string"}]}},
                "values": {
                    "deleted": {"count": 0, "sample": []},
                    "not_found": {"count": 0, "sample": []}
                },
                "total_duration": 0.10439563915133476
            }
        }
        m.register_uri('DELETE', '/integration/v1/data_quality/', json=async_response)
        m.register_uri('GET', '/api/v1/bulk_metadata/job/?id=1', json=job_response)
        async_result = MOCK_DQ.delete_data_quality_fields(dq_field_list)

        self.assertTrue(async_result)

    @requests_mock.Mocker()
    def test_failed_delete_data_quality_fields(self, m):

        dq_field = DataQualityField()
        dq_field.key = '1.Test.DataQuality'
        dq_field_list = [dq_field]
        failed_response = {
            "Entry": -1,
            "Message": "A \"values\" or \"fields\" property must be specified"
        }
        m.register_uri('DELETE', '/integration/v1/data_quality/',
                       json=failed_response, status_code=400)
        async_result = MOCK_DQ.delete_data_quality_fields(dq_field_list)

        self.assertFalse(async_result)

    @requests_mock.Mocker()
    def test_success_get_data_quality_values(self, m):

        mock_params = DataQualityValueParams()
        mock_params.field_key.add("1.DQ.Test")
        success_response = [
            {
                "object_key": "1.superstore.public.superstore_reporting.product_name",
                "object_name": "product_name",
                "otype": "attribute",
                "oid": 84,
                "source_object_key": "1.superstore.public.superstore_reporting.product_name",
                "source_object_name": "product_name",
                "source_otype": "attribute",
                "source_oid": 84,
                "value_id": 174,
                "value_value": "Pass Rate: 81.5655%",
                "value_quality": "ALERT",
                "value_last_updated": "2023-08-31T19:12:26.093295Z",
                "value_external_url": None,
                "field_key": "1.DQ.Test",
                "field_name": "COL_GOLD",
                "field_description": None
            }
        ]
        success_dq_values = [DataQualityValue.from_api_response(item) for item in success_response]
        m.register_uri('GET', '/integration/v1/data_quality/values/?field_key=1.DQ.Test',
                       json=success_response)
        dq_values = MOCK_DQ.get_data_quality_values(mock_params)

        self.assertEqual(success_dq_values, dq_values)

    @requests_mock.Mocker()
    def test_failed_get_data_quality_values(self, m):

        failed_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }
        m.register_uri('GET', '/integration/v1/data_quality/values/', json=failed_response,
                       status_code=403)
        dq_values = MOCK_DQ.get_data_quality_values()

        self.assertIsNone(dq_values)

    @requests_mock.Mocker()
    def test_success_post_data_quality_values(self, m):

        dq_value = DataQualityValueItem()
        dq_value.field_key = '1.DQ.Test'
        dq_value.object_key = '1.Test.Table'
        dq_value.object_type = 'Table'
        dq_value.status = 'WARNING'
        dq_value.value = 'ETL job warning'
        dq_value_list = [dq_value]

        async_response = {
            "job_id": 1,
            "href": "/api/v1/bulk_metadata/job/?id=815"
        }
        job_response = {
            "status": "successful",
            "msg": "Job finished in 0.102986 seconds at 2023-11-30 17:19:08.627064+00:00",
            "result": {
                "fields": {
                    "created": {"count": 0, "sample": []},
                    "updated": {"count": 0, "sample": []}
                },
                "values": {
                    "created": {"count": 0, "sample": []},
                    "updated": {"count": 0, "sample": []}
                },
                "created_object_attribution": {
                    "success_count": 0,
                    "failure_count": 1,
                    "success_sample": [],
                    "failure_sample": [
                        {
                            "field_key": "human_name_string_2",
                            "object_key": "3.superstore.public.people"
                        }
                    ]
                },
                "flag_counts": {
                    "GOOD": 0,
                    "WARNING": 0,
                    "ALERT": 0
                },
                "total_duration": 0.10394948534667492
            }
        }

        m.register_uri('POST', '/integration/v1/data_quality/', json=async_response)
        m.register_uri('GET', '/api/v1/bulk_metadata/job/?id=1', json=job_response)
        async_result = MOCK_DQ.post_data_quality_values(dq_value_list)

        self.assertTrue(async_result)

    @requests_mock.Mocker()
    def test_failed_post_data_quality_values(self, m):

        dq_value = DataQualityValueItem()
        dq_value.field_key = '1.DQ.Test'
        dq_value.object_key = '1.Test.Table'
        dq_value.object_type = 'Table'
        dq_value.status = 'WARNING'
        dq_value.value = 'ETL job warning'
        dq_value_list = [dq_value]

        failed_response = {
            "Entry": 1,
            "Message": "field_key is required"
        }
        m.register_uri('POST', '/integration/v1/data_quality/', json=failed_response,
                       status_code=400)
        async_result = MOCK_DQ.post_data_quality_values(dq_value_list)

        self.assertFalse(async_result)

    @requests_mock.Mocker()
    def test_success_delete_data_quality_values(self, m):

        dq_value = DataQualityValue()
        dq_value.field_key = '1.DQ.Test'
        dq_value.object_key = '1.Test.Table'
        dq_value_list = [dq_value]

        async_response = {
            "job_id": 1,
            "href": "/api/v1/bulk_metadata/job/?id=819"
        }
        job_response = {
            "status": "successful",
            "msg": "Job finished in 0.086684 seconds at 2023-11-30 17:30:34.582365+00:00",
            "result": {
                "fields": {
                    "deleted": {
                        "count": 0,
                        "sample": []
                    },
                    "not_found": {
                        "count": 0,
                        "sample": []
                    }
                },
                "values": {
                    "deleted": {
                        "count": 0,
                        "sample": []
                    },
                    "not_found": {
                        "count": 1,
                        "sample": [{"field_key": "human_name_string_2", "object_key": "3.superstore.public.people"}]
                    }
                },
                "total_duration": 0.0881261546164751
            }
        }

        m.register_uri('DELETE', '/integration/v1/data_quality/', json=async_response)
        m.register_uri('GET', '/api/v1/bulk_metadata/job/?id=1', json=job_response)
        async_result = MOCK_DQ.delete_data_quality_values(dq_value_list)

        self.assertTrue(async_result)

    @requests_mock.Mocker()
    def test_failed_async_delete_process(self, m):

        dq_value = DataQualityValue()
        dq_value.field_key = '1.DQ.Test'
        dq_value.object_key = '1.Test.Table'
        dq_value_list = [dq_value]

        failed_response = {
            "Entry": 1,
            "Message": "field_key is required"
        }
        m.register_uri('DELETE', '/integration/v1/data_quality/', json=failed_response,
                       status_code=400)
        async_result = MOCK_DQ.delete_data_quality_values(dq_value_list)

        self.assertFalse(async_result)


if __name__ == '__main__':
    unittest.main()
