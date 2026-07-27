"""Alation Data Products API data models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ..core.custom_exceptions import InvalidPostBody, validate_rest_payload
from ..core.data_structures import BaseClass, BaseParams


DATA_PRODUCT_PERMISSION_ROLES = {
    "product_admin",
    "product_viewer",
}
DATA_PRODUCT_PERMISSION_ACTIONS = {
    "view",
    "view_events",
    "view_stats",
    "delete",
    "update",
    "manage_roles",
}
PERMISSION_ROLES = {
    "app_admin",
    "app_user",
    "app_viewer",
    "marketplace_admin",
    "marketplace_maintainer",
    "marketplace_viewer",
    "product_admin",
    "product_viewer",
}
PERMISSION_SUBJECT_TYPES = {
    "everyone",
    "user",
    "group",
}
PERMISSION_OBJECT_TYPES = {
    "app",
    "data_product",
    "markeplace",
}
DATA_PRODUCT_VERSION_STATUSES = {
    "draft",
    "ready",
}


def _validate_extensions(extensions: dict[str, Any], field_name: str):
    """Validate custom extension properties."""

    if not extensions:
        return

    if not isinstance(extensions, dict):
        raise InvalidPostBody(f"'{field_name}' must be a dictionary of x- properties.")

    invalid_keys = [key for key in extensions if not str(key).startswith("x-")]
    if invalid_keys:
        raise InvalidPostBody(
            f"All custom properties in '{field_name}' must start with 'x-'. Invalid keys: {invalid_keys}"
        )


def _merge_extensions(payload: dict[str, Any], extensions: dict[str, Any], field_name: str) -> dict[str, Any]:
    """Merge custom extension properties into the payload."""

    _validate_extensions(extensions, field_name)
    if extensions:
        payload.update(extensions)
    return payload


def _convert_timestamp(value: str | datetime | None) -> datetime | None:
    """Convert API timestamp strings into ``datetime`` objects."""

    if isinstance(value, str):
        return BaseClass.convert_timestamp(value)
    return value


def _map_list(items: list[Any] | None, model_class: type[BaseClass]) -> list[Any]:
    """Convert lists of dictionaries into SDK model instances."""

    if not items:
        return []

    mapped_items = []
    for item in items:
        if isinstance(item, dict):
            mapped_items.append(model_class.from_api_response(item))
        else:
            mapped_items.append(item)
    return mapped_items


def _map_dict_values(items: dict[str, Any] | None, model_class: type[BaseClass]) -> dict[str, Any]:
    """Convert dictionary values into SDK model instances."""

    if not items:
        return {}

    mapped_items = {}
    for key, value in items.items():
        if isinstance(value, dict):
            mapped_items[key] = model_class.from_api_response(value)
        else:
            mapped_items[key] = value
    return mapped_items


@dataclass(kw_only=True)
class DataProductLanguage(BaseClass):
    """Localized data product properties."""

    name: str = field(default=None)
    description: str = field(default=None)
    shortDescription: str = field(default=None)
    logoUrl: str = field(default=None)
    extensions: dict[str, Any] = field(default_factory=dict)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for localized product properties."""

        if self.name is None:
            raise InvalidPostBody("'name' is a required field for Data Product language payload bodies")

        payload = {"name": self.name}
        if self.description is not None:
            payload["description"] = self.description
        if self.shortDescription is not None:
            payload["shortDescription"] = self.shortDescription
        if self.logoUrl is not None:
            payload["logoUrl"] = self.logoUrl

        return _merge_extensions(payload, self.extensions, "extensions")


@dataclass(kw_only=True)
class DataProductAccessRequestInstruction(BaseClass):
    """Access instructions for a delivery system."""

    type: str = field(default=None)
    instruction: str = field(default=None)
    request: str = field(default=None)
    uri: str = field(default=None)
    provider: str = field(default=None)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for access request instructions."""

        if self.type is None:
            raise InvalidPostBody(
                "'type' is a required field for Data Product access request instruction payload bodies"
            )

        if self.type == "external":
            if self.uri is None:
                raise InvalidPostBody(
                    "'uri' is a required field when type='external' for Data Product access request instruction payload bodies"
                )
            if self.provider is None:
                raise InvalidPostBody(
                    "'provider' is a required field when type='external' for Data Product access request instruction payload bodies"
                )

            return {
                "type": self.type,
                "uri": self.uri,
                "provider": self.provider,
            }

        if self.instruction is None:
            raise InvalidPostBody(
                "'instruction' is a required field for manual Data Product access request instruction payload bodies"
            )

        payload = {
            "type": self.type,
            "instruction": self.instruction,
        }
        if self.request is not None:
            payload["request"] = self.request
        return payload


@dataclass(kw_only=True)
class DataProductDeliverySystem(BaseClass):
    """Delivery system definition within a data product spec."""

    type: str = field(default=None)
    uri: str = field(default=None)
    datasourceId: int = field(default=None)
    accessRequestInstruction: DataProductAccessRequestInstruction = field(default=None)

    def __post_init__(self):
        if isinstance(self.accessRequestInstruction, dict):
            self.accessRequestInstruction = DataProductAccessRequestInstruction.from_api_response(
                self.accessRequestInstruction
            )

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for delivery systems."""

        if self.type is None:
            raise InvalidPostBody("'type' is a required field for Data Product delivery system payload bodies")
        if self.uri is None:
            raise InvalidPostBody("'uri' is a required field for Data Product delivery system payload bodies")

        payload = {
            "type": self.type,
            "uri": self.uri,
        }
        if self.datasourceId is not None:
            payload["datasourceId"] = self.datasourceId
        if self.accessRequestInstruction is not None:
            payload["accessRequestInstruction"] = self.accessRequestInstruction.generate_api_payload()
        return payload


