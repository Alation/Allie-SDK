"""Alation Critical Data Manager (CDM / CDE) API Authentication Methods."""

import logging

import requests

from ..core.cde_token_manager import CDETokenManager
from ..core.request_handler import SUCCESS_CODES, RequestHandler
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

    def __init__(self, access_token: str | None = None, session: requests.Session | None = None,
                 host: str | None = None, token_manager: CDETokenManager | None = None) -> None:
        """Create an instance of the CDM Authentication object.

        Args:
            access_token (str, optional): Alation REST API Access Token to exchange for a
                CDE token. Can be overridden per-call in :meth:`create_cde_token`.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.
            token_manager (CDETokenManager | None): Shared credential cache. A standalone
                client creates an isolated manager when omitted. A supplied access_token
                must match the manager's credential.

        Returns:
            None: Initializes the exchange client and its credential manager.

        Raises:
            ValueError: If access_token conflicts with the supplied manager's credential.
        """
        if token_manager is not None and access_token is not None and access_token != token_manager.access_token:
            error_message = "access_token must match the shared CDE token manager's credential."
            LOGGER.error(error_message)
            raise ValueError(error_message)
        self._token_manager = token_manager if token_manager is not None else CDETokenManager(access_token)
        super().__init__(session=session, host=host, access_token=self._token_manager.access_token)

    @property
    def access_token(self) -> str | None:
        """Return the Alation credential from the shared manager.

        Args:
            None.

        Returns:
            str | None: Current Alation access token.
        """
        return self._token_manager.access_token

    @access_token.setter
    def access_token(self, token: str | None) -> None:
        """Update shared credentials and this client's default headers.

        Args:
            token (str | None): Replacement Alation access token.

        Returns:
            None: Invalidates cached CDE credentials when the token changes.
        """
        self._token_manager.access_token = token
        RequestHandler.access_token.fset(self, token)

    def create_cde_token(self, alation_token: str | None = None) -> CDEToken:
        """Exchange an Alation API token for a CDE (Critical Data Manager) token.

        Calls ``POST /cde-service/integration/auth/`` passing the Alation API token in
        the ``token`` request header. The endpoint returns a plain-string CDE token that
        is valid for 24 hours.

        Args:
            alation_token (str, optional): Alation API token (refresh or access token) to
                exchange. Defaults to the access token this instance was created with.

        Returns:
            CDEToken: The CDE token (valid for 24 hours from creation).
                Exchanges for the configured Alation token also update the shared cache.
                Exchanges for another token do not replace the configured credentials.

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

        # Override default authentication and retain the bodyless exchange request.
        api_response = self._request(
            "POST", self.host + CDE_AUTH_ENDPOINT,
            headers={"token": token_to_exchange, "Content-Type": None},
        )

        if api_response.status_code not in SUCCESS_CODES:
            self._log_response(api_response, "POST")
            api_response.raise_for_status()

        # The endpoint returns the CDE token as a plain string. Some deployments may
        # JSON-encode it (a quoted string), so handle both shapes robustly.
        parsed_response = self._parse_response(api_response)
        cde_token_value = parsed_response if isinstance(parsed_response, str) else None

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

        self._log_response(api_response, "POST")

        self._token_manager.cache_token(token_to_exchange, cde_token_value)
        return CDEToken(token=cde_token_value)
