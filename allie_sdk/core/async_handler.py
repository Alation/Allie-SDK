"""Work with the Alation PATCH, POST and PUT Calls Asynchronously"""

import logging
import requests

from .request_handler import RequestHandler
from ..methods.job import AlationJob
from ..models.job_model import *

LOGGER = logging.getLogger('allie_sdk_logger')


class AsyncHandler(RequestHandler):
    """"Alation REST API Async Handler."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the AsyncHandler object.
        
        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
        
        """
        super().__init__(session, host, access_token=access_token)

        self.access_token = access_token
        self.host = host
        self.session = session

    def async_delete(self, url: str, payload: list, batch_size: int = None) -> list:
        """Delete Alation Objects via an Async Job Process.

        Args:
            url (str): Delete API Call URL.
            payload (list): REST API Delete Body.
            batch_size (int): REST API Delete Body Size Limit.

        Returns:
            list: job execution results

        """
        results = []
        batches = self._batch_objects(payload, batch_size)

        for batch in batches:
            try:
                LOGGER.debug(batch)
                async_response = self.delete(url, body=batch)
                if async_response:
                    # check if the response includes a job_id and only then fetch job details
                    if any(var in async_response.keys() for var in ("task", "job", "job_id", "job_name")):
                        job = AlationJob(self.access_token, self.session, self.host, async_response)
                        results.extend(job.check_job_status())
                    else:
                        # add the error details to the results list
                        results.append(async_response)

            except Exception as batch_error:
                LOGGER.error(batch_error, exc_info=True)
                results.append(self._map_batch_error_to_job_details(batch_error))

        return results

    def async_delete_dict_payload(self, url: str, payload: dict) -> list:
        """Delete the Alation Objects via an Async Job Process.

        Args:
            url (str): Delete API Call URL.
            payload (list): REST API Delete Body.

        Returns:
            list: job execution results

        """
        results = []
        async_response = self.delete(url, body=payload)
        if async_response:
            # check if the response includes a job_id and only then fetch job details
            if any(var in async_response.keys() for var in ("task", "job", "job_id", "job_name")):
                job = AlationJob(self.access_token, self.session, self.host, async_response)
                results.extend(job.check_job_status())
            else:
                # add the error details to the results list
                results.append(async_response)

        return results

    def async_patch(self, url: str, payload: list, batch_size: int = None) -> list:
        """Patch Alation Objects via an Async Job Process.

        Args:
            url (str): PATCH API Call URL.
            payload (list): REST API PATCH Body.
            batch_size (int): REST API PATCH Body Size Limit.

        Returns:
            list: job execution results

        """
        results = []
        batches = self._batch_objects(payload, batch_size)

        for batch in batches:
            try:
                LOGGER.debug(batch)
                async_response = self.patch(url, body=batch)
                if async_response:
                    # check if the response includes a job_id and only then fetch job details
                    if any(var in async_response.keys() for var in ("task", "job", "job_id", "job_name")):
                        job = AlationJob(self.access_token, self.session, self.host, async_response)
                        results.extend(job.check_job_status())
                    else:
                        # add the error details to the results list
                        results.append(async_response)

            except Exception as batch_error:
                LOGGER.error(batch_error, exc_info=True)
                results.append(self._map_batch_error_to_job_details(batch_error))

        return results

    def async_post(self, url: str, payload: list, batch_size: int = None, query_params: dict = None) -> list:
        """Post Alation Objects via an Async Job Process.

        Args:
            url (str): POST API Call URL.
            payload (list): REST API POST Body.
            batch_size (int): REST API POST Body Size Limit.
            query_params (dict): REST API POST Query Parameters

        Returns:
            list: job execution results

        """
        results = []
        batches = self._batch_objects(payload, batch_size)

        for batch in batches:
            try:
                LOGGER.debug(batch)
                async_response = self.post(url, body=batch, query_params=query_params)
                if async_response:
                    # check if the response includes a job_id and only then fetch job details
                    if any(var in async_response.keys() for var in ("task", "job", "job_id", "job_name")):
                        job = AlationJob(self.access_token, self.session, self.host, async_response)
                        results.extend(job.check_job_status())
                    else:
                        # add the error details to the results list
                        results.append(async_response)

            except Exception as batch_error:
                LOGGER.error(batch_error, exc_info=True)
                results.append(self._map_batch_error_to_job_details(batch_error))
        return results

    def async_post_data_payload(self, url: str, data: any, query_params: dict = None) -> list:
        """POST the Alation Objects via an Async Job Process.
            Method to process the posts that are not lists, but data e.g. strings. Batching is not needed in these cases
            and the payload should be processed in their entirety as the contents and sequence of objects is important.
            For example Virtual Data and File Sources use this logic
        Args:
            url (str): POST API Call URL.
            payload (str): REST API data type payload.

        Returns:
            bool: Returns True if the job fails.

        """
        results = []
        try:
            LOGGER.debug(data)
            async_response = self.post(url, body=data, query_params=query_params)
            if async_response:
                # check if the response includes a job_id and only then fetch job details
                if any(var in async_response.keys() for var in ("task", "job", "job_id", "job_name")):
                    job = AlationJob(self.access_token, self.session, self.host, async_response)
                    results.extend(job.check_job_status())
                else:
                    # add the error details to the results list
                    results.append(async_response)

        except Exception as batch_error:
            LOGGER.error(batch_error, exc_info=True)
            results.append(self._map_batch_error_to_job_details(batch_error))

        return results

    def async_post_dict_payload(self, url: str, payload: dict) -> dict:
        """POST the Alation Objects via an Async Job Process.

        Args:
            url (str): POST API Call URL.
            payload (list): REST API Delete Body.

        Returns:
            job execution results

        """

        async_response = self.post(url, body=payload)
        if async_response:
            # check if the response includes a job_id and only then fetch job details
            if any(var in async_response.keys() for var in ("task", "job", "job_id", "job_name")):
                job = AlationJob(self.access_token, self.session, self.host, async_response)
                result = job.check_job_status()
                return result
            else:
                # add the error details to the results list
                return async_response

    def async_put(self, url: str, payload: list, batch_size: int = None) -> list:
        """Put Alation Objects via an Async Job Process.

        Args:
            url (str): PUT API Call URL.
            payload (list): REST API PUT Body.
            batch_size (int): REST API PUT Body Size Limit.

        Returns:
            list: job execution results

        """
        batches = self._batch_objects(payload, batch_size)
        results = []

        for batch in batches:
            try:
                LOGGER.debug(batch)
                async_response = self.put(url, body=batch)
                if async_response:
                    # check if the response includes a job_id and only then fetch job details
                    if any(var in async_response.keys() for var in ("task", "job", "job_id", "job_name")):
                        job = AlationJob(self.access_token, self.session, self.host, async_response)
                        results.extend(job.check_job_status())
                    else:
                        # add the error details to the results list
                        results.append(async_response)
            except Exception as batch_error:
                LOGGER.error(batch_error, exc_info=True)
                results.append(self._map_batch_error_to_job_details(batch_error))

        return results

    def _batch_objects(self, objects: list, batch_size: int = None) -> list:
        """Batch the Alation Objects into Acceptable Payload Sizes.

        Args:
            objects (list): Alation Objects.
            batch_size (int): REST API Body Size Limit.

        Returns:
            list: List of batched Alation Objects.

        """
        if batch_size:
            page_size = batch_size
        else:
            page_size = self.page_size

        LOGGER.debug(f'Batching the {len(objects)} objects into lists of {page_size}')
        batch_payload = [objects[x:x + page_size] for x in range(0, len(objects), page_size)]
        LOGGER.debug(f'Batching complete. {len(batch_payload)} batches created.')

        return batch_payload

    @staticmethod
    def _map_batch_error_to_job_details(batch_error:Exception) -> dict:

        # conform with JobDetails structure
        error_data = dict(
            status = "failed"
            , msg = ""
            , result = batch_error
        )

        return error_data