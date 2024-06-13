
"""Alation REST API Group Data Models."""

from dataclasses import dataclass, field
from ..core.data_structures import BaseClass, BaseParams

@dataclass
class Group(BaseClass):
    display_name:str = field(default=None)
    email:str = field(default=None)
    id:int = field(default=None)
    profile_id:int = field(default=None)
    url:str = field(default=None)

@dataclass
class GroupParams(BaseParams):
    display_name:str = field(default = None)
    display_name__contains:str = field(default = None)
    display_name__icontains:str = field(default = None)
    email:str = field(default = None)
    email__contains:str = field(default = None)
    email__icontains:str = field(default = None)
    id:int = field(default = None)
    profile_id:int = field(default = None)
    order_by:str = field(default = None)
    values:str = field(default = None)

