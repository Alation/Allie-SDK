"""Alation OAuth 2.0 API methods."""

import logging
from dataclasses import asdict
from urllib.parse import urlencode

import requests

from ..core.request_handler import RequestHandler, SUCCESS_CODES
from ..models.oauth2_model import (
    ActiveIntrospectTokenResponse,
    ClientCredentialsGrantRequestPayload,
    InactiveIntrospectTokenResponse,
    JWKSetResponse,
    TokenIntrospectRequestPayload,
    TokenResponse,
)

LOGGER = logging.getLogger('allie_sdk_logger')


class AlationOAuth2(RequestHandler):
    """Methods for interacting with the OAuth 2.0 API v2."""

    def __init__(self, session: requests.Session, host: str):
        super().__init__(session=session, host=host)

    def create_token(
        self,
        payload: ClientCredentialsGrantRequestPayload,
        auth: tuple[str, str] | None = None,
    ) -> TokenResponse:
        """Create a JSON web token (JWT) using the client credentials grant."""

        data = urlencode({k: v for k, v in asdict(payload).items() if v is not None})
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        api_response = self.s.post(
            self.host + '/oauth/v2/token/', data=data, headers=headers, auth=auth
        )

        log_url = self._format_log_url(api_response.url)
        log_details = {
            'Method': 'POST',
            'URL': api_response.url,
            'Response': api_response.status_code,
        }

        try:
            response_data = api_response.json()
        except requests.exceptions.JSONDecodeError:
            response_data = api_response.text

        if api_response.status_code not in SUCCESS_CODES:
            self._log_error(
                response_data,
                log_details,
                message=f'Error submitting the POST Request to: {log_url}',
            )
            api_response.raise_for_status()

        self._log_success(
            log_details,
            message=f'Successfully submitted the POST Request to: {log_url}',
        )

        return TokenResponse.from_api_response(response_data)

    def introspect_token(
        self,
        payload: TokenIntrospectRequestPayload,
        verify_token: bool = False,
        auth: tuple[str, str] | None = None,
    ):
        """Introspect a JSON web token (JWT)."""

        params = {'verify_token': str(verify_token).lower()} if verify_token else None
        data = urlencode({k: v for k, v in asdict(payload).items() if v is not None})
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        api_response = self.s.post(
            self.host + '/oauth/v2/introspect/',
            data=data,
            params=params,
            headers=headers,
            auth=auth,
        )

        log_url = self._format_log_url(api_response.url)
        log_details = {
            'Method': 'POST',
            'URL': api_response.url,
            'Response': api_response.status_code,
        }

        try:
            response_data = api_response.json()
        except requests.exceptions.JSONDecodeError:
            response_data = api_response.text

        if api_response.status_code not in SUCCESS_CODES:
            self._log_error(
                response_data,
                log_details,
                message=f'Error submitting the POST Request to: {log_url}',
            )
            api_response.raise_for_status()

        self._log_success(
            log_details,
            message=f'Successfully submitted the POST Request to: {log_url}',
        )

        if response_data.get('active'):
            return ActiveIntrospectTokenResponse.from_api_response(response_data)
        return InactiveIntrospectTokenResponse.from_api_response(response_data)

    def get_jwks(self) -> JWKSetResponse:
        """Retrieve the JSON Web Key Set (JWKS)."""

        jwks = self.get('/oauth/v2/.well-known/jwks.json/', pagination=False)
        return JWKSetResponse.from_api_response(jwks)

