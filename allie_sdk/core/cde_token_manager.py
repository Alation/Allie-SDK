"""Manage shared, in-memory credentials for the Critical Data Manager APIs."""

import logging
from collections.abc import Callable

from ..models.cdm_authentication_model import CDEToken

LOGGER = logging.getLogger("allie_sdk_logger")


class CDETokenManager:
    """Cache one CDE token for the current Alation access token.

    The exchange callable is supplied by the authentication client so this core
    component does not depend on the methods package or perform HTTP requests.
    """

    def __init__(self, access_token: str | None = None) -> None:
        """Initialize an empty credential cache without exchanging a token.

        Args:
            access_token (str | None): Alation access token to exchange on first use.

        Returns:
            None: Initializes the in-memory credential state.
        """
        self._access_token = access_token
        self._cde_token: str | None = None

    @property
    def access_token(self) -> str | None:
        """Return the Alation credential shared by the CDE clients.

        Args:
            None.

        Returns:
            str | None: Current Alation access token.
        """
        return self._access_token

    @access_token.setter
    def access_token(self, token: str | None) -> None:
        """Discard cached CDE credentials when the Alation credential changes.

        Args:
            token (str | None): Replacement Alation token; empty values clear it.

        Returns:
            None: Updates the shared credential and invalidates a stale cache.
        """
        if token != self._access_token:
            self._access_token = token
            self._cde_token = None
            LOGGER.debug("Invalidated cached CDE credentials after an Alation token change.")

    def cache_token(self, alation_token: str, cde_token: str) -> None:
        """Cache an exchange result only when it belongs to the current credential.

        Args:
            alation_token (str): Alation credential used for the exchange.
            cde_token (str): Validated CDE token returned by the authentication API.

        Returns:
            None: Stores matching credentials; leaves other identities isolated.
        """
        if alation_token == self.access_token and cde_token != self._cde_token:
            self._cde_token = cde_token
            LOGGER.debug("Cached CDE credentials for the current Alation token.")

    def get_token(self, exchange_token: Callable[[str], CDEToken], force: bool = False) -> str:
        """Return cached credentials or delegate a token exchange on demand.

        Args:
            exchange_token (Callable[[str], CDEToken]): Authentication endpoint method.
            force (bool): Discard the cached token and exchange again when True.

        Returns:
            str: CDE token to use in the request header.

        Raises:
            ValueError: If no Alation token is configured.
            requests.HTTPError: If the delegated token exchange fails.
        """
        alation_token = self.access_token
        if not alation_token:
            error_message = (
                "No Alation API token available to exchange for a CDE token. "
                "Provide an alation_token argument or instantiate with an access_token."
            )
            LOGGER.error(error_message)
            raise ValueError(error_message)
        if force:
            self._cde_token = None
        cde_token = self._cde_token
        if not cde_token:
            LOGGER.debug("Exchanging Alation credentials for a CDE token.")
            response = exchange_token(alation_token)
            cde_token = response.token
            self.cache_token(alation_token, cde_token)
        return cde_token
