"""Alation REST API Connectors Methods."""

import logging
import requests

from ..core.async_handler import AsyncHandler
from ..models.connector_model import Connector

LOGGER = logging.getLogger('allie_sdk_logger')


class AlationConnector(AsyncHandler):
    """Alation REST API Connectors Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the Connector object.

        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.

        """
        super().__init__(access_token, session, host)

    def get_connectors(self) -> list[Connector]:
        """Get the details of all Installed OCF Connectors.

        Returns:
            list[Connector]: Installed OCF Connectors
            
        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        connectors = self.get('/integration/v2/connectors/')

        if connectors:
            return [Connector.from_api_response(connector) for connector in connectors]
        return []


