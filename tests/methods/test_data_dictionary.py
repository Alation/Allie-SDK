import unittest
import requests
import requests_mock
import pytest

from allie_sdk.methods.data_dictionary import AlationDataDictionary, SUPPORTED_OBJECT_TYPES
from allie_sdk.models.data_dictionary_model import *
from allie_sdk.models.job_model import *
from allie_sdk.core.custom_exceptions import InvalidPostBody


class TestDataDictionary(unittest.TestCase):

    def setUp(self):
        self.client = AlationDataDictionary(
            access_token='token',
            session=requests.session(),
            host='https://test.com'
        )

    @requests_mock.Mocker()
    def test_upload_data_dictionary_success(self, requests_mock):

        # ENDPOINT: Upload a data dictionary
        api_response = {
            "task": {
                "id": "68575488-5fad-4117-927f-1e23576e733a",
                "type": "COMMIT_TO_CATALOG",
                "state": "QUEUED",
                "ts_created": "2023-08-17T11:23:19.766425Z",
                "links": [],
            }
        }

        requests_mock.register_uri(
            'PUT',
            'https://test.com/integration/v1/data_dictionary/data/1/upload/',
            json=api_response,
            status_code=202,
        )

        payload = DataDictionaryItem(
            overwrite_values=True,
            allow_reset=True,
            file=b"name,description",
            file_name="dictionary.csv",
        )

        # ENDPOINT: Get data dictionary task details
        get_task_details_reponse = {
            "id": "1e7a8e8f-fe46-4da4-8393-fce89be3ebcb",
            "type": "COMMIT_TO_CATALOG",
            "state": "COMPLETED",
            "status": "PARTIALLY_SUCCEEDED",
            "progress": {"total_batches": 1, "batches_completed": 1},
            "result": {
                "records": {
                    "total": 351,
                    "succeeded": 349,
                    "failed": 2,
                }
            },
            "ts_created": "2025-04-25T03:28:26.287938Z",
            "ts_updated": "2025-04-25T03:28:35.916508Z",
            "ts_completed": "2025-04-25T03:28:35.916048Z",
            "dd_resource": {
                "id": "12b32089-e26a-45b6-816c-44364d395ba7",
                "oid": 1,
                "otype": "data",
                "user_id": 1,
            },
            "report_download_link": "http://localhost:8000/download/data_dictionary/data_1_1_2023-08-17T11-35-03-577118.csv/",
        }

        requests_mock.register_uri(
            method = "GET"
            , url = "https://test.com/integration/v1/data_dictionary/tasks/68575488-5fad-4117-927f-1e23576e733a"
            , json = get_task_details_reponse
            , status_code = 200
        )

        # ENDPOINT: Get data dictionary task errors

        get_task_error_response = {
            "timestamp": "2024-03-11T12:10:25.379537Z",
            "name": "TaskflowException",
            "fatal": True,
            "error_message": "'NoneType' object is not callable",
            "original_error_message": None,
            "details": {
                "items": {
                    "range": {
                        "start": {"index": 0, "key": "public.users"},
                        "end": {"index": 3, "key": "public.users.email"},
                        "start_inclusive": True,
                        "end_inclusive": True,
                    },
                    "total": 4,
                },
                "error": "'NoneType' object is not callable",
            },
            "category": "System Error",
        }

        requests_mock.register_uri(
            method="GET"
            , url="https://test.com/integration/v1/data_dictionary/tasks/68575488-5fad-4117-927f-1e23576e733a/errors/"
            , json= get_task_error_response
            , status_code=200
        )

        result = self.client.upload_data_dictionary('data', 1, payload)

        expected_result = JobDetails(
            status='partially_successful'
            , msg=''
            , result=DataDictionaryTaskDetails(
                id='1e7a8e8f-fe46-4da4-8393-fce89be3ebcb'
                , type='COMMIT_TO_CATALOG'
                , state='COMPLETED'
                , status='PARTIALLY_SUCCEEDED'
                , progress=DataDictionaryTaskProgress(
                    total_batches=1
                    , batches_completed=1
                )
                , result=DataDictionaryTaskResult(
                    records=DataDictionaryTaskRecords(
                        total=351
                        , succeeded=349
                        , failed=2
                    )
                )
                , ts_created=datetime(2025, 4, 25, 3, 28, 26, 287938)
                , ts_updated=datetime(2025, 4, 25, 3, 28, 35, 916508)
                , ts_completed=datetime(2025, 4, 25, 3, 28, 35, 916048)
                , dd_resource=DataDictionaryResource(
                    id='12b32089-e26a-45b6-816c-44364d395ba7'
                    , oid=1
                    , otype='data'
                    , user_id=1
                )
                , report_download_link='http://localhost:8000/download/data_dictionary/data_1_1_2023-08-17T11-35-03-577118.csv/')
        )

        assert expected_result == result

    @requests_mock.Mocker()
    def test_get_data_dictionary_task_details(self, requests_mock):
        task_payload = {
            "id": "1e7a8e8f-fe46-4da4-8393-fce89be3ebcb",
            "type": "COMMIT_TO_CATALOG",
            "state": "PROCESSING",
            "status": None,
            "progress": {"total_batches": 1, "batches_completed": 0},
            "result": None,
            "ts_created": "2025-04-25T03:28:26.287938Z",
            "ts_updated": "2025-04-25T03:28:35.916508Z",
            "ts_completed": None,
            "dd_resource": None,
            "report_download_link": None,
        }

        requests_mock.register_uri(
            'GET',
            'https://test.com/integration/v1/data_dictionary/tasks/1e7a8e8f-fe46-4da4-8393-fce89be3ebcb',
            json=task_payload,
            status_code=200,
        )

        result = self.client._get_data_dictionary_task_details('1e7a8e8f-fe46-4da4-8393-fce89be3ebcb')

        assert isinstance(result, DataDictionaryTaskDetails)
        assert result.state == 'PROCESSING'
        assert result.progress.total_batches == 1

    @requests_mock.Mocker()
    def test_get_data_dictionary_task_errors(self, requests_mock):
        errors_payload = [
            {
                "timestamp": "2024-03-11T12:10:25.379537Z",
                "name": "TaskflowException",
                "fatal": True,
                "error_message": "'NoneType' object is not callable",
                "original_error_message": None,
                "details": None,
                "category": "System Error",
            }
        ]

        requests_mock.register_uri(
            'GET',
            'https://test.com/integration/v1/data_dictionary/tasks/abc/errors/',
            json=errors_payload,
            status_code=200,
        )

        result = self.client._get_data_dictionary_task_errors('abc')

        assert len(result) == 1
        assert isinstance(result[0], DataDictionaryTaskError)
        assert result[0].fatal is True

    def test_upload_data_dictionary_invalid_object_type(self):
        payload = DataDictionaryItem(
            overwrite_values=True,
            file=b"name,description",
        )

        with pytest.raises(InvalidPostBody):
            self.client.upload_data_dictionary('invalid', 1, payload)

    def test_upload_data_dictionary_missing_object_id(self):
        payload = DataDictionaryItem(
            overwrite_values=True,
            file=b"name,description",
        )

        with pytest.raises(InvalidPostBody):
            self.client.upload_data_dictionary('data', None, payload)

    def test_supported_object_types_constant(self):
        expected_values = {
            'data',
            'schema',
            'table',
            'glossary_v3',
            'bi_server',
            'bi_folder',
            'bi_report',
            'bi_datasource',
        }

        assert SUPPORTED_OBJECT_TYPES == expected_values
