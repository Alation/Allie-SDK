"""Alation Critical Data Manager (CDM / CDE) — Job Methods."""

import logging
import requests

from ..core.cde_request_handler import CDERequestHandler, CDE_BASE
from ..core.custom_exceptions import validate_query_params
from ..models.cde_job_model import CDEJob, CDEJobParams

LOGGER = logging.getLogger("allie_sdk_logger")

CDE_JOB_ENDPOINT = f"{CDE_BASE}/job/"


class AlationCDMJob(CDERequestHandler):
    """Alation Critical Data Manager (CDM / CDE) Job Methods.

    CDE jobs track asynchronous CDE operations (e.g. bulk-create). They use their own
    endpoint and status vocabulary (``QUEUED``/``IN_PROGRESS``/``FINISHED``/``ERROR``/
    ``CANCELED``), distinct from the core Alation background-job API.
    """

    def __init__(self, access_token: str = None, session: requests.Session = None,
                 host: str = None):
        """Create an instance of the CDE Job object.

        Args:
            access_token (str, optional): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.

        """
        super().__init__(access_token=access_token, session=session, host=host)

    def get_cde_jobs(self, query_params: CDEJobParams = None) -> list[CDEJob]:
        """Get (filter) Critical Data Manager jobs.

        Calls ``GET /cde-service/integration/job/``, following the CDE service's
        ``skip``/``limit`` pagination to return all matching jobs.

        Args:
            query_params (CDEJobParams): REST API GET filter values (e.g. ``type``,
                ``status``, ``order_by``).

        Returns:
            list[CDEJob]: The matching CDE jobs.

        Raises:
            requests.HTTPError: If the CDE API returns a non-success status code.

        """
        validate_query_params(query_params, CDEJobParams)
        params = query_params.generate_params_dict() if query_params else None

        jobs = self._cde_get(CDE_JOB_ENDPOINT, query_params=params)

        if jobs:
            return [CDEJob.from_api_response(job) for job in jobs]
        return []

    def get_cde_job(self, job_id: int) -> CDEJob:
        """Get a single Critical Data Manager job by its (integer) ID.

        Calls ``GET /cde-service/integration/job/{id}/``.

        Note:
            This endpoint takes the integer ``id``, not the uuid ``key`` returned by
            asynchronous write operations. To wait on a write by its ``key``, use
            :meth:`wait_for_cde_job`.

        Args:
            job_id (int): The CDE job ID.

        Returns:
            CDEJob: The requested CDE job.

        Raises:
            requests.HTTPError: If the CDE API returns a non-success status code.

        """
        job = self._cde_get(f"{CDE_JOB_ENDPOINT}{job_id}/", paginate=False)
        return CDEJob.from_api_response(job)

    def cancel_cde_job(self, job_id: int) -> None:
        """Cancel a Critical Data Manager job by its (integer) ID.

        Calls ``POST /cde-service/integration/job/{id}/cancel/``.

        Args:
            job_id (int): The CDE job ID.

        Raises:
            requests.HTTPError: If the CDE API returns a non-success status code.

        """
        self._cde_post(f"{CDE_JOB_ENDPOINT}{job_id}/cancel/")

    def wait_for_cde_job(self, job_key: str | int, poll_interval: int = 3,
                         timeout: float = 300,
                         job_type: str = "API_BULK_CREATION") -> CDEJob:
        """Block until the CDE job with the given ``key`` reaches a terminal state.

        Polls ``GET /cde-service/integration/job/`` and matches the uuid ``key``
        client-side (the list endpoint has no key filter). Terminal states are
        ``FINISHED`` / ``ERROR`` / ``CANCELED``.

        Args:
            job_key (str | int): The job ``key`` returned by an asynchronous write.
            poll_interval (int): Seconds to wait between polls.
            timeout (float): Maximum seconds to wait before raising. None disables it.
            job_type (str): CDE job ``type`` filter (e.g. ``API_BULK_CREATION``).

        Returns:
            CDEJob: The terminal job.

        Raises:
            TimeoutError: If the job does not reach a terminal state within ``timeout``.
            requests.HTTPError: If the CDE API returns a non-success status code.

        """
        terminal_job = self._wait_for_cde_job(
            job_key, poll_interval=poll_interval, timeout=timeout, job_type=job_type
        )
        return CDEJob.from_api_response(terminal_job)
