"""Alation REST API Authentication Methods."""

import logging
import base64
import requests

from ..core.request_handler import RequestHandler
from ..models.authentication_model import *
from ..models.job_model import *

LOGGER = logging.getLogger('allie_sdk_logger')


class AlationAuthentication(RequestHandler):
    """Alation REST API Authentication Methods."""

    def __init__(self, refresh_token: str = None, user_id: int = None,
                 session: requests.Session = None, host: str = None,
                 client_id: str = None, client_secret: str = None):
        """Create an instance of the Authentication object.

        Args:
            refresh_token (str, optional): Alation REST API Refresh Token.
            user_id (int, optional): Alation User ID.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
            client_id (str, optional): OAuth client ID.
            client_secret (str, optional): OAuth client secret.

        """
        super().__init__(session, host)

        self.refresh_token = refresh_token
        self.user_id = user_id
        self.client_id = client_id
        self.client_secret = client_secret

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

    def create_oauth_token(self, client_credentials: OAuthCredentials = None,
                          use_basic_auth: bool = True) -> OAuthToken:
        """Create an OAuth JWT access token using client_credentials grant type.

        Args:
            client_credentials (OAuthCredentials, optional): OAuth client credentials.
                If not provided, uses the client_id and client_secret from the constructor.
            use_basic_auth (bool): Whether to use Basic authentication header.
                If False, sends credentials in request body. Defaults to True.

        Returns:
            OAuthToken: OAuth JWT access token with metadata.

        Raises:
            requests.HTTPError: If the API returns a non-success status code.
            ValueError: If client credentials are not provided.
        """
        # Get credentials from parameter or instance variables
        if client_credentials:
            client_id = client_credentials.client_id
            client_secret = client_credentials.client_secret
        else:
            client_id = self.client_id
            client_secret = self.client_secret
        if not client_id or not client_secret:
            raise ValueError("Client ID and client secret are required for OAuth authentication")
        # Prepare request body
        token_body = {'grant_type': 'client_credentials'}
        # Prepare headers
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        if use_basic_auth:
            # Use Basic authentication header
            credentials = f"{client_id}:{client_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            headers['Authorization'] = f"Basic {encoded_credentials}"
        else:
            # Include credentials in request body
            token_body['client_id'] = client_id
            token_body['client_secret'] = client_secret
        LOGGER.info("Creating OAuth token using client_credentials grant type")
        # Make request with the token body dict
        token_response = self.post(
            url='/oauth/v2/token',
            body=token_body,
            headers=headers
        )
        # Check for OAuth-specific errors in the response
        if isinstance(token_response, dict):
            if 'error' in token_response:
                error_msg = f"OAuth token creation failed: {token_response.get('error', 'Unknown error')}"
                if 'error_description' in token_response:
                    error_msg += f" - {token_response['error_description']}"
                LOGGER.error(error_msg)
                
                # Convert OAuth error to HTTPError with appropriate status code
                error_response = requests.Response()
                error_response.status_code = 400  # Bad request for OAuth errors
                error_response._content = str.encode(str(token_response))
                error = requests.exceptions.HTTPError(error_msg, response=error_response)
                raise error
            else:
                LOGGER.info("OAuth token created successfully")
        return OAuthToken.from_api_response(token_response)


