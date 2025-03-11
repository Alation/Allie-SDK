"""Alation REST API Otype Methods."""

import logging
import requests

from ..core.async_handler import AsyncHandler
from ..models.otype_model import Otype

LOGGER = logging.getLogger('allie_sdk_logger')


class AlationOtype(AsyncHandler):
    """Alation REST API Glossary Term Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the AlationOtype object.

        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.

        """
        super().__init__(access_token, session, host)

    def get_otypes(self) -> list[Otype]:
        """Get the details of all allowed Alation Otypes.

        Returns:
            list: Allowed Alation Otypes

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        otypes = self.get('/integration/v1/otype/')

        if otypes:
            return [Otype.from_api_response(otype) for otype in otypes]
        return []