@dataclass(kw_only=True)
class DataProductRecordSetField(BaseClass):
    """Schema field definition for a record set."""

    name: str = field(default=None)
    displayName: str = field(default=None)
    description: str = field(default=None)
    type: str = field(default=None)
    extensions: dict[str, Any] = field(default_factory=dict)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for record set fields."""

        if self.name is None:
            raise InvalidPostBody("'name' is a required field for Data Product record set field payload bodies")
        if self.type is None:
            raise InvalidPostBody("'type' is a required field for Data Product record set field payload bodies")

        payload = {
            "name": self.name,
            "type": self.type,
        }
        if self.displayName is not None:
            payload["displayName"] = self.displayName
        if self.description is not None:
            payload["description"] = self.description

        return _merge_extensions(payload, self.extensions, "extensions")


@dataclass(kw_only=True)
class DataProductRecordSetSample(BaseClass):
    """Sample data attached to a record set."""

    type: str = field(default=None)
    data: str = field(default=None)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for record set samples."""

        if self.type is None:
            raise InvalidPostBody("'type' is a required field for Data Product sample payload bodies")
        if self.data is None:
            raise InvalidPostBody("'data' is a required field for Data Product sample payload bodies")
        return {
            "type": self.type,
            "data": self.data,
        }


@dataclass(kw_only=True)
class DataProductQualifiedName(BaseClass):
    """Qualified object name used in SQL data access definitions."""

    database: str = field(default=None)
    schema: str = field(default=None)
    table: str = field(default=None)
    column: str = field(default=None)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for qualified object names."""

        if self.schema is None:
            raise InvalidPostBody("'schema' is a required field for Data Product qualified name payload bodies")
        if self.table is None:
            raise InvalidPostBody("'table' is a required field for Data Product qualified name payload bodies")

        payload = {
            "schema": self.schema,
            "table": self.table,
        }
        if self.database is not None:
            payload["database"] = self.database
        if self.column is not None:
            payload["column"] = self.column
        return payload


@dataclass(kw_only=True)
class DataProductDataAccess(BaseClass):
    """Data access definition for a record set."""

    type: str = field(default=None)
    format: str = field(default=None)
    host: str = field(default=None)
    qualifiedName: DataProductQualifiedName = field(default=None)
    documentationUrl: str = field(default=None)
    extensions: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.qualifiedName, dict):
            self.qualifiedName = DataProductQualifiedName.from_api_response(self.qualifiedName)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for record set data access definitions."""

        if self.type is None:
            raise InvalidPostBody("'type' is a required field for Data Product data access payload bodies")

        payload = {"type": self.type}

        if self.format is not None:
            payload["format"] = self.format
        if self.host is not None:
            payload["host"] = self.host
        if self.qualifiedName is not None:
            payload["qualifiedName"] = self.qualifiedName.generate_api_payload()
        if self.documentationUrl is not None:
            payload["documentationUrl"] = self.documentationUrl

        return _merge_extensions(payload, self.extensions, "extensions")


