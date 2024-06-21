"""Alation REST API Virtual Data Source Model."""
import dataclasses
import json
from dataclasses import dataclass, field

from ..core.custom_exceptions import InvalidPostBody
from ..core.data_structures import BaseClass, BaseParams

@dataclass
class VirtualDataSource(BaseClass):
    pass

@dataclass
class VirtualDataSourceParams(BaseParams):
    set_title_descs: bool = field(default=None)
    remove_not_seen: bool = field(default=None)


@dataclass
class VirtualDataSourceItem(BaseClass):
    key: str = field(default=None)
    description: str = field(default=None)
    title: str = field(default=None)

    def generate_api_post_payload(self) -> dict:
        if self.key is None:
            raise InvalidPostBody("'key' is required for metadata object payload.")

        return dataclasses.asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})

@dataclass
class VirtualDataSourceSchema(VirtualDataSourceItem):

    def generate_api_post_payload(self) -> dict:
        return dataclasses.asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})

@dataclass
class VirtualDataSourceTable(VirtualDataSourceItem):
    _table_type = "TABLE"
    data_location: str = field(default=None)
    db_owner: str = field(default=None)
    definition_sql: str = field(default=None)
    constraint_text: str = field(default=None)
    ts_created: str = field(default=None)
    ts_last_altered: str = field(default=None)
    partitioning_attributes: list = field(default=None)
    bucket_attributes: list = field(default=None)
    sort_attributes: list = field(default=None)
    synonyms: list = field(default=None)
    skews_info: dict = field(default=None)
    table_comment: str = field(default=None)

    def generate_api_post_payload(self) -> dict:
        return_dict = dataclasses.asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})
        return_dict["table_type"] = self._table_type
        return return_dict

@dataclass
class VirtualDataSourceView(VirtualDataSourceItem):
    _table_type = "VIEW"
    db_owner: str = field(default=None)
    view_sql: str = field(default=None)
    view_sql_expanded: str = field(default=None)
    ts_created: str = field(default=None)
    ts_last_altered: str = field(default=None)
    partitioning_attributes: list = field(default=None)
    bucket_attributes: list = field(default=None)
    sort_attributes: list = field(default=None)
    bucket_attributed: list = field(default=None)
    synonyms: list = field(default=None)
    skews_info: dict = field(default=None)
    table_comment: str = field(default=None)

    def generate_api_post_payload(self) -> dict:
        return_dict = dataclasses.asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})
        return_dict["table_type"] = self._table_type
        return return_dict

@dataclass
class VirtualDataSourceColumn(VirtualDataSourceItem):
    column_type: str = field(default=None)
    position: int = field(default=None)
    column_comment: str = field(default=None)
    nullable: bool = field(default=None)

    def generate_api_post_payload(self) -> dict:
        return dataclasses.asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})

@dataclass
class VirtualDataSourceIndex(VirtualDataSourceItem):
    index_type: str = field(default=None)
    column_names: list = field(default=None)
    data_structure: str = field(default=None)
    index_type_detail: str = field(default=None)
    is_ascending: bool = field(default=None)
    filter_condition: str = field(default=None)
    is_foreign_key: bool = field(default=None)
    foreign_key_table_name: str = field(default=None)
    foreign_key_column_names: list = field(default=None)

    def generate_api_post_payload(self) -> dict:

        if self.index_type is None:
            raise InvalidPostBody("'index_type' is required for index POST payload.")

        if self.column_names is None:
            raise InvalidPostBody("'column_names' is required for index POST payload.")

        if self.is_foreign_key:
            if self.foreign_key_table_name is None:
                raise InvalidPostBody("'foreign_key_table_name' is required for "
                                      "index POST payload, when is_foreign_key is true.")
            if self.foreign_key_column_names is None:
                raise InvalidPostBody("'foreign_key_column_names' is required for "
                                      "index POST payload, when is_foreign_key is true.")

        return dataclasses.asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})





