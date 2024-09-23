"""Alation REST API Authentication Methods."""

import logging
import requests

from ..core.request_handler import RequestHandler
from ..models.authentication_model import *

LOGGER = logging.getLogger('allie_sdk_logger')


class AlationAuthentication(RequestHandler):
    """Alation REST API Authentication Methods."""

    def __init__(self, refresh_token: str, user_id: int,
                 session: requests.Session, host: str):
        """Create an instance of the Authentication object.

        Args:
            refresh_token (str): Alation REST API Refresh Token.
            user_id (int): Alation User ID.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.

        """
        super().__init__(session, host)

        self.refresh_token = refresh_token
        self.user_id = user_id

    def validate_refresh_token(self) -> RefreshToken:
        """Validate the Alation API Refresh Token.

        Returns:
            RefreshToken: Alation API Refresh Token.

        """
        validate_body = {
            'refresh_token': self.refresh_token
            , 'user_id': self.user_id
        }

        validity = self.post('/integration/v1/validateRefreshToken/',
                             validate_body)

        if validity:
            return RefreshToken.from_api_response(validity)

    def create_access_token(self) -> AccessToken:
        """Create an Alation API Access Token.

        Returns:
            AccessToken: Alation API Access Token.

        """
        refresh_status = self.validate_refresh_token()

        if refresh_status.token_status.upper() != 'ACTIVE':
            LOGGER.error("The Refresh Token is expired! Please generate a new"
                         " refresh token and try again.")

        else:
            token_body = {'refresh_token': self.refresh_token,
                          'user_id': self.user_id}
            token = self.post('/integration/v1/createAPIAccessToken/',
                              token_body)

            if token:
                return AccessToken.from_api_response(token)

    def validate_access_token(self, access_token: str) -> AccessToken:
        """Validate the Alation API Access Token.

        Args:
            access_token (str): Alation API Access Token.

        Returns:
            AccessToken: Alation API Access Token.

        """
        validate_body = {'api_access_token': access_token,
                         'user_id': self.user_id}
        validity = self.post('/integration/v1/validateAPIAccessToken/',
                             validate_body)

        if validity:
            return AccessToken.from_api_response(validity)

    def revoke_access_tokens(self) -> bool:
        """Revoke the Alation API Access Tokens of an Alation API Refresh Token.

        Returns:
            bool: Result of the API Call to Revoke Access Tokens.

        """
        revoke_body = {'refresh_token': self.refresh_token,
                       'user_id': self.user_id}
        revoke = self.post('/integration/v1/revokeAPIAccessTokens/',
                           revoke_body)

        return True if revoke else False
