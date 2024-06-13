"""Alation REST API Job Methods,"""

import logging
import requests
from time import sleep

from ..core.request_handler import RequestHandler
from ..models.job_model import *

LOGGER = logging.getLogger()


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
        else: # cater for standard result set structure: {'job_id': 23442, ... }
            self.async_job = AsyncJobDetails.from_api_response(job_response)

    def check_job_status(self):
        """Query the Alation Background Job and Log Status until Job has completed."""

        while True:
            job = self._get_job()
            self._log_job(job)

            if job.status.lower() in ['successful', 'failed']:
                break
            else:
                sleep(3)

        sleep(1)

    def _get_job(self) -> JobDetails:
        """Query the Alation Job.

        Returns:
            JobDetails: Alation Job.

        """
        job_response = self.get('/api/v1/bulk_metadata/job/',
                                query_params={'id': self.async_job.job_id}, pagination=False)

        if job_response:
            return JobDetails.from_api_response(job_response)

    def _log_job(self, job: JobDetails):
        """Format the Logs Messages of the Alation Job.

        Args:
            job: Alation Job.
        """

        if job.status.lower() == 'running':
            LOGGER.debug(f'Job: {self.async_job.job_id}... {job.status}')
            LOGGER.debug(job.result)

        if job.status == 'successful':
            LOGGER.debug(f'Job: {self.async_job.job_id}\nJob Status: Successful\n'
                         f'Job Message: {job.msg}')
            LOGGER.debug(job.result)

        if job.status == 'failed':
            LOGGER.error(f'Job: {self.async_job.job_id}\nJob Status: Failed\n'
                         f'Job Message: {job.msg}')
            LOGGER.debug(job.result)
