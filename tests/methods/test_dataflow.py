"""Test the Alation REST API Dataflow Methods."""

import requests_mock
import unittest
from allie_sdk.methods.dataflow import *


class TestDataflow(unittest.TestCase):

    def setUp(self):
        self.mock_df = AlationDataflow(
            access_token='test',
            session=requests.session(),
            host='https://test.com'
        )

    @requests_mock.Mocker()
    def test_get_dataflows(self, requests_mock):
        api_response = {
            "dataflow_objects": [
                {
                    "id": 1,
                    "external_id": "api/df101",
                    "title": "Purchase transaction Transformation",
                    "description": "Data flow from customer table to purchase history table",
                    "content": "select * from table",
                    "group_name": "Snowflake-1"
                }
            ],
            "paths": [
                [
                    [{"otype": "table", "key": "1.schema.Customers"}],
                    [{"otype": "dataflow", "key": "api/df101"}],
                    [{"otype": "table", "key": "1.schema.Purchases"}],
                ]
            ]
        }

        expected = DataflowPayload.from_api_response(api_response)

        requests_mock.register_uri(
            method='GET',
            url='/integration/v2/dataflow/?keyField=id',
            json=api_response,
            status_code=200
        )

        result = self.mock_df.get_dataflows([1], DataflowParams(keyField='id'))
        self.assertEqual(result, expected)

    @requests_mock.Mocker()
    def test_create_or_replace_dataflows(self, requests_mock):
        post_response = {"job_id": 100}
        job_response = {
            "status": "successful",
            "msg": "",
            "result": None
        }
        requests_mock.register_uri(
            method='POST',
            url='/integration/v2/dataflow/',
            json=post_response,
            status_code=202
        )
        requests_mock.register_uri(
            method='GET',
            url='/api/v1/bulk_metadata/job/?id=100',
            json=job_response,
            status_code=200
        )
        payload = DataflowPayload(
            dataflow_objects=[Dataflow(external_id="api/df101")]
        )
        result = self.mock_df.create_or_replace_dataflows(payload)
        expected = [JobDetailsDataflowPost.from_api_response(job_response)]
        self.assertEqual(result, expected)

    @requests_mock.Mocker()
    def test_update_dataflows(self, requests_mock):
        patch_response = {"job_id": 101}
        job_response = {
            "status": "successful",
            "msg": "",
            "result": None
        }
        requests_mock.register_uri(
            method='PATCH',
            url='/integration/v2/dataflow/',
            json=patch_response,
            status_code=202
        )
        requests_mock.register_uri(
            method='GET',
            url='/api/v1/bulk_metadata/job/?id=101',
            json=job_response,
            status_code=200
        )
        items = [DataflowPatchItem(id=1, title="New")]
        result = self.mock_df.update_dataflows(items)
        expected = [JobDetailsDataflowPost.from_api_response(job_response)]
        self.assertEqual(result, expected)

    @requests_mock.Mocker()
    def test_delete_dataflows(self, requests_mock):
        delete_response = {"job_id": 102}
        job_response = {
            "status": "successful",
            "msg": "",
            "result": None
        }
        requests_mock.register_uri(
            method='DELETE',
            url='/integration/v2/dataflow/?keyField=id',
            json=delete_response,
            status_code=202
        )
        requests_mock.register_uri(
            method='GET',
            url='/api/v1/bulk_metadata/job/?id=102',
            json=job_response,
            status_code=200
        )
        result = self.mock_df.delete_dataflows([1], DataflowParams(keyField='id'))
        expected = [JobDetailsDataflowDelete.from_api_response(job_response)]
        self.assertEqual(result, expected)
