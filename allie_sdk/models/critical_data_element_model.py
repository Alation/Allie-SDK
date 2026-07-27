"""Alation Critical Data Manager (CDM / CDE) — Critical Data Element Data Models.

See: https://developer.alation.com/dev/reference/cde-api-overview
"""

from dataclasses import dataclass, field
from datetime import datetime

from ..core.custom_exceptions import InvalidPostBody
from ..core.data_structures import BaseClass, BaseParams


# Known Critical Data Element statuses, kept as a reference tuple (not enforced with a
# Literal on the response model) so unexpected server values never break parsing.
# Only CANDIDATE / DRAFT are valid creation states.
CDE_STATUSES = (
    "CANDIDATE",
    "DRAFT",
    "PENDING_APPROVERS_APPROVAL",
    "PENDING_OWNERS_APPROVAL",
    "IN_REVIEW",
    "CERTIFIED",
)
CDE_CREATION_STATUSES = ("CANDIDATE", "DRAFT")


@dataclass
class CriticalDataElementBase(BaseClass):
    """Fields shared between the response and create payload representations."""
    name: str = field(default=None)
    description: str = field(default=None)
    status: str = field(default=None)


@dataclass
class CriticalDataElement(CriticalDataElementBase):
    """A Critical Data Element as returned by the CDE API (GET responses)."""
    id: int = field(default=None)
    key: str = field(default=None)  # uuid
    job_id: int = field(default=None)
    ts_created: datetime = field(default=None)
    ts_updated: datetime = field(default=None)

    def __post_init__(self):
        if isinstance(self.ts_created, str):
            self.ts_created = self.convert_timestamp(self.ts_created)
        if isinstance(self.ts_updated, str):
            self.ts_updated = self.convert_timestamp(self.ts_updated)


@dataclass
class CriticalDataElementItem(CriticalDataElementBase):
    """A Critical Data Element to be created (POST / bulk POST payload)."""

    def generate_api_post_payload(self) -> dict:
        """Build the request payload for creating a Critical Data Element.

        Returns:
            dict: Payload containing ``name`` and any provided optional fields.

        Raises:
            InvalidPostBody: If ``name`` is not set.

        """
        if not self.name:
            raise InvalidPostBody(
                "'name' is a required field for a Critical Data Element POST payload body"
            )
        payload = {"name": self.name}
        if self.description is not None:
            payload["description"] = self.description
        if self.status:
            payload["status"] = self.status
        return payload


@dataclass
class CriticalDataElementParams(BaseParams):
    """Filter parameters for GET ``/cde-service/integration/cde/``.

    Note:
        ``skip``/``limit`` pagination is handled by the request handler, so callers
        should generally not set them here (``BaseParams`` also drops falsy values such
        as ``skip=0``).
    """
    search: str = field(default=None)
    status: str = field(default=None)
    key: str = field(default=None)
    job_id: int = field(default=None)
    order_by: str = field(default=None)