@dataclass(kw_only=True)
class DataProductRelationship(BaseClass):
    """Relationship between record sets."""

    name: str = field(default=None)
    rightTable: str = field(default=None)
    expression: str = field(default=None)
    sqlDialect: str = field(default=None)
    cardinality: str = field(default=None)
    leftNullable: bool = field(default=None)
    rightNullable: bool = field(default=None)
    notes: str = field(default=None)
    extensions: dict[str, Any] = field(default_factory=dict)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for record set relationships."""

        required_fields = {
            "rightTable": self.rightTable,
            "expression": self.expression,
            "sqlDialect": self.sqlDialect,
            "cardinality": self.cardinality,
            "leftNullable": self.leftNullable,
            "rightNullable": self.rightNullable,
        }
        missing_fields = [key for key, value in required_fields.items() if value is None]
        if missing_fields:
            raise InvalidPostBody(
                f"Missing required fields for Data Product relationship payload bodies: {missing_fields}"
            )

        payload = {
            "rightTable": self.rightTable,
            "expression": self.expression,
            "sqlDialect": self.sqlDialect,
            "cardinality": self.cardinality,
            "leftNullable": self.leftNullable,
            "rightNullable": self.rightNullable,
        }
        if self.name is not None:
            payload["name"] = self.name
        if self.notes is not None:
            payload["notes"] = self.notes

        return _merge_extensions(payload, self.extensions, "extensions")


@dataclass(kw_only=True)
class DataProductRecordSet(BaseClass):
    """Record set definition inside a data product spec."""

    name: str = field(default=None)
    displayName: str = field(default=None)
    description: str = field(default=None)
    schema: list[DataProductRecordSetField] = field(default_factory=list)
    sample: DataProductRecordSetSample = field(default=None)
    dataAccess: list[DataProductDataAccess] = field(default_factory=list)
    relationships: list[DataProductRelationship] = field(default_factory=list)
    extensions: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.schema = _map_list(self.schema, DataProductRecordSetField)
        if isinstance(self.sample, dict):
            self.sample = DataProductRecordSetSample.from_api_response(self.sample)
        self.dataAccess = _map_list(self.dataAccess, DataProductDataAccess)
        self.relationships = _map_list(self.relationships, DataProductRelationship)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for record sets."""

        payload = {}
        if self.name is not None:
            payload["name"] = self.name
        if self.displayName is not None:
            payload["displayName"] = self.displayName
        if self.description is not None:
            payload["description"] = self.description
        if self.schema:
            validate_rest_payload(self.schema, (DataProductRecordSetField,))
            payload["schema"] = [field_item.generate_api_payload() for field_item in self.schema]
        if self.sample is not None:
            payload["sample"] = self.sample.generate_api_payload()
        if self.dataAccess:
            validate_rest_payload(self.dataAccess, (DataProductDataAccess,))
            payload["dataAccess"] = [item.generate_api_payload() for item in self.dataAccess]
        if self.relationships:
            validate_rest_payload(self.relationships, (DataProductRelationship,))
            payload["relationships"] = [item.generate_api_payload() for item in self.relationships]

        return _merge_extensions(payload, self.extensions, "extensions")


@dataclass(kw_only=True)
class DataProductMetric(BaseClass):
    """Metric definition inside data product metadata."""

    displayName: str = field(default=None)
    description: str = field(default=None)
    type: str = field(default=None)
    expression: str = field(default=None)
    columns: list[str] = field(default_factory=list)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for data product metrics."""

        if self.displayName is None:
            raise InvalidPostBody("'displayName' is a required field for Data Product metric payload bodies")
        if self.description is None:
            raise InvalidPostBody("'description' is a required field for Data Product metric payload bodies")
        if self.expression is None:
            raise InvalidPostBody("'expression' is a required field for Data Product metric payload bodies")

        payload = {
            "displayName": self.displayName,
            "description": self.description,
            "expression": self.expression,
        }
        if self.type is not None:
            payload["type"] = self.type
        if self.columns:
            payload["columns"] = self.columns
        return payload


@dataclass(kw_only=True)
class DataProductMetadata(BaseClass):
    """Metadata section inside a data product spec."""

    metrics: dict[str, DataProductMetric] = field(default_factory=dict)
    extensions: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.metrics = _map_dict_values(self.metrics, DataProductMetric)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for data product metadata."""

        payload = {}
        if self.metrics:
            payload["metrics"] = {
                key: value.generate_api_payload() if isinstance(value, DataProductMetric) else value
                for key, value in self.metrics.items()
            }
        return _merge_extensions(payload, self.extensions, "extensions")


