"""Alation REST API Custom Field Data Models."""

from dataclasses import dataclass, field
from datetime import datetime
from dateutil.parser import parse

from ..core.custom_exceptions import InvalidPostBody
from ..core.data_structures import BaseClass, BaseParams


@dataclass(kw_only = True)
class CustomField(BaseClass):
    allow_multiple: bool = field(default=None)
    allowed_otypes: list = field(default=None)
    backref_name: str = field(default=None)
    backref_tooltip_text: str = field(default=None)
    builtin_name: str = field(default=None)
    field_type: str = field(default=None)
    id: int = field(default=None)
    name_plural: str = field(default=None)
    name_singular: str = field(default=None)
    options: list = field(default=None)
    tooltip_text: str = field(default=None)

@dataclass(kw_only = True)
class CustomFieldItem(BaseClass):
    """
    Originally we didn't inherit from the BaseClass here
    The reason why we added it was that if someone has already
    a dict with the same structure, they can use the
    from_api_response() method to easily convert it to this class
    """
    allow_multiple: bool = field(default=None)
    allowed_otypes: list = field(default=None)
    backref_name: str = field(default=None)
    backref_tooltip_text: str = field(default=None)
    field_type: str = field(default=None)
    name_plural: str = field(default=None)
    name_singular: str = field(default=None)
    options: list = field(default=None)
    tooltip_text: str = field(default=None)

    def generate_api_post_payload(self) -> dict:
        if self.field_type.upper() not in ['OBJECT_SET', 'PICKER', 'MULTI_PICKER', 'RICH_TEXT', 'DATE']:
            raise InvalidPostBody(f"The field type '{self.field_type}' is not supported")

        payload = {'field_type': self.field_type.upper()}

        if self.field_type.upper() == 'PICKER':
            for item in [self.name_singular, self.options]:
                if item is None:
                    raise InvalidPostBody(
                        "'name_singular' and 'options' are required fields for Picker Custom Fields POST Payload Body")
            picker = {'name_singular': self.name_singular, 'options': self.options}
            if self.tooltip_text:
                picker['tooltip_text'] = self.tooltip_text
            payload.update(picker)

        if self.field_type.upper() == 'MULTI_PICKER':
            for item in [self.name_singular, self.name_plural, self.options]:
                if item is None:
                    raise InvalidPostBody("'name_singular', 'name_plural', and 'options' are required fields "
                                          "for Multi-Picker Custom Fields POST Payload Body")
            multi_picker = {'name_singular': self.name_singular, 'name_plural': self.name_plural,
                            'options': self.options}
            if self.tooltip_text:
                multi_picker['tooltip_text'] = self.tooltip_text
            payload.update(multi_picker)

        if self.field_type.upper() == 'RICH_TEXT':
            if self.name_singular is None:
                raise InvalidPostBody(
                    "'name_singular' is a required field for Rich Text Custom Fields POST Payload Body")
            rich_text = {'name_singular': self.name_singular}
            if self.tooltip_text:
                rich_text['tooltip_text'] = self.tooltip_text
            payload.update(rich_text)

        if self.field_type.upper() == 'DATE':
            if self.name_singular is None:
                raise InvalidPostBody("'name_singular' is a required field for Date Custom Fields POST Payload Body")
            date = {'name_singular': self.name_singular}
            if self.tooltip_text:
                date['tooltip_text'] = self.tooltip_text
            payload.update(date)

        if self.field_type.upper() == 'OBJECT_SET':
            for item in [self.allow_multiple, self.allowed_otypes, self.backref_name, self.name_singular]:
                if item is None:
                    raise InvalidPostBody(
                        "'allowed_multiple', 'allowed_otypes', 'backref_name', and "
                        "'name_singular' are required fields for Object Set Custom Fields POST Payload Body")
            if self.allow_multiple:
                if self.name_plural is None:
                    raise InvalidPostBody("'name_plural' is a require field when allow_multiple is True "
                                          "for Object Set Custom Fields POST Payload Body.")
            for item in self.allowed_otypes:
                if item not in ['data', 'schema', 'table', 'attribute', 'user', 'groupprofile',
                                'article', 'glossary_term', 'glossary_v3', 'business_policy']:
                    raise InvalidPostBody(f"The otype '{item}' is not supported")
            object_set = {'allow_multiple': self.allow_multiple, 'allowed_otypes': self.allowed_otypes,
                          'backref_name': self.backref_name, 'name_singular': self.name_singular}
            if self.allow_multiple:
                object_set['name_plural'] = self.name_plural
            if self.backref_tooltip_text:
                object_set['backref_tooltip_text'] = self.backref_tooltip_text
            if self.tooltip_text:
                object_set['tooltip_text'] = self.tooltip_text
            payload.update(object_set)

        return payload


