"""Work with the Alation PATCH, POST and PUT Calls Asynchronously"""

import logging
import requests
import re
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

    def async_delete(
            self,
            url: str,
            payload: list,
            batch_size: int = None,
            query_params: dict = None,
    ) -> list:
        """Delete Alation Objects via an Async Job Process.

        Args:
            url (str): Delete API Call URL.
            payload (list): REST API Delete Body.
            batch_size (int): REST API Delete Body Size Limit.
            query_params (dict): DELETE API Call Query Parameters.


        Returns:
            list: job execution results

        Raises:
            requests.exceptions.HTTPError: If the API returns a non-success status code.
        """
        results = []
        batches = self._batch_objects(payload, batch_size)

        for batch in batches:
            try:
                LOGGER.debug(batch)
                async_response = self.delete(
                    url, body=batch, query_params=query_params, is_async=True
                )
                if async_response:
                    # check if the response includes a job_id and only then fetch job details
                    if any(var in async_response.keys() for var in ("task", "job", "job_id", "job_name")):
                        job = AlationJob(self.access_token, self.session, self.host, async_response)
                        results.extend(job.check_job_status())
                    else:
                        # add the error details to the results list
                        results.append(async_response)

            except requests.exceptions.HTTPError as e:
                LOGGER.error(f"HTTP error occurred: {e}", exc_info=True)
                # Raise all HTTP errors for consistent behavior
                raise
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

        Raises:
            requests.exceptions.HTTPError: If the API returns a non-success status code.
        """

        results: list = []
        # Note: batching is implemented on a higher level since the structure of the payload is not standardised
        try:
            async_response = self.delete(
                url=url,
                body=payload,
                is_async=True,
            )

            if async_response:
                # check if the response includes a job_id and only then fetch job details
                if any(var in async_response.keys() for var in ("task", "job", "job_id", "job_name")):
                    job = AlationJob(self.access_token, self.session, self.host, async_response)
                    results = job.check_job_status()
                else:
                    # add the error details
                    # this needs to be a list here since results above is also a list
                    results = [async_response]
            else:
                LOGGER.debug("No async response received from delete request")
        except requests.exceptions.HTTPError as e:
            LOGGER.error(f"HTTP error occurred: {e}", exc_info=True)
            # Raise all HTTP errors for consistent behavior
            raise

        return results

    def async_patch(self, url: str, payload: list, batch_size: int = None) -> list:
        """Patch Alation Objects via an Async Job Process.

        Args:
            url (str): PATCH API Call URL.
            payload (list): REST API PATCH Body.
            batch_size (int): REST API PATCH Body Size Limit.

        Returns:
            list: job execution results

        Raises:
            requests.exceptions.HTTPError: If the API returns a non-success status code.
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

            except requests.exceptions.HTTPError as e:
                LOGGER.error(f"HTTP error occurred: {e}", exc_info=True)
                # Raise all HTTP errors for consistent behavior
                raise
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

        Raises:
            requests.exceptions.HTTPError: If the API returns a non-success status code.
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

            except requests.exceptions.HTTPError as e:
                LOGGER.error(f"HTTP error occurred: {e}", exc_info=True)
                # Raise all HTTP errors for consistent behavior
                raise
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
            list: job execution results

        Raises:
            requests.exceptions.HTTPError: If the API returns a non-success status code.
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

        except requests.exceptions.HTTPError as e:
            LOGGER.error(f"HTTP error occurred: {e}", exc_info=True)
            # Raise all HTTP errors for consistent behavior
            raise
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

        Raises:
            requests.exceptions.HTTPError: If the API returns a non-success status code.
        """

        # Note: batching is implemented on a higher level since the structure of the payload is not standardised
        try:
            async_response = self.post(url, body=payload)
            if async_response:
                # check if the response includes a job_id and only then fetch job details
                if any(var in async_response.keys() for var in ("task", "job", "job_id", "job_name")):
                    job = AlationJob(self.access_token, self.session, self.host, async_response)
                    results = job.check_job_status()
                else:
                    # add the error details to the results list
                    # this needs to be a list here since results above is also a list
                    results = [ async_response ]

                return results
        except requests.exceptions.HTTPError as e:
            LOGGER.error(f"HTTP error occurred: {e}", exc_info=True)
            # Raise all HTTP errors for consistent behavior
            raise

    def async_put(self, url: str, payload: list, batch_size: int = None) -> list:
        """Put Alation Objects via an Async Job Process.

        Args:
            url (str): PUT API Call URL.
            payload (list): REST API PUT Body.
            batch_size (int): REST API PUT Body Size Limit.

        Returns:
            list: job execution results

        Raises:
            requests.exceptions.HTTPError: If the API returns a non-success status code.
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
                        job_status = job.check_job_status()
                        results.extend(job_status)

                        # the custom fields values endpoint returns additionally a legacy job id
                        # see also https://github.com/Alation/Allie-SDK/issues/26
                        if isinstance(job_status[0]["result"], list):
                            r = re.compile(r"\(can be tracked using jobs API\)\:\s([0-9]+)$")
                            m = r.search(job_status[0]["result"][0])

                            if m is None:
                                LOGGER.debug("No legacy job_id found")
                            else:
                                legacy_job_id = m.groups()[0]
                                LOGGER.debug(f"Following legacy job id found: {legacy_job_id}")
                                legacy_job = AlationJob(
                                    session=self.session
                                    , host=self.host
                                    , access_token=self.access_token
                                    , job_response={'job_id': legacy_job_id}
                                )
                                legacy_job_status = legacy_job.check_job_status()
                                results.extend(legacy_job_status)
                    else:
                        # add the error details to the results list
                        results.append(async_response)
            except requests.exceptions.HTTPError as e:
                LOGGER.error(f"HTTP error occurred: {e}", exc_info=True)
                # Raise all HTTP errors for consistent behavior
                raise
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