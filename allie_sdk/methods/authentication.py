"""Alation REST API Authentication Methods."""

import logging
import requests

from ..core.request_handler import RequestHandler
from ..models.authentication_model import *
from ..models.job_model import *

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

    def validate_refresh_token(self, refresh_token = None) -> RefreshToken:
        """Validate the Alation API Refresh Token.

        Args:
            refresh_token (str, optional): Alation API Refresh Token. Defaults to None.

        Returns:
            RefreshToken: Alation API Refresh Token

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        ref_token = refresh_token if refresh_token else self.refresh_token

        validate_body = {
            'refresh_token': ref_token
            , 'user_id': self.user_id
        }

        validity = self.post('/integration/v1/validateRefreshToken/', validate_body)

        # API can return success but with a status="failed" in the body for logical errors
        # This is distinct from HTTP errors which are raised by RequestHandler
        status = validity.get("status")
        if status and status == "failed":
            # Convert to HTTPError with appropriate status code
            error_response = requests.Response()
            error_response.status_code = 400  # Bad request
            error_response._content = str.encode(str(validity))
            error = requests.exceptions.HTTPError("Refresh token validation failed", response=error_response)
            raise error

        return RefreshToken.from_api_response(validity)

    def create_access_token(self) -> AccessToken:
        """Create an Alation API Access Token.

        Returns:
            AccessToken: Alation API Access Token.

        Raises:
            requests.HTTPError: If the API returns a non-success status code or if refresh token is invalid.
        """
        # This will raise HTTPError if the token is invalid
        refresh_token_validation = self.validate_refresh_token()
        
        # Check if refresh token is expired
        if refresh_token_validation.token_status.upper() != 'ACTIVE':
            validation_error_message = "The Refresh Token is expired! Please generate a new refresh token and try again."
            LOGGER.error(validation_error_message)
            
            # Create and raise an HTTP error
            error_response = requests.Response()
            error_response.status_code = 401  # Unauthorized
            error_response._content = str.encode(validation_error_message)
            error = requests.exceptions.HTTPError(validation_error_message, response=error_response)
            raise error
            
        # Create access token
        token_body = {'refresh_token': self.refresh_token, 'user_id': self.user_id}
        token = self.post('/integration/v1/createAPIAccessToken/', token_body)
        
        # API can return success but with a status="failed" in the body for logical errors
        status = token.get("status")
        if status and status == "failed":
            # Convert to HTTPError with appropriate status code
            error_response = requests.Response()
            error_response.status_code = 400  # Bad request
            error_response._content = str.encode(str(token))
            error = requests.exceptions.HTTPError("Access token creation failed", response=error_response)
            raise error
            
        return AccessToken.from_api_response(token)

    def validate_access_token(self, access_token: str) -> AccessToken:
        """Validate the Alation API Access Token.

        Args:
            access_token (str): Alation API Access Token.

        Returns:
            AccessToken: Alation API Access Token

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        validate_body = {
            'api_access_token': access_token
            , 'user_id': self.user_id
        }

        validity = self.post(
            url = '/integration/v1/validateAPIAccessToken/'
            , body = validate_body
        )

        # API can return success but with a status="failed" in the body for logical errors
        status = validity.get("status")
        if status and status == "failed":
            # Convert to HTTPError with appropriate status code
            error_response = requests.Response()
            error_response.status_code = 401  # Unauthorized
            error_response._content = str.encode(str(validity))
            error = requests.exceptions.HTTPError("Access token validation failed", response=error_response)
            raise error

        return AccessToken.from_api_response(validity)

    def revoke_access_tokens(self) -> JobDetails:
        """Revoke the Alation API Access Tokens of an Alation API Refresh Token.

        Returns:
            JobDetails: Result of the API Call to Revoke Access Tokens.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
        """
        revoke_body = {'refresh_token': self.refresh_token,
                      'user_id': self.user_id}
        
        revoke_response = self.post(
            url = '/integration/v1/revokeAPIAccessTokens/'
            , body = revoke_body
        )

        # API can return success but with a status="failed" in the body for logical errors
        status = revoke_response.get("status")
        if status and status == "failed":
            # Convert to HTTPError with appropriate status code
            error_response = requests.Response()
            error_response.status_code = 400  # Bad request
            error_response._content = str.encode(str(revoke_response))
            error = requests.exceptions.HTTPError("Token revocation failed", response=error_response)
            raise error

        # Map the response to a JobDetails structure for backward compatibility
        mapped_revoke_response = self._map_request_success_to_job_details(revoke_response)
        return JobDetails.from_api_response(mapped_revoke_response)


