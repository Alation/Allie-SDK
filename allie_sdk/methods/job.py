"""Alation REST API Job Methods,"""

import logging
import requests
from time import sleep

from ..core.request_handler import RequestHandler
from ..models.job_model import *

LOGGER = logging.getLogger('allie_sdk_logger')


class AlationJob(RequestHandler):
    """Alation REST API Job Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str, job_response: dict):
        """Creates an instance of the Job object.

        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
            job_response (dict): Alation REST API Async Job Details.

        """
        super().__init__(session, host, access_token=access_token)

        if "task" in job_response.keys():
            # cater for non-standard result sets (e.g. policy endpoint) structure: {'task': {'id': 25647, ... }}
            self.async_job = AsyncJobDetails.from_api_response(job_response['task'])
        elif "job" in job_response.keys():
            # cater for non-standard result sets (e.g. virtual file system endpoint)
            # structure: {'job': {'id': 25647, ... }}
            self.async_job = AsyncJobDetails.from_api_response(job_response['job'])
        else: # cater for standard result set structure: {'job_id': 23442, ... }
            # virtual data source endpoint returns {'job_name': MetadataExtraction#, ... }
            self.async_job = AsyncJobDetails.from_api_response(job_response)

    def check_job_status(self):
        """Query the Alation Background Job and Log Status until Job has completed."""

        job_details = []

        while True:
            job, job_details_vanilla = self._get_job()
            self._log_job(job)

            if job.status.lower() == 'failed':
                job_details.append(job_details_vanilla)
                break
            elif job.status.lower() == 'successful':
                job_details.append(job_details_vanilla)
                break
            else:
                sleep(3)

        sleep(1)
        # Note: We return the original unparsed job details here
        # since it is not standardised across endpoints and methods
        # we can do the mapping to data classes in the actual methods
        # so we have more context for the processing
        return job_details

    def _get_job(self) -> tuple[JobDetails, dict]:
        """Query the Alation Job.

        Returns:
            tuple[JobDetails, dict]: Alation Job details and raw response.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        query_params = {'name': self.async_job.job_name} if self.async_job.job_name else {'id': self.async_job.job_id}
        job_response = self.get(
            url ='/api/v1/bulk_metadata/job/'
            , query_params=query_params
            , pagination=False
        )

        job_details = JobDetails.from_api_response(job_response)
        # since the job response is not standardised across endpoints and methods
        # we cannot just map it to a generic data class here
        # we need some context as to what endpoint and method was used
        # and then can do the mapping
        return job_details, job_response

    def _log_job(self, job: JobDetails):
        """Format the Logs Messages of the Alation Job.

        Args:
            job: Alation Job.
        """
        job_identifier = self.async_job.job_id if self.async_job.job_name else self.async_job.job_id
        if job.status.lower() == 'running':
            LOGGER.debug(f'Job: {job_identifier}... {job.status}')
            LOGGER.debug(job.result)

        if job.status == 'successful':
            LOGGER.debug(f'Job: {job_identifier}\nJob Status: Successful\n'
                         f'Job Message: {job.msg}')
            LOGGER.debug(job.result)

        if job.status == 'failed':
            LOGGER.error(f'Job: {job_identifier}\nJob Status: Failed\n'
                         f'Job Message: {job.msg}')
            LOGGER.debug(job.result)
