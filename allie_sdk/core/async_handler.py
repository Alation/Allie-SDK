"""Work with the Alation PATCH, POST and PUT Calls Asynchronously"""

import logging
import requests

from .request_handler import RequestHandler
from ..methods.job import AlationJob

LOGGER = logging.getLogger()


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

    def async_delete(self, url: str, payload: list, batch_size: int = None) -> bool:
        """Delete Alation Objects via an Async Job Process.

        Args:
            url (str): Delete API Call URL.
            payload (list): REST API Delete Body.
            batch_size (int): REST API Delete Body Size Limit.

        Returns:
            bool: Returns True if a batch fails.

        """
        failed_result = None
        batches = self._batch_objects(payload, batch_size)

        for batch in batches:
            try:
                LOGGER.debug(batch)
                async_response = self.delete(url, body=batch)
                if async_response:
                    job = AlationJob(self.access_token, self.session, self.host, async_response)
                    job.check_job_status()
                else:
                    failed_result = True
            except Exception as batch_error:
                LOGGER.error(batch_error, exc_info=True)
                failed_result = True

        return failed_result

    def async_delete_dict_payload(self, url: str, payload: dict) -> bool:
        """Delete the Alation Objects via an Async Job Process.

        Args:
            url (str): Delete API Call URL.
            payload (list): REST API Delete Body.

        Returns:
            bool: Returns True if the job fails.

        """
        failed_result = None
        async_response = self.delete(url, body=payload)
        if async_response:
            job = AlationJob(self.access_token, self.session, self.host, async_response)
            job.check_job_status()
        else:
            failed_result = True

        return failed_result

    def async_patch(self, url: str, payload: list, batch_size: int = None) -> bool:
        """Patch Alation Objects via an Async Job Process.

        Args:
            url (str): PATCH API Call URL.
            payload (list): REST API PATCH Body.
            batch_size (int): REST API PATCH Body Size Limit.

        Returns:
            bool: Returns True if a batch fails.

        """
        failed_result = None
        batches = self._batch_objects(payload, batch_size)

        for batch in batches:
            try:
                LOGGER.debug(batch)
                async_response = self.patch(url, body=batch)
                if async_response:
                    job = AlationJob(self.access_token, self.session, self.host, async_response)
                    job.check_job_status()
                else:
                    failed_result = True
            except Exception as batch_error:
                LOGGER.error(batch_error, exc_info=True)
                failed_result = True

        return failed_result

    def async_post(self, url: str, payload: list, batch_size: int = None, query_params: dict = None) -> bool:
        """Post Alation Objects via an Async Job Process.

        Args:
            url (str): POST API Call URL.
            payload (list): REST API POST Body.
            batch_size (int): REST API POST Body Size Limit.
            query_params (dict): REST API POST Query Parameters

        Returns:
            bool: Returns True if a batch fails

        """
        failed_result = None
        batches = self._batch_objects(payload, batch_size)

        for batch in batches:
            try:
                LOGGER.debug(batch)
                async_response = self.post(url, body=batch, query_params=query_params)
                if async_response:
                    job = AlationJob(self.access_token, self.session, self.host, async_response)
                    results = job.check_job_status()
                else:
                    failed_result = True
                    results = []
            except Exception as batch_error:
                LOGGER.error(batch_error, exc_info=True)
                failed_result = True
                results = []
        # OPEN: previously the return type used to be boolean
        # This is a change of behaviour => Test impact
        # OPEN: Should the result be mapped to a data class?
        # return failed_result
        return results



    def async_post_dict_payload(self, url: str, payload: dict) -> bool:
        """POST the Alation Objects via an Async Job Process.

        Args:
            url (str): POST API Call URL.
            payload (list): REST API Delete Body.

        Returns:
            bool: Returns True if the job fails.

        """
        failed_result = None
        async_response = self.post(url, body=payload)
        if async_response:
            job = AlationJob(self.access_token, self.session, self.host, async_response)
            job.check_job_status()
        else:
            failed_result = True

        return failed_result

    def async_put(self, url: str, payload: list, batch_size: int = None) -> bool:
        """Put Alation Objects via an Async Job Process.

        Args:
            url (str): PUT API Call URL.
            payload (list): REST API PUT Body.
            batch_size (int): REST API PUT Body Size Limit.

        Returns:
            bool: Returns True if a batch fails

        """
        failed_result = None
        batches = self._batch_objects(payload, batch_size)

        for batch in batches:
            try:
                LOGGER.debug(batch)
                async_response = self.put(url, body=batch)
                if async_response:
                    job = AlationJob(self.access_token, self.session, self.host, async_response)
                    job.check_job_status()
                else:
                    failed_result = True
            except Exception as batch_error:
                LOGGER.error(batch_error, exc_info=True)
                failed_result = True

        return failed_result

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
