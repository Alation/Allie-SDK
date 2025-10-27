"""Alation REST API Relational Integration Data Models."""

from dataclasses import dataclass, field

from .custom_field_model import CustomFieldValue, CustomFieldValueItem
from ..core.custom_exceptions import InvalidPostBody, validate_rest_payload
from ..core.data_structures import BaseClass, BaseParams


@dataclass
class BaseRDBMS(BaseClass):
    id: int = field(default=None)
    name: str = field(default=None)
    title: str = field(default=None)
    description: str = field(default=None)
    ds_id: int = field(default=None)
    key: str = field(default=None)
    url: str = field(default=None)
    custom_fields: str = field(default=None)

    def __post_init__(self):
        if isinstance(self.custom_fields, list):
            self.custom_fields = [CustomFieldValue.from_api_response(item) for item in self.custom_fields]


@dataclass
class BaseRDBMSItem:
    title: str = field(default=None)
    description: str = field(default=None)
    key: str = field(default=None)
    custom_fields: str = field(default=None)

    def _create_fields_payload(self) -> list:
        item: CustomFieldValueItem
        validate_rest_payload(self.custom_fields, (CustomFieldValueItem,))

        return [{'field_id': item.field_id, 'value': item.get_field_values()}
                    for item in self.custom_fields]


@dataclass
class BaseRDBMSParams(BaseParams):
    id: set = field(default_factory=set)
    name: set = field(default_factory=set)
    ds_id: set = field(default_factory=set)
    id__gt: set = field(default_factory=set)
    id__gte: set = field(default_factory=set)
    id__lt: set = field(default_factory=set)
    id__lte: set = field(default_factory=set)
    name__contains: set = field(default_factory=set)
    name__startswith: set = field(default_factory=set)
    name__endswith: set = field(default_factory=set)
    ds_id__gt: set = field(default_factory=set)
    ds_id__gte: set = field(default_factory=set)
    ds_id__lt: set = field(default_factory=set)
    ds_id__lte: set = field(default_factory=set)

@dataclass
class Schema(BaseRDBMS):
    db_comment: str = field(default=None)


@dataclass
class SchemaItem(BaseRDBMSItem):
    db_comment: str = field(default=None)

    def generate_api_post_payload(self):
        if self.key is None:
            raise InvalidPostBody("'key' is a required field for Schema POST payload body")
        payload = {'key': self.key}
        if self.title:
            payload['title'] = self.title
        if self.description:
            payload['description'] = self.description
        if self.db_comment:
            payload['db_comment'] = self.db_comment
        if self.custom_fields:
            payload['custom_fields'] = self._create_fields_payload()

        return payload


@dataclass
class SchemaPatchItem(BaseRDBMSItem):
    id: int = field(default=None)
    db_comment: str = field(default=None)

    def generate_api_patch_payload(self):
        if self.id is None:
            raise InvalidPostBody("'id' is a required field for Schema PATCH payload body")
        payload = {'id': self.id}
        if self.title:
            payload['title'] = self.title
        if self.description:
            payload['description'] = self.description
        if self.db_comment:
            payload['db_comment'] = self.db_comment
        if self.custom_fields:
            payload['custom_fields'] = self._create_fields_payload()

        return payload

@dataclass
class SchemaParams(BaseRDBMSParams):
    pass

@dataclass
class Table(BaseRDBMS):
    table_type: str = field(default=None)
    schema_id: int = field(default=None)
    schema_name: str = field(default=None)
    sql: str = field(default=None)
    table_comment: str = field(default=None)


@dataclass
class TableItem(BaseRDBMSItem):
    table_comment: str = field(default=None)
    table_type: str = field(default=None)
    table_type_name: str = field(default=None)
    owner: str = field(default=None)
    sql: str = field(default=None)
    base_table_key: str = field(default=None)
    partition_definition: str = field(default=None)
    partition_columns: list = field(default=None)

    def generate_api_post_payload(self):
        if self.key is None:
            raise InvalidPostBody("'key' is a required field for Table POST payload body")
        payload = {'key': self.key}
        if self.title:
            payload['title'] = self.title
        if self.description:
            payload['description'] = self.description
        if self.table_comment:
            payload['table_comment'] = self.table_comment
        if self.table_type:
            payload['table_type'] = self.table_type
            if self.table_type.upper() == 'SYNONYM':
                if self.base_table_key:
                    payload['base_table_key'] = self.base_table_key
        if self.table_type_name:
            payload['table_type_name'] = self.table_type_name
        if self.owner:
            payload['owner'] = self.owner
        if self.sql:
            payload['sql'] = self.sql
        if self.partition_definition:
            payload['partition_definition'] = self.partition_definition
        if self.partition_columns:
            payload['partition_columns'] = self.partition_columns
        if self.custom_fields:
            payload['custom_fields'] = self._create_fields_payload()

        return payload


@dataclass
class TablePatchItem(BaseRDBMSItem):
    id: int = field(default=None)
    table_comment: str = field(default=None)
    table_type: str = field(default=None)
    table_type_name: str = field(default=None)
    owner: str = field(default=None)
    sql: str = field(default=None)
    base_table_key: str = field(default=None)
    partition_definition: str = field(default=None)
    partition_columns: list = field(default=None)

    def generate_api_patch_payload(self):
        if self.id is None:
            raise InvalidPostBody("'id' is a required field for Table PATCH payload body")

        payload = {'id': self.id}
        if self.title:
            payload['title'] = self.title
        if self.description:
            payload['description'] = self.description
        if self.table_comment:
            payload['table_comment'] = self.table_comment
        if self.table_type:
            payload['table_type'] = self.table_type
        if self.table_type_name:
            payload['table_type_name'] = self.table_type_name
        if self.owner:
            payload['owner'] = self.owner
        if self.sql:
            payload['sql'] = self.sql
        if self.base_table_key:
            payload['base_table_key'] = self.base_table_key
        if self.partition_definition:
            payload['partition_definition'] = self.partition_definition
        if self.partition_columns:
            payload['partition_columns'] = self.partition_columns
        if self.custom_fields:
            payload['custom_fields'] = self._create_fields_payload()

        return payload


