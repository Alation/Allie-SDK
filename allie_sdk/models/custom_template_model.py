
"""Alation REST API User Data Models."""

from dataclasses import dataclass, field
from datetime import datetime
from ..core.data_structures import BaseClass, BaseParams
from .custom_field_model import CustomField
from ..core.custom_exceptions import validate_rest_payload, InvalidPostBody

TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

@dataclass
class CustomTemplate(BaseClass):
    id: int = field(default=None)
    builtin_name: str = field(default=None)
    layout_otype: int = field(default=None)
    title: str = field(default=None)
    visual_config_id: int = field(default=None)
    fields: list[CustomField] = field(default = None)

    def __post_init__(self):
        # Make sure the nested custom fields gets converted to the proper data class
        if isinstance(self.fields, list):
            self.fields = [CustomField.from_api_response(value) for value in self.fields]

@dataclass
class CustomTemplateParams(BaseParams):
    title:str = field(default = None)