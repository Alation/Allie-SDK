"""Alation REST API Document Hub Folders Data Models."""

from dataclasses import dataclass, field
from ..core.data_structures import BaseClass, BaseParams
from .custom_field_model import CustomFieldValue, CustomFieldValueItem
from ..core.custom_exceptions import validate_rest_payload, InvalidPostBody

@dataclass(kw_only = True)
class DocumentHubFolderBase(BaseClass):
    title:str = field(default = None)
    description:str = field(default = None)
    document_hub_id:int = field(default = None)
    custom_fields:list[CustomFieldValueItem] = field(default = None)

    # the following method is used for post and put methods only
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

@dataclass(kw_only = True)
class DocumentHubFolder(DocumentHubFolderBase):
    id:int = field(default = False)
    # id is not mandatory for the get request you can pick the values you want to extract
    # so id does not necessarily have to be part of this values list
    template_id: int = field(default=None)
    # Note: Document Hub Folders can have only on template. It is present in the GET response
    # as it may still be useful to know, e.g. to fetch data about the template via the custom template public API
    deleted:bool = field(default = False)
    ts_deleted:str = field(default = None)
    ts_created:str = field(default = None)
    ts_updated:str = field(default = None)

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
class DocumentHubFolderPostItem(DocumentHubFolderBase):

    # PREPARE PAYLOAD
    # make sure payload includes only fields with values
    def generate_api_post_payload(self) -> dict:
        # validate mandatory fields
        if self.title is None:
            raise InvalidPostBody("'title' is a required field for Document Hub Folder POST payload body")
        if self.document_hub_id is None:
            raise InvalidPostBody("'document_hub_id' is a required field for Document Hub Folder POST payload body")

        # create payload
        payload = {'title': self.title}
        if self.description:
            payload['description'] = self.description
        if self.document_hub_id:
            payload['document_hub_id'] = self.document_hub_id
        if self.custom_fields:
            payload['custom_fields'] = self._create_fields_payload()

        return payload

@dataclass(kw_only = True)
class DocumentHubFolderPutItem(DocumentHubFolderBase):
    id:int = field(default = None)

    # PREPARE PAYLOAD
    # make sure payload includes only fields with values
    def generate_api_put_payload(self) -> dict:
        # validate mandatory fields
        if self.id is None:
            raise InvalidPostBody("'id' is a required field for Document Hub Folder PUT payload body")

        # create payload
        payload = {'id': self.id}
        if self.title:
            payload['title'] = self.title
        if self.description:
            payload['description'] = self.description
        if self.document_hub_id:
            payload['document_hub_id'] = self.document_hub_id
        if self.custom_fields:
            payload['custom_fields'] = self._create_fields_payload()

        return payload
@dataclass(kw_only = True)
class DocumentHubFolderParams(BaseParams):
    id:int = field(default = None)
    document_hub_id:int = field(default = None)
    search:str = field(default = None)
    deleted:bool = field(default = False)
    values:str = field(default = None)