@dataclass(kw_only=True)
class DataProductSpecDefinition(BaseClass):
    """Top-level ``product`` block in a data product spec."""

    productId: str = field(default=None)
    version: str = field(default=None)
    contactEmail: str = field(default=None)
    contactName: str = field(default=None)
    en: DataProductLanguage = field(default=None)
    deliverySystems: dict[str, DataProductDeliverySystem] = field(default_factory=dict)
    recordSets: dict[str, DataProductRecordSet] = field(default_factory=dict)
    metadata: DataProductMetadata = field(default=None)
    extensions: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.en, dict):
            self.en = DataProductLanguage.from_api_response(self.en)
        self.deliverySystems = _map_dict_values(self.deliverySystems, DataProductDeliverySystem)
        self.recordSets = _map_dict_values(self.recordSets, DataProductRecordSet)
        if isinstance(self.metadata, dict):
            self.metadata = DataProductMetadata.from_api_response(self.metadata)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for the top-level product definition."""

        required_fields = {
            "productId": self.productId,
            "version": self.version,
            "contactEmail": self.contactEmail,
            "contactName": self.contactName,
            "en": self.en,
        }
        missing_fields = [key for key, value in required_fields.items() if value is None]
        if missing_fields:
            raise InvalidPostBody(
                f"Missing required fields for Data Product spec payload bodies: {missing_fields}"
            )

        payload = {
            "productId": self.productId,
            "version": self.version,
            "contactEmail": self.contactEmail,
            "contactName": self.contactName,
            "en": self.en.generate_api_payload(),
        }
        if self.deliverySystems:
            payload["deliverySystems"] = {
                key: value.generate_api_payload() if isinstance(value, DataProductDeliverySystem) else value
                for key, value in self.deliverySystems.items()
            }
        if self.recordSets:
            payload["recordSets"] = {
                key: value.generate_api_payload() if isinstance(value, DataProductRecordSet) else value
                for key, value in self.recordSets.items()
            }
        if self.metadata is not None:
            payload["metadata"] = self.metadata.generate_api_payload()

        return _merge_extensions(payload, self.extensions, "extensions")


@dataclass(kw_only=True)
class DataProductSpec(BaseClass):
    """Data product specification payload used for create and update calls."""

    schema: str = field(default=None)
    product: DataProductSpecDefinition = field(default=None)
    extensions: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.product, dict):
            self.product = DataProductSpecDefinition.from_api_response(self.product)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for a data product specification."""

        if self.product is None:
            raise InvalidPostBody("'product' is a required field for Data Product spec payload bodies")

        payload = {"product": self.product.generate_api_payload()}
        if self.schema is not None:
            payload["schema"] = self.schema
        return _merge_extensions(payload, self.extensions, "extensions")


@dataclass(kw_only=True)
class DataProductStandardDisplayName(BaseClass):
    """Display name structure used by marketplace standards."""

    en: str = field(default=None)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for standard display names."""

        if self.en is None:
            raise InvalidPostBody("'en' is a required field for Data Product standard display names")
        return {"en": self.en}


@dataclass(kw_only=True)
class DataProductStandard(BaseClass):
    """Marketplace badge or standard definition."""

    type: str = field(default=None)
    check: str = field(default=None)
    key: str = field(default=None)
    report_key: str = field(default=None)
    displayName: DataProductStandardDisplayName = field(default=None)
    onFail: str = field(default=None)

    def __post_init__(self):
        if isinstance(self.displayName, dict):
            self.displayName = DataProductStandardDisplayName.from_api_response(self.displayName)

    def generate_api_payload(self, require_on_fail: bool = False) -> dict[str, Any]:
        """Generate the API payload for marketplace standards."""

        if self.type is None:
            raise InvalidPostBody("'type' is a required field for Data Product standard payload bodies")
        if self.check is None:
            raise InvalidPostBody("'check' is a required field for Data Product standard payload bodies")
        if self.displayName is None:
            raise InvalidPostBody("'displayName' is a required field for Data Product standard payload bodies")
        if self.key is None and self.report_key is None:
            raise InvalidPostBody(
                "Either 'key' or 'report_key' is required for Data Product standard payload bodies"
            )
        if require_on_fail and self.onFail is None:
            raise InvalidPostBody("'onFail' is a required field for marketplace minimum standard payload bodies")

        payload = {
            "type": self.type,
            "check": self.check,
            "displayName": self.displayName.generate_api_payload(),
        }
        if self.key is not None:
            payload["key"] = self.key
        if self.report_key is not None:
            payload["report_key"] = self.report_key
        if self.onFail is not None:
            payload["onFail"] = self.onFail
        return payload


@dataclass(kw_only=True)
class DataMarketplaceLanguage(BaseClass):
    """Localized marketplace properties."""

    name: str = field(default=None)
    description: str = field(default=None)
    shortDescription: str = field(default=None)
    heroImage: str = field(default=None)
    extensions: dict[str, Any] = field(default_factory=dict)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for localized marketplace properties."""

        if self.name is None:
            raise InvalidPostBody("'name' is a required field for Data Marketplace language payload bodies")

        payload = {"name": self.name}
        if self.description is not None:
            payload["description"] = self.description
        if self.shortDescription is not None:
            payload["shortDescription"] = self.shortDescription
        if self.heroImage is not None:
            payload["heroImage"] = self.heroImage

        return _merge_extensions(payload, self.extensions, "extensions")


