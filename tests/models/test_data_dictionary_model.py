from datetime import datetime
from io import BytesIO
from pathlib import Path

import pytest

from allie_sdk.models.data_dictionary_model import (
    AsyncTaskDetails,
    DataDictionaryTaskDetails,
    DataDictionaryTaskError,
    UploadDataDictionaryRequestPayload,
)
from allie_sdk.core.custom_exceptions import InvalidPostBody


def test_async_task_details_from_api():
    payload = {
        "task": {
            "id": "68575488-5fad-4117-927f-1e23576e733a",
            "type": "COMMIT_TO_CATALOG",
            "state": "QUEUED",
            "ts_created": "2023-08-17T11:23:19.766425Z",
            "links": [
                {
                    "rel": "info and status",
                    "href": "http://localhost:8000/integration/v1/data_dictionary/tasks/68575488-5fad-4117-927f-1e23576e733a",
                }
            ],
        }
    }

    result = AsyncTaskDetails.from_api_response(payload)

    assert isinstance(result.task, AsyncTaskDetails.__annotations__["task"])
    assert isinstance(result.task.ts_created, datetime)
    assert result.task.links[0].rel == "info and status"


def test_data_dictionary_task_details_from_api():
    payload = {
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

    result = DataDictionaryTaskDetails.from_api_response(payload)

    assert result.progress.total_batches == 1
    assert result.result.records.failed == 2
    assert isinstance(result.ts_created, datetime)
    assert result.dd_resource.otype == "data"


def test_data_dictionary_task_error_from_api():
    payload = {
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

    result = DataDictionaryTaskError.from_api_response(payload)

    assert isinstance(result.timestamp, datetime)
    assert result.details.items.range.start.key == "public.users"
    assert result.details.items.total == 4


def test_upload_payload_from_bytes():
    payload = UploadDataDictionaryRequestPayload(
        overwrite_values=True,
        allow_reset=False,
        file=b"column,description",
        file_name="dictionary.csv",
    )

    data, files, closeables = payload.generate_multipart_payload()

    assert data["overwrite_values"] == "true"
    assert data["allow_reset"] == "false"
    file_tuple = files["file"]
    assert file_tuple[0] == "dictionary.csv"
    assert file_tuple[2] == "text/csv"
    assert list(closeables)  # ensure the BytesIO is returned for closing


def test_upload_payload_from_path(tmp_path: Path):
    file_path = tmp_path / "dd.csv"
    file_path.write_text("column,description")

    payload = UploadDataDictionaryRequestPayload(
        overwrite_values=False,
        file=str(file_path),
    )

    data, files, closeables = payload.generate_multipart_payload()

    assert data["overwrite_values"] == "false"
    assert files["file"][0] == "dd.csv"
    closeable = list(closeables)[0]
    assert not closeable.closed
    closeable.close()


def test_upload_payload_invalid_file():
    payload = UploadDataDictionaryRequestPayload(
        overwrite_values=True,
        file=BytesIO(b"column"),
    )

    with pytest.raises(InvalidPostBody):
        UploadDataDictionaryRequestPayload(
            overwrite_values="yes",  # type: ignore[arg-type]
            file=BytesIO(b"column"),
        )

    with pytest.raises(InvalidPostBody):
        UploadDataDictionaryRequestPayload(
            overwrite_values=True,
            file_name=" ",
            file="/tmp/non-existing-file.csv",
        )

    payload.file = object()  # type: ignore[assignment]
    with pytest.raises(InvalidPostBody):
        payload.generate_multipart_payload()
