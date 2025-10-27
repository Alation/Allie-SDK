"""Alation REST API Data Dictionary Methods."""

from __future__ import annotations

import logging
from typing import Iterable
from time import sleep

import requests

from ..core.custom_exceptions import InvalidPostBody, validate_rest_payload
from ..core.request_handler import RequestHandler
from ..models.data_dictionary_model import (
    DataDictionaryAsyncTaskDetails,
    DataDictionaryTaskDetails,
    DataDictionaryTaskError,
    DataDictionaryItem,
)
from ..models.job_model import *

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

    def _get_data_dictionary_task_details(self, task_id: str) -> DataDictionaryTaskDetails:
        """Retrieve details of an asynchronous data dictionary upload task."""

        if not task_id:
            raise InvalidPostBody("'task_id' must be provided to retrieve task details.")

        LOGGER.info("Fetching data dictionary task details for task_id='%s'", task_id)
        response = self.get(
            url=f'/integration/v1/data_dictionary/tasks/{task_id}',
            pagination=False,
        )

        return DataDictionaryTaskDetails.from_api_response(response)

    def _get_data_dictionary_task_errors(self, task_id: str) -> list[DataDictionaryTaskError]:
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

    def upload_data_dictionary(
        self,
        object_type: str,
        object_id: int | str,
        payload: DataDictionaryItem,
    ) -> JobDetails:
        """Upload a data dictionary file for a catalog object."""

        self._validate_object_type(object_type)
        self._validate_object_id(object_id)

        validate_rest_payload([payload], expected_types=(DataDictionaryItem,))

        data, files, closeables = payload.generate_multipart_payload()
        url = f'/integration/v1/data_dictionary/{object_type}/{object_id}/upload/'

        result = ""

        try:
            LOGGER.info(
                "Uploading data dictionary for object_type='%s', object_id='%s'", object_type, object_id
            )
            """
            The data dict upload is an async job. Why are we not using async_put here? Reasons:
            
            - async_put doesn't expect file input (it splits a payload into batches for processing)
            - the async_handler uses the job status endpoint to get the status 
            
            So overall it was easier to just keep the logic contained within here.
            """

            response = self.put(url=url, body=data, files=files)
            task =  DataDictionaryAsyncTaskDetails.from_api_response(response)

            # Poll the task endpoint for a short time just to illustrate usage
            task_details = self._get_data_dictionary_task_details(task.task.id)

            while task_details.state != "COMPLETED":
                batches_completed = task_details.progress.batches_completed if task_details.progress else 0
                total_batches = task_details.progress.total_batches if task_details.progress else 0
                logging.info(
                    f"Task {task_details.id} currently in state {task_details.state} (batches completed: {batches_completed}/{total_batches})"
                )
                sleep(2)
                task_details = self._get_data_dictionary_task_details(task.task.id)

            logging.info(f"Task {task_details.id} completed with status {task_details.status}")

            if task_details.status == "FAILED":
                errors = self._get_data_dictionary_task_errors(task_details.id)
                if errors:
                    logging.info(f"First reported error: {errors[0].error_message}")
                result = JobDetails(
                    status = "failed"
                    , msg = errors[0].error_message
                    , result = ""
                )
            elif task_details.status == "PARTIALLY_SUCCEEDED":
                result = JobDetails(
                    status = "partially_successful"
                    , msg = ""
                    , result = task_details
                )
            elif task_details.status == "SUCCEEDED":
                result = JobDetails(
                    status = "successful"
                    , msg = f"Upload stats: {task_details.result}. Link to status report: {task_details.report_download_link}"
                    , result = task_details
                )
            else:
                result = JobDetails(
                    status = "unexpected status - check result for details"
                    , msg = ""
                    , result = task_details
                )

        finally:
            self._close_file_handles(closeables)

        return result

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