@dataclass(kw_only=True)
class DataMarketplaceDefinition(BaseClass):
    """Top-level ``marketplace`` block in a marketplace spec."""

    marketplaceId: str = field(default=None)
    contactName: str = field(default=None)
    contactEmail: str = field(default=None)
    dataProductRequirementsSchema: dict[str, Any] = field(default_factory=dict)
    heroBackgroundColor: str = field(default=None)
    badges: list[DataProductStandard] = field(default_factory=list)
    minimumStandard: list[DataProductStandard] = field(default_factory=list)
    en: DataMarketplaceLanguage = field(default=None)
    extensions: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.badges = _map_list(self.badges, DataProductStandard)
        self.minimumStandard = _map_list(self.minimumStandard, DataProductStandard)
        if isinstance(self.en, dict):
            self.en = DataMarketplaceLanguage.from_api_response(self.en)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for a marketplace definition."""

        required_fields = {
            "marketplaceId": self.marketplaceId,
            "contactName": self.contactName,
            "contactEmail": self.contactEmail,
            "en": self.en,
        }
        missing_fields = [key for key, value in required_fields.items() if value is None]
        if missing_fields:
            raise InvalidPostBody(
                f"Missing required fields for Data Marketplace spec payload bodies: {missing_fields}"
            )

        payload = {
            "marketplaceId": self.marketplaceId,
            "contactName": self.contactName,
            "contactEmail": self.contactEmail,
            "en": self.en.generate_api_payload(),
        }
        if self.dataProductRequirementsSchema:
            payload["dataProductRequirementsSchema"] = self.dataProductRequirementsSchema
        if self.heroBackgroundColor is not None:
            payload["heroBackgroundColor"] = self.heroBackgroundColor
        if self.badges:
            validate_rest_payload(self.badges, (DataProductStandard,))
            payload["badges"] = [item.generate_api_payload() for item in self.badges]
        if self.minimumStandard:
            validate_rest_payload(self.minimumStandard, (DataProductStandard,))
            payload["minimumStandard"] = [
                item.generate_api_payload(require_on_fail=True) for item in self.minimumStandard
            ]

        return _merge_extensions(payload, self.extensions, "extensions")


@dataclass(kw_only=True)
class DataMarketplaceSpec(BaseClass):
    """Marketplace specification payload used for create and update calls."""

    schema: str = field(default=None)
    marketplace: DataMarketplaceDefinition = field(default=None)
    extensions: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.marketplace, dict):
            self.marketplace = DataMarketplaceDefinition.from_api_response(self.marketplace)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for a marketplace specification."""

        if self.marketplace is None:
            raise InvalidPostBody("'marketplace' is a required field for Data Marketplace spec payload bodies")

        payload = {"marketplace": self.marketplace.generate_api_payload()}
        if self.schema is not None:
            payload["schema"] = self.schema
        return _merge_extensions(payload, self.extensions, "extensions")


@dataclass(kw_only=True)
class DataProductMarketplaceAssociationMarketplace(BaseClass):
    """Marketplace summary attached to a published data product."""

    external_id: str = field(default=None)
    name: str = field(default=None)


@dataclass(kw_only=True)
class DataProductMarketplaceAssociationState(BaseClass):
    """Association state for a published data product."""

    status: str = field(default=None)
    ts_created: datetime | None = field(default=None)
    ts_updated: datetime | None = field(default=None)

    def __post_init__(self):
        self.ts_created = _convert_timestamp(self.ts_created)
        self.ts_updated = _convert_timestamp(self.ts_updated)


@dataclass(kw_only=True)
class DataProductMarketplaceAssociation(BaseClass):
    """Marketplace association entry on a data product response."""

    marketplace: DataProductMarketplaceAssociationMarketplace = field(default=None)
    state: DataProductMarketplaceAssociationState = field(default=None)

    def __post_init__(self):
        if isinstance(self.marketplace, dict):
            self.marketplace = DataProductMarketplaceAssociationMarketplace.from_api_response(
                self.marketplace
            )
        if isinstance(self.state, dict):
            self.state = DataProductMarketplaceAssociationState.from_api_response(self.state)


@dataclass(kw_only=True)
class DataProductVersionSummary(BaseClass):
    """Version summary returned when ``group_by_product=true``."""

    version_id: str = field(default=None)
    name: str = field(default=None)
    status: str = field(default=None)
    ts_created: datetime | None = field(default=None)
    ts_updated: datetime | None = field(default=None)

    def __post_init__(self):
        self.ts_created = _convert_timestamp(self.ts_created)
        self.ts_updated = _convert_timestamp(self.ts_updated)


