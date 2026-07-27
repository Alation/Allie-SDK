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
    """A Critical Data Element as returned by the CDE API (GET responses).

    Scalar attributes are typed. The relationship/ownership attributes
    (``domains``/``stewards``/``owners``/``sources``/``approvers``/``contributors``) and
    the audit objects (``created_by``/``updated_by``/``deleted_by``) are exposed as raw
    values (``list``/``dict`` of the API payload) rather than typed sub-models — those
    workflows are not modelled yet. Each object-reference is shaped like
    ``{"id": int, "name": str, "source_key": "alation://<type>/<id>"}``.
    """
    id: int = field(default=None)
    key: str = field(default=None)  # uuid
    id_no: int = field(default=None)  # human-facing sequential number
    version: int = field(default=None)
    cde_risk_level: str = field(default=None)  # e.g. "Low"/"Medium"/"High" (read-only)

    # Relationship / ownership arrays (raw object-reference dicts).
    domains: list = field(default=None)
    stewards: list = field(default=None)
    owners: list = field(default=None)
    sources: list = field(default=None)
    approvers: list = field(default=None)
    contributors: list = field(default=None)

    # Metrics. data_assets_counts is a dict of PDE-relationship counts,
    # e.g. {"all", "control_points", "related", "suggested"}; scores may be null.
    data_assets_counts: dict = field(default=None)
    quality_score: float = field(default=None)
    curation_score: float = field(default=None)

    job_id: int = field(default=None)

    # Audit trail.
    ts_created: datetime = field(default=None)
    ts_updated: datetime = field(default=None)
    ts_deleted: datetime = field(default=None)
    created_by: dict = field(default=None)  # {id, name, source_key}
    updated_by: dict = field(default=None)
    deleted_by: dict = field(default=None)
    deleted: bool = field(default=None)

    def __post_init__(self):
        if isinstance(self.ts_created, str):
            self.ts_created = self.convert_timestamp(self.ts_created)
        if isinstance(self.ts_updated, str):
            self.ts_updated = self.convert_timestamp(self.ts_updated)
        if isinstance(self.ts_deleted, str):
            self.ts_deleted = self.convert_timestamp(self.ts_deleted)


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

    def generate_api_put_payload(self) -> dict:
        """Build the request payload for updating a Critical Data Element.

        Only the fields that are set are included. ``status`` is intentionally excluded:
        it is not an update field (status changes go through the CDE status-transition
        endpoint), so it is ignored here even if set on the item.

        Returns:
            dict: Payload containing whichever of ``name``/``description`` are set.

        """
        payload = {}
        if self.name is not None:
            payload["name"] = self.name
        if self.description is not None:
            payload["description"] = self.description
        return payload


@dataclass
class CriticalDataElementParams(BaseParams):
    """Filter parameters for GET ``/cde-service/integration/cde/``.

    Repeatable filters (``status``, ``risk_level``, ``owner_key``, ``domain_keys``,
    ``steward_key``, ``version``, ``key``) are modelled as sets and serialized as repeated
    query parameters. ``risk_level`` filters by integer risk codes (e.g. ``1``, ``2``),
    even though the response returns ``cde_risk_level`` as a string label.

    Note:
        ``skip``/``limit`` pagination is handled by the request handler, so it is not a
        parameter here. ``BaseParams`` also drops falsy values, so ``latest_only=False``
        would be omitted (leaving the server default) rather than sent as ``false``.
    """
    search: str = field(default=None)
    status: set = field(default_factory=set)
    risk_level: set = field(default_factory=set)
    owner_key: set = field(default_factory=set)
    domain_keys: set = field(default_factory=set)
    steward_key: set = field(default_factory=set)
    version: set = field(default_factory=set)
    key: set = field(default_factory=set)
    job_id: int = field(default=None)
    latest_only: bool = field(default=None)
    latest_certified_only: bool = field(default=None)
    order_by: str = field(default=None)

    def generate_params_dict(self) -> dict:
        """Build the query-parameter dict, mapping ``domain_keys`` to the API's
        bracketed key name ``domain_keys[]`` (the other array filters use the bare name).
        """
        params = super().generate_params_dict()
        if "domain_keys" in params:
            params["domain_keys[]"] = params.pop("domain_keys")
        return params
