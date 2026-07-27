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

# Valid PDE relationship types for a Critical Data Element.
CDE_PDE_RELATIONSHIPS = ("control_point", "related", "suggested")

# Risk levels use a fixed 1-3 value scale (1 = lowest, 3 = highest); the number of levels
# and the allowed values cannot be changed. The labels ARE tenant-configurable in the Risk
# Assessment Framework governance standard, so these are only the default labels — do not
# enforce them. See:
# https://docs.alation.com/en/latest/steward/CDEManagement/ReviewDefaultCDEStandards.html
CDE_RISK_LEVEL_DEFAULT_LABELS = {1: "Low", 2: "Medium", 3: "High"}


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
    # Risk: list responses return `cde_risk_level` (a string label); get responses return
    # a `risk_level` object plus `risk_rationale` / `risk_confidence`.
    cde_risk_level: str = field(default=None)  # e.g. "Low"/"Medium"/"High" (list responses)
    risk_level: dict = field(default=None)  # {value, label, number_of_levels} (get responses)
    risk_rationale: str = field(default=None)
    risk_confidence: float = field(default=None)

    # Relationship / ownership arrays and applied overlay-standard data (raw passthrough).
    domains: list = field(default=None)
    stewards: list = field(default=None)
    owners: list = field(default=None)
    sources: list = field(default=None)
    approvers: list = field(default=None)
    contributors: list = field(default=None)
    fields: list = field(default=None)  # applied overlay-standard data

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
    """A Critical Data Element to be created/updated (POST / bulk POST / PUT payload).

    Beyond ``name``/``description``/``status``, the create and update endpoints accept
    optional risk fields and relationship data. The relationship arrays
    (``domains``/``stewards``/``owners``/``sources``/``approvers``/``contributors``), the
    overlay-standard ``fields``, and the physical-data-element ``pdes`` are passed through
    as raw ``list`` values (not typed sub-models). Object-references use ``source_key`` in
    the ``alation://<type>/<id>`` form, e.g.
    ``{"id": 123, "name": "Privacy Officer", "source_key": "alation://user/123"}``.
    """
    risk_level_value: int = field(default=None)
    risk_level_label: str = field(default=None)
    risk_rationale: str = field(default=None)
    domains: list = field(default=None)
    stewards: list = field(default=None)
    owners: list = field(default=None)
    sources: list = field(default=None)
    approvers: list = field(default=None)
    contributors: list = field(default=None)
    fields: list = field(default=None)  # applied overlay-standard data
    pdes: list = field(default=None)  # physical-data-element mappings (create only)

    # Optional fields common to create and update, in the order shown by the API docs.
    _RISK_FIELDS = ("risk_level_value", "risk_level_label", "risk_rationale")
    _RELATIONSHIP_FIELDS = (
        "domains", "stewards", "owners", "sources", "approvers", "contributors", "fields",
    )

    @staticmethod
    def _require_keys(obj: dict, required: tuple, context: str) -> None:
        """Raise InvalidPostBody unless ``obj`` is a dict containing all ``required`` keys."""
        if not isinstance(obj, dict):
            raise InvalidPostBody(f"{context} must be an object, got {type(obj).__name__}")
        missing = [key for key in required if obj.get(key) is None]
        if missing:
            raise InvalidPostBody(
                f"{context} is missing required field(s): {', '.join(missing)}"
            )

    def _validate_fields(self) -> None:
        """Validate the nested overlay-standard ``fields`` structure (if set)."""
        for i, cde_field in enumerate(self.fields):
            self._require_keys(cde_field, ("key", "derived_requirements"), f"fields[{i}]")
            requirements = cde_field["derived_requirements"]
            if not isinstance(requirements, list):
                raise InvalidPostBody(f"fields[{i}].derived_requirements must be a list")
            for j, requirement in enumerate(requirements):
                ctx = f"fields[{i}].derived_requirements[{j}]"
                self._require_keys(requirement, ("key", "fields"), ctx)
                inner_fields = requirement["fields"]
                if not isinstance(inner_fields, list):
                    raise InvalidPostBody(f"{ctx}.fields must be a list")
                for k, inner in enumerate(inner_fields):
                    self._require_keys(inner, ("key", "value"), f"{ctx}.fields[{k}]")

    def _validate_pdes(self) -> None:
        """Validate the nested ``pdes`` structure (if set)."""
        for i, pde in enumerate(self.pdes):
            self._require_keys(
                pde, ("name", "relationship", "source_key", "path"), f"pdes[{i}]"
            )
            relationship = pde["relationship"]
            if relationship not in CDE_PDE_RELATIONSHIPS:
                raise InvalidPostBody(
                    f"pdes[{i}].relationship must be one of "
                    f"{', '.join(CDE_PDE_RELATIONSHIPS)}; got {relationship!r}"
                )
            path = pde["path"]
            if not isinstance(path, list):
                raise InvalidPostBody(f"pdes[{i}].path must be a list")
            for j, level in enumerate(path):
                self._require_keys(level, ("type", "name"), f"pdes[{i}].path[{j}]")

    def _add_optional_fields(self, payload: dict, include_pdes: bool) -> None:
        """Add any set optional fields to ``payload``, validating nested structures."""
        for name in self._RISK_FIELDS:
            value = getattr(self, name)
            if value is not None:
                payload[name] = value
        for name in self._RELATIONSHIP_FIELDS:
            value = getattr(self, name)
            if value is not None:
                if name == "fields":
                    self._validate_fields()
                payload[name] = value
        # `pdes` is accepted on create but is not an update-body field.
        if include_pdes and self.pdes is not None:
            self._validate_pdes()
            payload["pdes"] = self.pdes

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
        self._add_optional_fields(payload, include_pdes=True)
        return payload

    def generate_api_put_payload(self) -> dict:
        """Build the request payload for updating a Critical Data Element.

        Only the fields that are set are included. ``status`` is intentionally excluded:
        it is not an update field (status changes go through the CDE status-transition
        endpoint), so it is ignored here even if set on the item. ``pdes`` is likewise not
        an update-body field and is omitted.

        Returns:
            dict: Payload containing whichever of the update fields are set.

        """
        payload = {}
        if self.name is not None:
            payload["name"] = self.name
        if self.description is not None:
            payload["description"] = self.description
        self._add_optional_fields(payload, include_pdes=False)
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