@dataclass(kw_only=True)
class DataProduct(BaseClass):
    """Data product returned by the Data Products API."""

    product_id: str = field(default=None)
    version_id: str = field(default=None)
    status: str = field(default=None)
    spec_json: DataProductSpec = field(default=None)
    spec_yaml: str = field(default=None)
    ts_created: datetime | None = field(default=None)
    ts_updated: datetime | None = field(default=None)
    marketplace_associations: list[DataProductMarketplaceAssociation] = field(default_factory=list)
    versions_details: list[DataProductVersionSummary] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.spec_json, dict):
            self.spec_json = DataProductSpec.from_api_response(self.spec_json)
        self.ts_created = _convert_timestamp(self.ts_created)
        self.ts_updated = _convert_timestamp(self.ts_updated)
        self.marketplace_associations = _map_list(
            self.marketplace_associations,
            DataProductMarketplaceAssociation,
        )
        self.versions_details = _map_list(self.versions_details, DataProductVersionSummary)


@dataclass(kw_only=True)
class DataProductMarketplaceContext(BaseClass):
    """Marketplace-specific context returned on search and publish endpoints."""

    badges: list[DataProductStandard] = field(default_factory=list)

    def __post_init__(self):
        self.badges = _map_list(self.badges, DataProductStandard)


@dataclass(kw_only=True)
class DataProductWithMarketplaceInfo(DataProduct):
    """Data product with marketplace-specific context."""

    marketplace_context: DataProductMarketplaceContext = field(default=None)

    def __post_init__(self):
        super().__post_init__()
        if isinstance(self.marketplace_context, dict):
            self.marketplace_context = DataProductMarketplaceContext.from_api_response(
                self.marketplace_context
            )


@dataclass(kw_only=True)
class DataMarketplace(BaseClass):
    """Marketplace returned by the Data Products API."""

    external_marketplace_id: str = field(default=None)
    name: str = field(default=None)
    spec: DataMarketplaceSpec = field(default=None)
    spec_yaml: str = field(default=None)
    products: list[DataProduct] = field(default_factory=list)
    products_total: int = field(default=None)

    def __post_init__(self):
        if isinstance(self.spec, dict):
            self.spec = DataMarketplaceSpec.from_api_response(self.spec)
        self.products = _map_list(self.products, DataProduct)


@dataclass(kw_only=True)
class DataProductParams(BaseParams):
    """Optional filters for listing data products."""

    limit: int = field(default=None)
    offset: int = field(default=None)
    order_by: str = field(default=None)
    role: str = field(default=None)
    action: str = field(default=None)
    product_ids: list[str] = field(default_factory=list)
    group_by_product: bool | None = field(default=None)

    def generate_params_dict(self) -> dict[str, Any]:
        """Generate query parameters for listing data products."""

        params = {}
        if self.limit is not None:
            params["limit"] = self.limit
        if self.offset is not None:
            params["skip"] = self.offset
        if self.order_by is not None:
            params["order_by"] = self.order_by
        if self.role is not None:
            params["role"] = self.role
        if self.action is not None:
            params["action"] = self.action
        if self.product_ids:
            params["product_ids"] = self.product_ids
        if self.group_by_product is not None:
            params["group_by_product"] = self.group_by_product
        return params


@dataclass(kw_only=True)
class DataMarketplaceParams(BaseParams):
    """Optional filters for marketplace list and detail calls."""

    limit: int = field(default=None)
    offset: int = field(default=None)

    def generate_params_dict(self) -> dict[str, Any]:
        """Generate query parameters for marketplace list and detail calls."""

        params = {}
        if self.limit is not None:
            params["limit"] = self.limit
        if self.offset is not None:
            params["skip"] = self.offset
        return params


@dataclass(kw_only=True)
class PublishedDataProductParams(BaseParams):
    """Optional filters for published data product list calls."""

    limit: int = field(default=None)
    offset: int = field(default=None)

    def generate_params_dict(self) -> dict[str, Any]:
        """Generate query parameters for published data product lists."""

        params = {}
        if self.limit is not None:
            params["limit"] = self.limit
        if self.offset is not None:
            params["skip"] = self.offset
        return params


@dataclass(kw_only=True)
class DataProductPublishParams(BaseParams):
    """Optional version parameter used by publish and update-published endpoints."""

    version: str = field(default=None)

    def generate_params_dict(self) -> dict[str, Any]:
        """Generate query parameters for publish and update-published calls."""

        params = {}
        if self.version is not None:
            params["version"] = self.version
        return params


