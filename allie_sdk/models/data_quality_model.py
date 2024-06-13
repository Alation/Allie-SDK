"""Alation REST API Data Quality Data Models."""

from dataclasses import dataclass, field, fields
from datetime import datetime

from ..core.custom_exceptions import InvalidPostBody
from ..core.data_structures import BaseClass, BaseParams


@dataclass
class DataQualityField(BaseClass):
    key: str = field(default=None)
    name: str = field(default=None)
    description: str = field(default=None)
    type: str = field(default=None)
    ts_created: datetime = field(default=None)

    def __post_init__(self):
        if isinstance(self.ts_created, str):
            self.ts_created = self.convert_timestamp(self.ts_created)


@dataclass
class DataQualityFieldItem:
    field_key: str = field(default=None)
    name: str = field(default=None)
    type: str = field(default=None)
    description: str = field(default=None)

    def generate_api_post_payload(self) -> dict:
        payload = {}
        for item in [self.field_key, self.name, self.type]:
            if item is None:
                raise InvalidPostBody(
                    f"'field_key', 'name', and 'type' are all required fields for the DQ Field API POST Call")

        if self.type.upper() not in ['NUMERIC', 'STRING', 'BOOLEAN']:
            raise InvalidPostBody(
                f"The value '{self.type}' is not a supported 'type' value.\n"
                f"Please update the value to: 'NUMERIC', 'STRING', or 'BOOLEAN'")
        else:
            self.type = self.type.upper()

        for item in fields(self):
            value = getattr(self, item.name)
            if value is not None:
                payload[item.name] = value

        return payload


@dataclass
class DataQualityFieldParams(BaseParams):
    key: set = field(default_factory=set)


@dataclass
class DataQualityValue(BaseClass):
    object_key: str = field(default=None)
    object_name: str = field(default=None)
    otype: str = field(default=None)
    oid: int = field(default=None)
    source_object_key: str = field(default=None)
    source_object_name: str = field(default=None)
    source_otype: str = field(default=None)
    source_oid: int = field(default=None)
    value_id: int = field(default=None)
    value_value: str | float | bool = field(default=None)
    value_quality: str = field(default=None)
    value_last_updated: datetime = field(default=None)
    value_external_url: str = field(default=None)
    field_key: str = field(default=None)
    field_name: str = field(default=None)
    field_description: str = field(default=None)

    def __post_init__(self):
        if isinstance(self.value_last_updated, str):
            self.value_last_updated = self.convert_timestamp(self.value_last_updated)

    def generate_api_delete_payload(self) -> dict:
        for item in [self.field_key, self.object_key]:
            if item is None:
                raise InvalidPostBody(
                    f"'field_key' and 'object_key' are all required fields for the DQ Value API DELETE Call")

        return {'field_key': self.field_key, 'object_key': self.object_key}


@dataclass
class DataQualityValueItem:
    field_key: str = field(default=None)
    object_key: str = field(default=None)
    object_type: str = field(default=None)
    status: str = field(default=None)
    value: str | float | bool = field(default=None)
    url: str = field(default=None)
    last_updated: str = field(default=None)

    def generate_api_post_payload(self) -> dict:
        payload = {}
        for item in [self.field_key, self.object_key, self.object_type, self.status, self.value]:
            if item is None:
                raise InvalidPostBody(
                    f"'field_key', 'object_key', 'object_type', 'status', and 'value' are all required "
                    f"fields for the API POST Call")

        if self.object_type.upper() not in ['ATTRIBUTE', 'TABLE', 'SCHEMA']:
            raise InvalidPostBody(
                f"The value '{self.object_type}' is not a supported 'object_type' value.\n"
                f"Please update the value to: 'ATTRIBUTE', 'TABLE', or 'SCHEMA'")
        else:
            self.object_type = self.object_type.upper()

        if self.status.upper() not in ['GOOD', 'WARNING', 'ALERT']:
            raise InvalidPostBody(
                f"The value '{self.status}' is not a supported 'status' value.\n"
                f"Please update the value to: 'GOOD', 'WARNING', or 'ALERT'")
        else:
            self.status = self.status.upper()

        for item in fields(self):
            value = getattr(self, item.name)
            if value is not None:
                payload[item.name] = value

        return payload


@dataclass
class DataQualityValueParams(BaseParams):
    object_key: set = field(default_factory=set)
    source_object_key: set = field(default_factory=set)
    field_key: set = field(default_factory=set)
    value_quality: set = field(default=None)
    hide_related: bool = field(default=None)
