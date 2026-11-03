"""Alation Critical Data Manager (CDM / CDE) — Critical Data Element Methods."""

import logging
import requests

from ..core.cde_request_handler import CDERequestHandler, CDE_BASE
from ..core.custom_exceptions import validate_query_params
from ..models.critical_data_element_model import (
    CriticalDataElement,
    CriticalDataElementParams,
)

LOGGER = logging.getLogger("allie_sdk_logger")

CDE_ENDPOINT = f"{CDE_BASE}/cde/"


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