@dataclass
class TableParams(BaseRDBMSParams):
    schema_id: set = field(default_factory=set)
    schema_name: set = field(default_factory=set)
    name__iexact: set = field(default_factory=set)
    name__icontains: set = field(default_factory=set)
    name__istartswith: set = field(default_factory=set)
    name__iendswith: set = field(default_factory=set)
    schema_id__gt: set = field(default_factory=set)
    schema_id__gte: set = field(default_factory=set)
    schema_id__lt: set = field(default_factory=set)
    schema_id__lte: set = field(default_factory=set)
    schema_name__iexact: set = field(default_factory=set)
    schema_name__contains: set = field(default_factory=set)
    schema_name__icontains: set = field(default_factory=set)
    schema_name__startswith: set = field(default_factory=set)
    schema_name__istartswith: set = field(default_factory=set)
    schema_name__endswith: set = field(default_factory=set)
    schema_name__iendswith: set = field(default_factory=set)


@dataclass(kw_only = True)
class ColumnIndex(BaseClass):
    isPrimaryKey: bool = field(default=None)
    isForeignKey: bool = field(default=None)
    referencedColumnId: str = field(default=None)
    isOtherIndex: bool = field(default=None)

    def generate_api_post_payload(self):
        payload = {}
        if self.isPrimaryKey is not None:
            payload['isPrimaryKey'] = self.isPrimaryKey
        if self.isForeignKey is not None:
            payload['isForeignKey'] = self.isForeignKey
        if self.referencedColumnId:
            payload['referencedColumnId'] = self.referencedColumnId
        if self.isOtherIndex is not None:
            payload['isOtherIndex'] = self.isOtherIndex

        return payload

@dataclass
class Column(BaseRDBMS):
    column_type: str = field(default=None)
    column_comment: str = field(default=None)
    index: ColumnIndex = field(default=None)
    nullable: bool = field(default=None)
    schema_id: int = field(default=None)
    table_id: int = field(default=None)
    table_name: str = field(default=None)
    position: int = field(default=None)

    def __post_init__(self):
        if isinstance(self.custom_fields, list):
            self.custom_fields = [CustomFieldValue.from_api_response(item) for item in self.custom_fields]
        if isinstance(self.index, dict):
            self.index = ColumnIndex.from_api_response(self.index)


@dataclass
class ColumnItem(BaseRDBMSItem):
    column_type: str = field(default=None)
    column_comment: str = field(default=None)
    nullable: bool = field(default=None)
    position: int = field(default=None)
    index: ColumnIndex = field(default=None)

    def generate_api_post_payload(self):
        for item in [self.key, self.column_type]:
            if item is None:
                raise InvalidPostBody(
                    "'key', and 'column_type' are required fields for Column POST payload body")
        payload = {'key': self.key, 'column_type': self.column_type}
        if self.title:
            payload['title'] = self.title
        if self.description:
            payload['description'] = self.description
        if self.column_comment:
            payload['column_comment'] = self.column_comment
        if self.nullable is not None:
            payload['nullable'] = self.nullable
        if self.position:
            payload['position'] = self.position
        if self.index:
            payload['index'] = ColumnIndex.generate_api_post_payload(self.index)
        if self.custom_fields:
            payload['custom_fields'] = self._create_fields_payload()

        return payload


@dataclass
class ColumnPatchItem(BaseRDBMSItem):
    id: int = field(default=None)
    column_comment: str = field(default=None)
    nullable: bool = field(default=None)
    position: int = field(default=None)
    index: ColumnIndex = field(default=None)

    def generate_api_patch_payload(self):
        if self.id is None:
            raise InvalidPostBody("'id' is a required field for Column PATCH payload body")
        payload = {'id': self.id}
        if self.title:
            payload['title'] = self.title
        if self.description:
            payload['description'] = self.description
        if self.column_comment:
            payload['column_comment'] = self.column_comment
        if self.nullable is not None:
            payload['nullable'] = self.nullable
        if self.position:
            payload['position'] = self.position
        if self.index:
            payload['index'] = ColumnIndex.generate_api_post_payload(self.index)
        if self.custom_fields:
            payload['custom_fields'] = self._create_fields_payload()

        return payload

@dataclass
class ColumnParams(BaseRDBMSParams):
    table_id: set = field(default_factory=set)
    table_name: set = field(default_factory=set)
    schema_id: set = field(default_factory=set)
    name__iexact: set = field(default_factory=set)
    name__icontains: set = field(default_factory=set)
    name__istartswith: set = field(default_factory=set)
    name__iendswith: set = field(default_factory=set)
    table_id__gt: set = field(default_factory=set)
    table_id__gte: set = field(default_factory=set)
    table_id__lt: set = field(default_factory=set)
    table_id__lte: set = field(default_factory=set)
    table_name__iexact: set = field(default_factory=set)
    table_name__contains: set = field(default_factory=set)
    table_name__icontains: set = field(default_factory=set)
    table_name__startswith: set = field(default_factory=set)
    table_name__istartswith: set = field(default_factory=set)
    table_name__endswith: set = field(default_factory=set)
    table_name__iendswith: set = field(default_factory=set)
    schema_id__gt: set = field(default_factory=set)
    schema_id__gte: set = field(default_factory=set)
    schema_id__lt: set = field(default_factory=set)
    schema_id__lte: set = field(default_factory=set)
