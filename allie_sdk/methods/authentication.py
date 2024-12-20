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

    def validate_refresh_token(self, refresh_token = None) -> RefreshToken | JobDetails:
        """Validate the Alation API Refresh Token.

        Returns:
            RefreshToken: Alation API Refresh Token if request succeeded
            JobDetails: Error details if request fails

        """
        ref_token = refresh_token if refresh_token else self.refresh_token

        validate_body = {
            'refresh_token': ref_token
            , 'user_id': self.user_id
        }

        validity = self.post('/integration/v1/validateRefreshToken/',
                             validate_body)

        if validity:
            # cater for error messages
            # check if the dict contains a status property
            status = validity.get("status")
            if status:
                if status == "failed":
                    return JobDetails.from_api_response(validity)
            else:
                return RefreshToken.from_api_response(validity)

    def create_access_token(self) -> AccessToken | JobDetails:
        """Create an Alation API Access Token.

        Returns:
            AccessToken: Alation API Access Token.

        """
        validate_refresh_token_response = self.validate_refresh_token()

        # Case: There was some other error validating the refresh token
        if isinstance(validate_refresh_token_response, JobDetails):
            # just pass on the error message
            # it's already in the JobDetails structure
            return validate_refresh_token_response

        # Case: A RefreshToken object is returned
        elif isinstance(validate_refresh_token_response, RefreshToken):
            # Case: Refresh token is expired
            if validate_refresh_token_response.token_status.upper() != 'ACTIVE':
                validation_error_message = "The Refresh Token is expired! Please generate a new refresh token and try again."
                LOGGER.error(validation_error_message)

                # make it conform to JobDetails structure
                mapped_response = self._map_request_error_to_job_details(validation_error_message)
                return JobDetails.from_api_response(mapped_response)
            # Case: We've got a valid refresh token and can proceed with creating a new access token
            else:
                token_body = {'refresh_token': self.refresh_token,
                              'user_id': self.user_id}
                token = self.post('/integration/v1/createAPIAccessToken/',
                                  token_body)

                if token:
                    # cater for error messages
                    # check if the dict contains a status property
                    status = token.get("status")
                    if status:
                        if status == "failed":
                            return JobDetails.from_api_response(token)
                    else:
                        return AccessToken.from_api_response(token)

    def validate_access_token(self, access_token: str) -> AccessToken | JobDetails:
        """Validate the Alation API Access Token.

        Args:
            access_token (str): Alation API Access Token.

        Returns:
            AccessToken: Alation API Access Token if request is successful
            JobDetails: Error details if request fails

        """
        validate_body = {
            'api_access_token': access_token
            , 'user_id': self.user_id
        }

        validity = self.post(
            url = '/integration/v1/validateAPIAccessToken/'
            , body = validate_body
        )

        if validity:
            # cater for error messages
            # check if the dict contains a status property
            status = validity.get("status")
            if status:
                if status == "failed":
                    return JobDetails.from_api_response(validity)
            else:
                return AccessToken.from_api_response(validity)

    def revoke_access_tokens(self) -> JobDetails:
        """Revoke the Alation API Access Tokens of an Alation API Refresh Token.

        Returns:
            bool: Result of the API Call to Revoke Access Tokens.

        """
        revoke_body = {'refresh_token': self.refresh_token,
                       'user_id': self.user_id}
        revoke_response = self.post(
            url = '/integration/v1/revokeAPIAccessTokens/'
            , body = revoke_body
        )


        if revoke_response:
            # check whether it was a success or failure
            status = revoke_response.get("status")
            if status:
                if status == "failed":
                    return JobDetails.from_api_response(revoke_response)
            else:
                mapped_revoke_response = self._map_request_success_to_job_details(revoke_response)
                return JobDetails.from_api_response(mapped_revoke_response)


