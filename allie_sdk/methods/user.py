"""Alation REST API User Methods."""

import logging
import requests

from ..core.request_handler import RequestHandler
from ..core.custom_exceptions import validate_query_params
from ..models.user_model import *

LOGGER = logging.getLogger('allie_sdk_logger')


class AlationUser(RequestHandler):
    """Alation REST API User Methods."""

    def __init__(self, access_token: str, session: requests.Session,
                 host: str, use_v2_endpoint: bool = True):
        """Creates an instance of the User object.

        Args:
            access_token (str): Alation REST API Access Token.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
            use_v2_endpoint (bool): Use the Alation REST API V2 User Endpoint.

        """
        super().__init__(session, host, access_token=access_token)

        self._use_v2_endpoint = use_v2_endpoint

        if self._use_v2_endpoint:
            self._user_endpoint = '/integration/v2/user/'
        else:
            self._user_endpoint = '/integration/v1/user/'

    def get_users(self, query_params: UserParams = None) -> list:
        """Get multiple Alation Users.

        Args:
            query_params (UserParams): REST API Get Filter Values.

        Returns:
            list: Alation Users

        """
        validate_query_params(query_params, UserParams)
        params = query_params.generate_params_dict() if query_params else None
        users = self.get(self.user_endpoint, query_params=params)

        if users:
            return [User.from_api_response(user) for user in users]

    def get_a_user(self, user_id: int) -> User:
        """Get an Alation User by User ID.

        Args:
            user_id (int): Alation User ID.

        Returns:
            User: Alation User.

        """
        user = self.get(f'{self.user_endpoint}{user_id}/')

        if user:
            return User.from_api_response(user)

    def get_authenticated_user(self) -> User:
        """Get the Details of the Authenticated Alation User.

        Returns:
            User: Authenticated Alation User Details.

        """
        details = self.get('/integration/v1/userinfo/')

        if details:
            return User.from_api_response(details)

    def post_remove_dup_users_accts(self, csv_file: str) -> str:
        """Post CSV to remove duplicate Alation Users.

        Returns:
            status: Confirmation of the removal of duplicate users

        """
        files = {"csv_file": (csv_file, open(csv_file, "rb"), "text/plain")}
        result = self.post('/integration/v1/remove_dup_users_accts/', files=files, body=None,
                           headers={"accept": "application/json"})

        return result

    def get_generate_dup_users_accts_csv(self) -> str:
        """Get duplicate Alation Users as CSV.

        Returns:
            list: CSV of duplicate Alation Users With headings

        """
        result = self.get('/integration/v1/generate_dup_users_accts_csv_file/')

        return result


    @property
    def use_v2_endpoint(self) -> bool:
        """Return the Bool Config to use the Alation REST API V2 User Endpoint.

        Returns:
            bool: Config to use the Alation REST API V2 User Endpoint.

        """
        return self._use_v2_endpoint

    @use_v2_endpoint.setter
    def use_v2_endpoint(self, config: bool):
        """Set the Bool Config to use the Alation REST API V2 User Endpoint.

        Args:
            config (bool): Config to use the Alation REST API V2 User Endpoint.

        """
        if config:
            self._user_endpoint = '/integration/v2/user/'
        else:
            self._user_endpoint = '/integration/v1/user/'

        self._use_v2_endpoint = config

    @property
    def user_endpoint(self) -> str:
        """Return the Alation REST API User Endpoint URL.

        Returns:
            str: Alation REST API User Endpoint URL.

        """
        return self._user_endpoint