@dataclass(kw_only = True)
class CustomFieldParams(BaseParams):
    id: set = field(default_factory=set)
    allow_multiple: bool = field(default=False)
    field_type: set = field(default_factory=set)
    name_plural: set = field(default_factory=set)
    name_plural__contains: set = field(default_factory=set)
    name_plural__icontains: set = field(default_factory=set)
    name_singular: set = field(default_factory=set)
    name_singular__contains: set = field(default_factory=set)
    name_singular__icontains: set = field(default_factory=set)
    tooltip_text: set = field(default_factory=set)
    tooltip_text__contains: set = field(default_factory=set)
    tooltip_text__icontains: set = field(default_factory=set)


@dataclass(kw_only = True)
class CustomFieldStringValue:
    value: str = field(default=None)

@dataclass(kw_only = True)
class CustomFieldStringValueItem(CustomFieldStringValue):
    def return_value(self) -> str:
        return self.value


@dataclass(kw_only = True)
class CustomFieldDictValue:
    otype: str = field(default=None)
    oid: int = field(default=None)

@dataclass(kw_only = True)
class CustomFieldDictValueItem(CustomFieldDictValue):
    def return_value(self) -> dict:
        return {
            'otype': self.otype.lower()
            , 'oid': self.oid
        }


@dataclass(kw_only = True)
class _BaseCustomFieldValue(BaseClass):
    field_id: int = field(default=None)
    ts_updated: datetime = field(default=None)
    otype: str = field(default=None)
    oid: int = field(default=None)


@dataclass(kw_only = True)
class CustomFieldValue(_BaseCustomFieldValue):
    field_name:str = field(default=None) # this is only returned by some endpoints, e.g. documents API
    value: CustomFieldStringValue | list[CustomFieldStringValue | CustomFieldDictValue] = field(default=None)

    def __post_init__(self):
        if self.value:
            self._parse_field_values()
        if isinstance(self.ts_updated, str):
            self.ts_updated = self.convert_timestamp(self.ts_updated)

    def _parse_field_values(self):

        if isinstance(self.value, str):
            self.value = CustomFieldStringValue(value=self.value)

        if isinstance(self.value, list):

            parsed_values = []

            for item in self.value:
                # for multi-select picker values
                if isinstance(item, str):
                    parsed_values.append(
                        CustomFieldStringValue(
                            value = item
                        )
                    )
                # for object sets etc
                elif isinstance(item, dict):
                    parsed_values.append(
                        CustomFieldDictValue(
                            otype=item.get('otype', None)
                            , oid=item.get('oid', None)
                        )
                    )

                elif isinstance(item, CustomFieldStringValue):
                    parsed_values.append(item)
                elif isinstance(item, CustomFieldDictValue):
                    parsed_values.append(item)

            self.value = parsed_values

@dataclass(kw_only = True)
class CustomFieldValueItem(_BaseCustomFieldValue):
    value: CustomFieldStringValueItem | list[CustomFieldStringValueItem | CustomFieldDictValueItem] = field(default=None)

    def get_field_values(self) -> str | list:
        if isinstance(self.value, CustomFieldStringValueItem):
            return self.value.return_value()

        if isinstance(self.value, list):

            field_values = []
            for item in self.value:
                if isinstance(item, CustomFieldDictValueItem):
                    field_values.append(item.return_value())
                # for multi-picker values
                elif isinstance(item, CustomFieldStringValueItem):
                    field_values.append(item.return_value())

            return field_values
    def generate_api_put_payload(self) -> dict:
        for item in [self.field_id, self.otype, self.oid, self.value]:
            if not item:
                raise InvalidPostBody("'field_id', 'otype', 'oid', and 'value' are all "
                                      "required fields for Custom Field Values PUT payload body")
        payload = {
            'field_id': self.field_id
            , 'otype': self.otype.lower()
            , 'oid': self.oid
            , 'value': self.get_field_values()
        }

        if self.ts_updated:
            if isinstance(self.ts_updated, str):
                payload['ts_updated'] = parse(self.ts_updated).isoformat()
            if isinstance(self.ts_updated, datetime):
                payload['ts_updated'] = self.ts_updated.isoformat()

        return payload

@dataclass(kw_only = True)
class CustomFieldValueParams(BaseParams):
    otype: set = field(default_factory=set)
    oid: set = field(default_factory=set)
    field_id: set = field(default_factory=set)