@dataclass(kw_only=True)
class DataProductVersionUpdate(BaseClass):
    """Payload used to update a data product version status."""

    status: str = field(default=None)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for version updates."""

        if self.status is None:
            raise InvalidPostBody("'status' is a required field for Data Product version update payload bodies")
        if self.status not in DATA_PRODUCT_VERSION_STATUSES:
            raise InvalidPostBody(
                f"'status' must be one of {sorted(DATA_PRODUCT_VERSION_STATUSES)} for Data Product version updates"
            )
        return {"status": self.status}


@dataclass(kw_only=True)
class PublishInfo(BaseClass):
    """Product/version identifier used in publish operations."""

    product_id: str = field(default=None)
    version_id: str = field(default=None)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for a publish operation entry."""

        if self.product_id is None:
            raise InvalidPostBody("'product_id' is a required field for Data Product publish payload bodies")

        payload = {"product_id": self.product_id}
        if self.version_id is not None:
            payload["version_id"] = self.version_id
        return payload


@dataclass(kw_only=True)
class BulkPublishInfo(BaseClass):
    """Payload used for bulk publish, update, and unpublish operations."""

    publish: list[PublishInfo] = field(default_factory=list)
    update: list[PublishInfo] = field(default_factory=list)
    unpublish: list[PublishInfo] = field(default_factory=list)

    def __post_init__(self):
        self.publish = _map_list(self.publish, PublishInfo)
        self.update = _map_list(self.update, PublishInfo)
        self.unpublish = _map_list(self.unpublish, PublishInfo)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for bulk publish operations."""

        payload = {}
        if self.publish:
            validate_rest_payload(self.publish, (PublishInfo,))
            payload["publish"] = [item.generate_api_payload() for item in self.publish]
        if self.update:
            validate_rest_payload(self.update, (PublishInfo,))
            payload["update"] = [item.generate_api_payload() for item in self.update]
        if self.unpublish:
            validate_rest_payload(self.unpublish, (PublishInfo,))
            payload["unpublish"] = [item.generate_api_payload() for item in self.unpublish]

        if not payload:
            raise InvalidPostBody(
                "At least one of 'publish', 'update', or 'unpublish' is required for bulk publish payload bodies"
            )
        return payload


@dataclass(kw_only=True)
class ProductReportResult(BaseClass):
    """Report result payload for a single data product."""

    report_key: str = field(default=None)
    value: Any = field(default=None)
    extra_fields: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api_response(cls, body_params: dict):
        body = dict(body_params)
        report_key = body.pop("report_key", None)
        value = body.pop("value", None)
        extra_fields = body.pop("extra_fields", {}) or {}
        if body:
            extra_fields = {**body, **extra_fields}
        return cls(report_key=report_key, value=value, extra_fields=extra_fields)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for a product report result."""

        if self.report_key is None:
            raise InvalidPostBody("'report_key' is a required field for Product Report payload bodies")

        payload = {
            "report_key": self.report_key,
            "value": self.value,
        }
        if self.extra_fields:
            payload.update(self.extra_fields)
        return payload


@dataclass(kw_only=True)
class ProductReportResultRead(ProductReportResult):
    """Report result returned when reading a single product's report results."""


@dataclass(kw_only=True)
class ReportResult(ProductReportResult):
    """Report result payload spanning multiple data products."""

    product_id: str = field(default=None)

    @classmethod
    def from_api_response(cls, body_params: dict):
        body = dict(body_params)
        product_id = body.pop("product_id", None)
        report_key = body.pop("report_key", None)
        value = body.pop("value", None)
        extra_fields = body.pop("extra_fields", {}) or {}
        if body:
            extra_fields = {**body, **extra_fields}
        return cls(
            product_id=product_id,
            report_key=report_key,
            value=value,
            extra_fields=extra_fields,
        )

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for a multi-product report result."""

        if self.product_id is None:
            raise InvalidPostBody("'product_id' is a required field for Report Result payload bodies")

        payload = super().generate_api_payload()
        payload["product_id"] = self.product_id
        return payload


@dataclass(kw_only=True)
class ReportResultRead(ReportResult):
    """Report result returned by the global report results endpoint."""


@dataclass(kw_only=True)
class DataProductReportResultsParams(BaseParams):
    """Optional query parameters for data product report results."""

    report_key: str = field(default=None)

    def generate_params_dict(self) -> dict[str, Any]:
        """Generate query parameters for product-specific report retrieval."""

        params = {}
        if self.report_key is not None:
            params["report_key"] = self.report_key
        return params


@dataclass(kw_only=True)
class ReportResultsParams(BaseParams):
    """Optional query parameters for the global report results endpoint."""

    product_id: str = field(default=None)
    report_key: str = field(default=None)

    def generate_params_dict(self) -> dict[str, Any]:
        """Generate query parameters for global report retrieval."""

        params = {}
        if self.product_id is not None:
            params["product_id"] = self.product_id
        if self.report_key is not None:
            params["report_key"] = self.report_key
        return params


@dataclass(kw_only=True)
class DataProductCheckStandard(BaseClass):
    """Standard used when checking a product against marketplace rules."""

    type: str = field(default=None)
    check: str = field(default=None)
    key: str = field(default=None)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for a data product check standard."""

        if self.type is None:
            raise InvalidPostBody("'type' is a required field for Data Product check payload bodies")
        if self.check is None:
            raise InvalidPostBody("'check' is a required field for Data Product check payload bodies")
        if self.key is None:
            raise InvalidPostBody("'key' is a required field for Data Product check payload bodies")
        return {
            "type": self.type,
            "check": self.check,
            "key": self.key,
        }


