"""Alation REST API Data Dictionary Methods."""

from __future__ import annotations

import logging
from typing import Iterable

import requests

from ..core.custom_exceptions import InvalidPostBody, validate_rest_payload
from ..core.request_handler import RequestHandler
from ..models.data_dictionary_model import (
    AsyncTaskDetails,
    DataDictionaryTaskDetails,
    DataDictionaryTaskError,
    UploadDataDictionaryRequestPayload,
)

LOGGER = logging.getLogger('allie_sdk_logger')

SUPPORTED_OBJECT_TYPES = {
    'data',
    'schema',
    'table',
    'glossary_v3',
    'bi_server',
    'bi_folder',
    'bi_report',
    'bi_datasource',
}


class AlationDataDictionary(RequestHandler):
    """Alation REST API Data Dictionary Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the DataDictionary object."""

        super().__init__(session=session, host=host, access_token=access_token)

    def upload_data_dictionary(
        self,
        object_type: str,
        object_id: int | str,
        payload: UploadDataDictionaryRequestPayload,
    ) -> AsyncTaskDetails:
        """Upload a data dictionary file for a catalog object."""

        self._validate_object_type(object_type)
        self._validate_object_id(object_id)

        validate_rest_payload([payload], expected_types=(UploadDataDictionaryRequestPayload,))

        data, files, closeables = payload.generate_multipart_payload()
        url = f'/integration/v1/data_dictionary/{object_type}/{object_id}/upload/'

        try:
            LOGGER.info(
                "Uploading data dictionary for object_type='%s', object_id='%s'", object_type, object_id
            )
            response = self.put(url=url, body=data, files=files)
            return AsyncTaskDetails.from_api_response(response)
        finally:
            self._close_file_handles(closeables)

    def get_data_dictionary_task_details(self, task_id: str) -> DataDictionaryTaskDetails:
        """Retrieve details of an asynchronous data dictionary upload task."""

        if not task_id:
            raise InvalidPostBody("'task_id' must be provided to retrieve task details.")

        LOGGER.info("Fetching data dictionary task details for task_id='%s'", task_id)
        response = self.get(
            url=f'/integration/v1/data_dictionary/tasks/{task_id}',
            pagination=False,
        )

        return DataDictionaryTaskDetails.from_api_response(response)

    def get_data_dictionary_task_errors(self, task_id: str) -> list[DataDictionaryTaskError]:
        """Retrieve the errors reported for a data dictionary upload task."""

        if not task_id:
            raise InvalidPostBody("'task_id' must be provided to retrieve task errors.")

        LOGGER.info("Fetching data dictionary task errors for task_id='%s'", task_id)
        response = self.get(
            url=f'/integration/v1/data_dictionary/tasks/{task_id}/errors/',
            pagination=False,
        )

        if not response:
            return []

        return [
            DataDictionaryTaskError.from_api_response(item)
            if isinstance(item, dict)
            else item
            for item in response
        ]

    @staticmethod
    def _close_file_handles(closeables: Iterable):
        for closeable in closeables:
            try:
                closeable.close()
            except Exception as close_error:  # pragma: no cover - defensive
                LOGGER.warning("Failed to close data dictionary file handle: %s", close_error, exc_info=True)

    @staticmethod
    def _validate_object_type(object_type: str):
        if not object_type:
            raise InvalidPostBody("'object_type' must be provided for the upload request.")

        if object_type not in SUPPORTED_OBJECT_TYPES:
            raise InvalidPostBody(
                f"Unsupported 'object_type' value '{object_type}'. Supported values: {sorted(SUPPORTED_OBJECT_TYPES)}"
            )

    @staticmethod
    def _validate_object_id(object_id: int | str):
        if object_id in (None, ''):
            raise InvalidPostBody("'object_id' must be provided for the upload request.")
