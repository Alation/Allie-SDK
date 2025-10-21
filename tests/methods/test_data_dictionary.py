import requests
import requests_mock
import pytest

from allie_sdk.methods.data_dictionary import AlationDataDictionary, SUPPORTED_OBJECT_TYPES
from allie_sdk.models.data_dictionary_model import (
    DataDictionaryAsyncTaskDetails,
    DataDictionaryTaskDetails,
    DataDictionaryTaskError,
    DataDictionaryItem,
)
from allie_sdk.core.custom_exceptions import InvalidPostBody


class TestDataDictionary:

    def setup_method(self):
        self.client = AlationDataDictionary(
            access_token='token',
            session=requests.session(),
            host='https://test.com',
        )

    @requests_mock.Mocker()
    def test_upload_data_dictionary_success(self, mocker):
        api_response = {
            "task": {
                "id": "68575488-5fad-4117-927f-1e23576e733a",
                "type": "COMMIT_TO_CATALOG",
                "state": "QUEUED",
                "ts_created": "2023-08-17T11:23:19.766425Z",
                "links": [],
            }
        }

        mocker.register_uri(
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

        result = self.client.upload_data_dictionary('data', 1, payload)

        assert isinstance(result, DataDictionaryAsyncTaskDetails)
        assert result.task.state == 'QUEUED'

        request_body = mocker.last_request.body
        assert b'name="overwrite_values"' in request_body
        assert b'true' in request_body
        assert b'name="allow_reset"' in request_body

    @requests_mock.Mocker()
    def test_get_data_dictionary_task_details(self, mocker):
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

        mocker.register_uri(
            'GET',
            'https://test.com/integration/v1/data_dictionary/tasks/1e7a8e8f-fe46-4da4-8393-fce89be3ebcb',
            json=task_payload,
            status_code=200,
        )

        result = self.client.get_data_dictionary_task_details('1e7a8e8f-fe46-4da4-8393-fce89be3ebcb')

        assert isinstance(result, DataDictionaryTaskDetails)
        assert result.state == 'PROCESSING'
        assert result.progress.total_batches == 1

    @requests_mock.Mocker()
    def test_get_data_dictionary_task_errors(self, mocker):
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

        mocker.register_uri(
            'GET',
            'https://test.com/integration/v1/data_dictionary/tasks/abc/errors/',
            json=errors_payload,
            status_code=200,
        )

        result = self.client.get_data_dictionary_task_errors('abc')

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