@dataclass(kw_only=True)
class DataProductCheck(BaseClass):
    """Payload used to validate a data product against standards."""

    product_spec: DataProductSpec = field(default=None)
    standards: list[DataProductCheckStandard] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.product_spec, dict):
            self.product_spec = DataProductSpec.from_api_response(self.product_spec)
        self.standards = _map_list(self.standards, DataProductCheckStandard)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for a standards check request."""

        if self.product_spec is None:
            raise InvalidPostBody("'product_spec' is a required field for Data Product check payload bodies")
        if not self.standards:
            raise InvalidPostBody("'standards' is a required field for Data Product check payload bodies")

        validate_rest_payload(self.standards, (DataProductCheckStandard,))
        return {
            "product_spec": self.product_spec.generate_api_payload(),
            "standards": [item.generate_api_payload() for item in self.standards],
        }


@dataclass(kw_only=True)
class DataProductCheckResultItem(BaseClass):
    """Single standards check result."""

    key: str = field(default=None)
    check: str = field(default=None)
    type: str = field(default=None)
    passed: bool = field(default=None)
    explanation: str = field(default=None)


@dataclass(kw_only=True)
class DataProductSearchQuery(BaseClass):
    """Natural-language marketplace search request."""

    user_query: str = field(default=None)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for an internal marketplace search request."""

        if self.user_query is None:
            raise InvalidPostBody("'user_query' is a required field for Data Product search payload bodies")
        return {"user_query": self.user_query}


@dataclass(kw_only=True)
class DataProductPermission(BaseClass):
    """Permission request and response payload."""

    subject_type: str = field(default=None)
    subject_id: str = field(default=None)
    object_type: str = field(default=None)
    object_id: str = field(default=None)
    role: str = field(default=None)

    def generate_api_payload(self) -> dict[str, Any]:
        """Generate the API payload for permission management endpoints."""

        required_fields = {
            "subject_type": self.subject_type,
            "subject_id": self.subject_id,
            "object_type": self.object_type,
            "object_id": self.object_id,
            "role": self.role,
        }
        missing_fields = [key for key, value in required_fields.items() if value is None]
        if missing_fields:
            raise InvalidPostBody(
                f"Missing required fields for Data Product permission payload bodies: {missing_fields}"
            )

        if self.subject_type not in PERMISSION_SUBJECT_TYPES:
            raise InvalidPostBody(
                f"'subject_type' must be one of {sorted(PERMISSION_SUBJECT_TYPES)} for Data Product permissions"
            )
        if self.object_type not in PERMISSION_OBJECT_TYPES:
            raise InvalidPostBody(
                f"'object_type' must be one of {sorted(PERMISSION_OBJECT_TYPES)} for Data Product permissions"
            )
        if self.role not in PERMISSION_ROLES:
            raise InvalidPostBody(
                f"'role' must be one of {sorted(PERMISSION_ROLES)} for Data Product permissions"
            )

        return {
            "subject_type": self.subject_type,
            "subject_id": self.subject_id,
            "object_type": self.object_type,
            "object_id": self.object_id,
            "role": self.role,
        }


@dataclass(kw_only=True)
class DataProductPermissionParams(BaseParams):
    """Optional filters for listing permissions."""

    subject_type: str = field(default=None)
    subject_id: str = field(default=None)
    object_type: str = field(default=None)
    object_id: str = field(default=None)
    role: str = field(default=None)

    def generate_params_dict(self) -> dict[str, Any]:
        """Generate query parameters for listing permissions."""

        params = {}
        if (self.subject_type is None) != (self.subject_id is None):
            raise InvalidPostBody("'subject_type' and 'subject_id' must be provided together")
        if (self.object_type is None) != (self.object_id is None):
            raise InvalidPostBody("'object_type' and 'object_id' must be provided together")

        if self.subject_type is not None:
            params["subject_type"] = self.subject_type
            params["subject_id"] = self.subject_id
        if self.object_type is not None:
            params["object_type"] = self.object_type
            params["object_id"] = self.object_id
        if self.role is not None:
            params["role"] = self.role
        return params
