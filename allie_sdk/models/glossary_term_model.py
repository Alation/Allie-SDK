"""Alation REST API Glossary Term Data Models."""

from dataclasses import dataclass, field
from datetime import datetime

from .custom_field_model import CustomFieldValue, CustomFieldValueItem
from ..core.custom_exceptions import validate_rest_payload, InvalidPostBody
from ..core.data_structures import BaseClass, BaseParams


@dataclass
class BaseGlossaryTerm(BaseClass):
    id: int = field(default=None)
    title: str = field(default=None)
    description: str = field(default=None)
    template_id: str = field(default=None)
    glossary_ids: list = field(default=None)
    custom_fields: list = field(default=None)

    def _create_fields_payload(self) -> list:
        item: CustomFieldValueItem
        validate_rest_payload(self.custom_fields, (CustomFieldValueItem,))

        return [{'field_id': item.field_id, 'value': item.get_field_values()}
                    for item in self.custom_fields]

    def generate_api_put_payload(self):
        if self.id is None:
            raise InvalidPostBody("'id' is a required field for Glossary Term PUT payload body")
        payload = {'id': self.id}
        if self.title:
            payload['title'] = self.title
        if self.description:
            payload['description'] = self.description
        if self.template_id:
            payload['template_id'] = self.template_id
        if self.glossary_ids:
            payload['glossary_ids'] = sorted(self.glossary_ids)
        if self.custom_fields:
            payload['custom_fields'] = self._create_fields_payload()

        return payload


@dataclass
class GlossaryTerm(BaseGlossaryTerm):
    ts_created: datetime = field(default=None)
    ts_updated: datetime = field(default=None)
    ts_deleted: datetime = field(default=None)
    deleted: bool = field(default=None)

    def __post_init__(self):
        if isinstance(self.ts_created, str):
            self.ts_created = self.convert_timestamp(self.ts_created)
        if isinstance(self.ts_updated, str):
            self.ts_updated = self.convert_timestamp(self.ts_updated)
        if isinstance(self.ts_deleted, str):
            self.ts_deleted = self.convert_timestamp(self.ts_deleted)
        if isinstance(self.custom_fields, list):
            self.custom_fields = [CustomFieldValue.from_api_response(value) for value in self.custom_fields]


@dataclass
class GlossaryTermItem(BaseGlossaryTerm):

    def generate_api_post_payload(self) -> dict:
        if self.title is None:
            raise InvalidPostBody("'title' is a required field for Glossary Term POST payload body")
        payload = {'title': self.title}
        if self.description:
            payload['description'] = self.description
        if self.template_id:
            payload['template_id'] = self.template_id
        if self.glossary_ids:
            payload['glossary_ids'] = sorted(self.glossary_ids)
        if self.custom_fields:
            payload['custom_fields'] = self._create_fields_payload()

        return payload


@dataclass
class GlossaryTermParams(BaseParams):
    id: set = field(default_factory=set)
    search: str = field(default=None)
    deleted: bool = field(default=False)
