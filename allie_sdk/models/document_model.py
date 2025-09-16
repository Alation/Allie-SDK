
"""Alation REST API Documents Data Models."""

from dataclasses import dataclass, field
from ..core.data_structures import BaseClass, BaseParams
from .custom_field_model import CustomFieldValue, CustomFieldValueItem
from ..core.custom_exceptions import validate_rest_payload, InvalidPostBody

@dataclass(kw_only = True)
class DocumentBase(BaseClass):
    title:str = field(default = None)
    description:str = field(default = None)
    template_id:int = field(default = None)
    # folder_ids:list[int] = field(default = None) # DEPRECATED IN 2024.3.2
    parent_folder_id: int = field(default = None)  # ADDED IN 2024.3.2
    parent_document_id: int = field(default = None)  # ADDED IN 2024.3.2
    nav_link_folder_ids: list[int] = field(default=None) # ADDED IN 2024.3.2
    document_hub_id:int = field(default = None)
    custom_fields:list[CustomFieldValueItem] = field(default = None)

@dataclass(kw_only = True)
class Document(DocumentBase):
    id:int = field(default = None)
    deleted:bool = field(default = False)
    ts_deleted:str = field(default = None)
    # is_public:bool = field(default = False) => was removed Apr 2024
    ts_created:str = field(default = None)
    ts_updated:str = field(default = None)
    # otype:str = field(default = None) => was removed Apr 2024

    def __post_init__(self):
        # convert to proper timestamps
        if isinstance(self.ts_created, str):
            self.ts_created = self.convert_timestamp(self.ts_created)
        if isinstance(self.ts_deleted, str):
            self.ts_deleted = self.convert_timestamp(self.ts_deleted)
        if isinstance(self.ts_updated, str):
            self.ts_updated = self.convert_timestamp(self.ts_updated)
        # Make sure the nested custom fields gets converted to the proper data class
        if isinstance(self.custom_fields, list):
            self.custom_fields = [CustomFieldValue.from_api_response(value) for value in self.custom_fields]



@dataclass(kw_only = True)
class DocumentPostItem(DocumentBase):

    # TODO: MOVE OUTSIDE, duplicate
    def _create_fields_payload(self) -> list:
        item: CustomFieldValueItem
        validate_rest_payload(self.custom_fields, (CustomFieldValueItem,))

        return [
            {
                'field_id': item.field_id
                , 'value': item.get_field_values()
            }
            for item in self.custom_fields
        ]

    # PREPARE PAYLOAD
    # make sure payload includes only fields with values
    def generate_api_post_payload(self) -> dict:
        # validate mandatory fields
        if self.title is None:
            raise InvalidPostBody("'title' is a required field for Document POST payload body")
        if self.document_hub_id is None:
            raise InvalidPostBody("'document_hub_id' is a required field for Document POST payload body")

        # create payload
        payload = {'title': self.title}
        if self.description:
            payload['description'] = self.description
        if self.template_id:
            payload['template_id'] = self.template_id
        if self.parent_folder_id:
            payload['parent_folder_id'] = self.parent_folder_id
        if self.nav_link_folder_ids:
            payload['nav_link_folder_ids'] = sorted(self.nav_link_folder_ids)
        if self.parent_document_id:
            payload['parent_document_id'] = self.parent_document_id
        if self.document_hub_id:
            payload['document_hub_id'] = self.document_hub_id
        if self.custom_fields:
            payload['custom_fields'] = self._create_fields_payload()

        return payload

@dataclass(kw_only = True)
class DocumentPutItem(DocumentBase):
    id:int # mandatory

    # TODO: MOVE OUTSIDE, duplicate
    def _create_fields_payload(self) -> list:
        item: CustomFieldValueItem
        validate_rest_payload(self.custom_fields, (CustomFieldValueItem,))

        return [
            {
                'field_id': item.field_id
                , 'value': item.get_field_values()
            }
            for item in self.custom_fields
        ]
    
    # PREPARE PAYLOAD
    # make sure payload includes only fields with values
    def generate_api_put_payload(self) -> dict:
        if self.id is None:
            raise InvalidPostBody("'id' is a required field for Document PUT payload body")
        payload = {'id': self.id}
        if self.title:
            payload['title'] = self.title
        if self.description:
            payload['description'] = self.description
        if self.template_id:
            payload['template_id'] = self.template_id
        if self.parent_folder_id:
            payload['parent_folder_id'] = self.parent_folder_id
        if self.nav_link_folder_ids:
            payload['nav_link_folder_ids'] = sorted(self.nav_link_folder_ids)
        if self.parent_document_id:
            payload['parent_document_id'] = self.parent_document_id
        if self.document_hub_id:
            payload['document_hub_id'] = self.document_hub_id
        if self.custom_fields:
            payload['custom_fields'] = self._create_fields_payload()

        return payload
    

# class for REST API Get filter values
@dataclass(kw_only = True)
class DocumentParams(BaseParams):
    id:int = field(default_factory = set)
    folder_id:int = field(default = None)
    document_hub_id:int = field(default = None)
    parent_folder_id:int = field(default = None)
    parent_document_id:int = field(default = None)
    nav_link_folder_id:int = field(default = None)
    search:str = field(default = None)
    deleted:bool = field(default = False)
    values:str = field(default=None)
