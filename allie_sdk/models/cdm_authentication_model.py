"""Alation Critical Data Manager (CDM / CDE) API Authentication Data Models."""

from dataclasses import dataclass, field

from ..core.data_structures import BaseClass


@dataclass
class CDEToken(BaseClass):
    """CDE (Critical Data Manager) API token.

    Obtained by exchanging an Alation API token (refresh or access token) at the
    CDE auth endpoint. The CDE token is a plain string that must be passed in the
    ``CDEToken`` request header for all subsequent CDE API calls, and is valid for
    24 hours from creation.

    See: https://developer.alation.com/dev/reference/cde-api-overview
    """
    token: str = field(default=None)
