"""Alation Critical Data Manager (CDM / CDE) — Critical Data Element Methods."""

import logging
import requests

from ..core.cde_request_handler import CDERequestHandler, CDE_BASE
from ..core.custom_exceptions import validate_query_params, validate_rest_payload
from ..models.cde_job_model import CDEJob
from ..models.critical_data_element_model import (
    CriticalDataElement,
    CriticalDataElementItem,
    CriticalDataElementParams,
)

LOGGER = logging.getLogger("allie_sdk_logger")

CDE_ENDPOINT = f"{CDE_BASE}/cde/"
CDE_BULK_ENDPOINT = f"{CDE_BASE}/cde/bulk/"
CDE_BULK_DELETE_ENDPOINT = f"{CDE_BASE}/cde/bulk_delete/"

# The CDE bulk-create endpoint accepts at most 1000 elements per request.
CDE_BULK_MAX = 1000


class AlationCDMCriticalDataElement(CDERequestHandler):
    """Alation Critical Data Manager (CDM / CDE) Critical Data Element Methods.

    All calls authenticate via the CDE token flow inherited from
    :class:`~allie_sdk.core.cde_request_handler.CDERequestHandler` (the CDE token is
    minted lazily from the Alation access token on first use).
    """

    def __init__(self, access_token: str = None, session: requests.Session = None,
                 host: str = None):
        """Create an instance of the Critical Data Element object.

        Args:
            access_token (str, optional): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.

        """
        super().__init__(access_token=access_token, session=session, host=host)

    def get_critical_data_elements(
        self, query_params: CriticalDataElementParams = None
    ) -> list[CriticalDataElement]:
        """Get (filter) Alation Critical Data Elements.

        Calls ``GET /cde-service/integration/cde/``, following the CDE service's
        ``skip``/``limit`` pagination to return all matching elements.

        Args:
            query_params (CriticalDataElementParams): REST API GET filter values.

        Returns:
            list[CriticalDataElement]: The matching Critical Data Elements.

        Raises:
            requests.HTTPError: If the CDE API returns a non-success status code.

        """
        validate_query_params(query_params, CriticalDataElementParams)
        params = query_params.generate_params_dict() if query_params else None

        critical_data_elements = self._cde_get(CDE_ENDPOINT, query_params=params)

        if critical_data_elements:
            return [
                CriticalDataElement.from_api_response(cde)
                for cde in critical_data_elements
            ]
        return []

    def get_critical_data_element(self, cde_id: int) -> CriticalDataElement:
        """Get a single Alation Critical Data Element by its ID.

        Calls ``GET /cde-service/integration/cde/{id}/``.

        Args:
            cde_id (int): The Critical Data Element ID.

        Returns:
            CriticalDataElement: The requested Critical Data Element.

        Raises:
            requests.HTTPError: If the CDE API returns a non-success status code.

        """
        critical_data_element = self._cde_get(
            f"{CDE_ENDPOINT}{cde_id}/", paginate=False
        )
        return CriticalDataElement.from_api_response(critical_data_element)

    def create_critical_data_element(
        self, critical_data_element: CriticalDataElementItem
    ) -> CriticalDataElement:
        """Create a single Critical Data Element.

        Calls ``POST /cde-service/integration/cde/``.

        Args:
            critical_data_element (CriticalDataElementItem): The element to create
                (``name`` is required; ``status`` must be a creation status, e.g.
                ``CANDIDATE`` or ``DRAFT``).

        Returns:
            CriticalDataElement: The created Critical Data Element.

        Raises:
            InvalidPostBody: If the payload is missing required fields.
            UnsupportedPostBody: If the payload is not a CriticalDataElementItem.
            requests.HTTPError: If the CDE API returns a non-success status code.

        """
        validate_rest_payload([critical_data_element], (CriticalDataElementItem,))
        payload = critical_data_element.generate_api_post_payload()

        created = self._cde_post(CDE_ENDPOINT, body=payload)
        return CriticalDataElement.from_api_response(created)

    def create_critical_data_elements_bulk(
        self,
        critical_data_elements: list[CriticalDataElementItem],
        allow_duplicates: bool = False,
        wait_for_completion: bool = True,
        poll_interval: int = 3,
        timeout: float = 300,
    ) -> CDEJob | str:
        """Create multiple Critical Data Elements in a single asynchronous request.

        Calls ``POST /cde-service/integration/cde/bulk/`` (up to 1000 elements). The
        endpoint runs asynchronously and returns a job ``key``.

        Args:
            critical_data_elements (list[CriticalDataElementItem]): The elements to
                create (max 1000).
            allow_duplicates (bool): Whether the server may create elements whose names
                duplicate existing ones.
            wait_for_completion (bool): If True (default), block until the job reaches a
                terminal state and return the resulting :class:`CDEJob`. If False, return
                the job ``key`` immediately.
            poll_interval (int): Seconds between polls while waiting.
            timeout (float): Maximum seconds to wait before raising. None disables it.

        Returns:
            CDEJob | str: The terminal :class:`CDEJob` (when waiting) or the job ``key``.

        Raises:
            ValueError: If more than 1000 elements are supplied, or no job key is returned.
            UnsupportedPostBody: If the payload contains non-CriticalDataElementItem items.
            TimeoutError: If the job does not complete within ``timeout`` (when waiting).
            requests.HTTPError: If the CDE API returns a non-success status code.

        """
        validate_rest_payload(critical_data_elements, (CriticalDataElementItem,))
        if len(critical_data_elements) > CDE_BULK_MAX:
            raise ValueError(
                f"The CDE bulk-create endpoint accepts at most {CDE_BULK_MAX} elements "
                f"per request; {len(critical_data_elements)} were supplied. Split them "
                f"into batches of {CDE_BULK_MAX} or fewer."
            )

        payload = {
            "cdes": [item.generate_api_post_payload() for item in critical_data_elements],
            "options": {"allow_duplicates": allow_duplicates},
        }

        response = self._cde_post(CDE_BULK_ENDPOINT, body=payload)
        job_key = self._extract_job_key(response)
        if job_key is None:
            error_message = (
                "The CDE bulk-create endpoint returned a success status but no job key "
                f"could be parsed from the response: {response!r}"
            )
            LOGGER.error(error_message)
            raise ValueError(error_message)

        if not wait_for_completion:
            return job_key

        terminal_job = self._wait_for_cde_job(
            job_key, poll_interval=poll_interval, timeout=timeout
        )
        return CDEJob.from_api_response(terminal_job)

    def update_critical_data_element(
        self, cde_id: int, critical_data_element: CriticalDataElementItem
    ) -> CriticalDataElement:
        """Update an existing Critical Data Element.

        Calls ``PUT /cde-service/integration/cde/{id}/`` with the fields to change. The
        endpoint runs synchronously and returns the updated element.

        Note:
            ``status`` is not an update field (use the CDE status-transition endpoint to
            change status); it is ignored even if set on the item.

        Args:
            cde_id (int): The Critical Data Element ID to update.
            critical_data_element (CriticalDataElementItem): The fields to change
                (``name`` / ``description``).

        Returns:
            CriticalDataElement: The updated Critical Data Element.

        Raises:
            UnsupportedPostBody: If the payload is not a CriticalDataElementItem.
            requests.HTTPError: If the CDE API returns a non-success status code.

        """
        validate_rest_payload([critical_data_element], (CriticalDataElementItem,))
        payload = critical_data_element.generate_api_put_payload()

        updated = self._cde_put(f"{CDE_ENDPOINT}{cde_id}/", body=payload)
        return CriticalDataElement.from_api_response(updated)

    def delete_critical_data_element(self, cde_id: int) -> None:
        """Delete a single Critical Data Element by its ID.

        Calls ``DELETE /cde-service/integration/cde/{id}/``.

        Args:
            cde_id (int): The Critical Data Element ID.

        Raises:
            requests.HTTPError: If the CDE API returns a non-success status code.

        """
        self._cde_delete(f"{CDE_ENDPOINT}{cde_id}/")

    def delete_critical_data_elements_bulk(self, cde_ids: list[int]) -> None:
        """Delete multiple Critical Data Elements by ID in a single request.

        Calls ``POST /cde-service/integration/cde/bulk_delete/`` with a body of
        ``{"ids": [...]}``. The endpoint runs synchronously.

        Args:
            cde_ids (list[int]): The IDs of the Critical Data Elements to delete.

        Raises:
            ValueError: If ``cde_ids`` is empty.
            requests.HTTPError: If the CDE API returns a non-success status code.

        """
        if not cde_ids:
            raise ValueError("cde_ids must contain at least one Critical Data Element ID.")

        self._cde_post(CDE_BULK_DELETE_ENDPOINT, body={"ids": list(cde_ids)})
