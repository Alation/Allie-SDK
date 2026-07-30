"""Alation Critical Data Manager (CDM / CDE) API Authentication Methods."""

import logging
import requests

from ..core.request_handler import RequestHandler, SUCCESS_CODES
from ..models.cdm_authentication_model import CDEToken

LOGGER = logging.getLogger("allie_sdk_logger")

# The CDE service uses a different authentication flow from all other Alation APIs.
# Step 1: exchange an Alation API token for a CDE token at this endpoint.
# See: https://developer.alation.com/dev/reference/cde-api-overview
CDE_AUTH_ENDPOINT = "/cde-service/integration/auth/"


class AlationCDMAuthentication(RequestHandler):
    """Alation Critical Data Manager (CDM / CDE) API Authentication Methods.

    The CDE API uses a dedicated authentication flow that differs from all other
    Alation APIs. An existing Alation API token (refresh or access token) is exchanged
    for a short-lived CDE token, which is then passed in the ``CDEToken`` request header
    for all subsequent CDE API calls.
    """

    def __init__(self, access_token: str = None, session: requests.Session = None,
                 host: str = None):
        """Create an instance of the CDM Authentication object.

        Args:
            access_token (str, optional): Alation REST API Access Token to exchange for a
                CDE token. Can be overridden per-call in :meth:`create_cde_token`.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.

        """
        super().__init__(session=session, host=host, access_token=access_token)

    def create_cde_token(self, alation_token: str = None) -> CDEToken:
        """Exchange an Alation API token for a CDE (Critical Data Manager) token.

        Calls ``POST /cde-service/integration/auth/`` passing the Alation API token in
        the ``token`` request header. The endpoint returns a plain-string CDE token that
        is valid for 24 hours.

        Args:
            alation_token (str, optional): Alation API token (refresh or access token) to
                exchange. Defaults to the access token this instance was created with.

        Returns:
            CDEToken: The CDE token (valid for 24 hours from creation).

        Raises:
            ValueError: If no Alation token is available to exchange.
            requests.HTTPError: If the CDE auth endpoint returns a non-success status code.
        """
        token_to_exchange = alation_token if alation_token else self.access_token
        if not token_to_exchange:
            error_message = (
                "No Alation API token available to exchange for a CDE token. "
                "Provide an alation_token argument or instantiate with an access_token."
            )
            LOGGER.error(error_message)
            raise ValueError(error_message)

        # The CDE auth endpoint expects the Alation token under the lower-case "token"
        # header key. It must NOT go through the standard request helpers, which inject
        # the "Token" header used by every other Alation API.
        request_url = self.host + CDE_AUTH_ENDPOINT
        api_response = self.s.post(request_url, headers={"token": token_to_exchange})

        log_url = self._format_log_url(api_response.url)
        log_details = {
            "Method": "POST",
            "URL": api_response.url,
            "Response": api_response.status_code,
        }

        if api_response.status_code not in SUCCESS_CODES:
            try:
                error_data = api_response.json()
            except requests.exceptions.JSONDecodeError:
                error_data = api_response.text
            self._log_error(
                error_data,
                log_details,
                message=f"Error exchanging the Alation token for a CDE token at: {log_url}",
            )
            api_response.raise_for_status()

        # The endpoint returns the CDE token as a plain string. Some deployments may
        # JSON-encode it (a quoted string), so handle both shapes robustly.
        try:
            parsed_response = api_response.json()
            cde_token_value = parsed_response if isinstance(parsed_response, str) else None
        except requests.exceptions.JSONDecodeError:
            cde_token_value = api_response.text

        if isinstance(cde_token_value, str):
            cde_token_value = cde_token_value.strip()

        if not cde_token_value:
            error_message = (
                "The CDE auth endpoint returned a success status but no token could be "
                f"parsed from the response: {api_response.text!r}"
            )
            LOGGER.error(error_message)
            error_response = requests.Response()
            error_response.status_code = 500
            error_response._content = str.encode(error_message)
            raise requests.exceptions.HTTPError(error_message, response=error_response)

        self._log_success(
            log_details,
            message=f"Successfully exchanged the Alation token for a CDE token at: {log_url}",
        )

        return CDEToken(token=cde_token_value)
