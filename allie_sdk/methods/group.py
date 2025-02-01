"""Alation REST API Group Methods."""

import logging
import requests

from ..core.request_handler import RequestHandler
from ..core.custom_exceptions import validate_query_params
from ..models.group_model import *

class AlationGroup(RequestHandler):
    """Alation REST API Business Policy Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the Business Policy  object.
        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
        """
        super().__init__(session = session, host = host, access_token = access_token)

    def get_groups(self, query_params:GroupParams = None) -> list[Group]:
        """Get Alation groups.

        Args:
            query_params (GroupParams, optional): Query parameters for filtering groups. Defaults to None.

        Returns:
            list[Group]: List of Alation groups.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        validate_query_params(query_params, GroupParams)
        params = query_params.generate_params_dict() if query_params else None

        groups = self.get(url = '/integration/v1/group/', query_params = params)

        if groups:
            groups_checked = [Group.from_api_response(g) for g in groups]
            return groups_checked
        return []