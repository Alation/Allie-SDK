"""Alation REST API Policies Methods."""

import logging
import requests

from ..core.request_handler import RequestHandler
from ..core.custom_exceptions import *
from ..models.policy_group_model import *

LOGGER = logging.getLogger('allie_sdk_logger')

class AlationPolicyGroup(RequestHandler):
    """Alation REST API Business Policy Methods."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Creates an instance of the Policy Group  object.
        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
        """
        super().__init__(session = session, host = host, access_token = access_token)

    def get_policy_groups(
            self
            , query_params: PolicyGroupParams = None
        ) -> list[PolicyGroup]:
        """Get policy groups.

        Args:
            query_params (PolicyGroupParams): REST API Get Filter Values.

        Returns:
            list[PolicyGroup]: List of policy groups.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        validate_query_params(query_params, PolicyGroupParams)
        params = query_params.generate_params_dict() if query_params else None

        # Note: The policy group API endpoint does not have a trailing slash! It won't work with one. Status: Jan 2024
        policy_groups = self.get('/integration/v1/policy_group', query_params = params)

        if policy_groups:
            policy_groups_result = [PolicyGroup.from_api_response(pg) for pg in policy_groups]
            return policy_groups_result
        return []