
"""Alation REST API User Data Models."""

from dataclasses import dataclass, field
from datetime import datetime
from ..core.data_structures import BaseClass, BaseParams

TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

@dataclass
class PolicyGroupStewardsField(BaseClass):
    otype:str = field(default=None)
    oid:int = field(default=None)
    otype_display_name:str = field(default=None)
    name:str = field(default=None)
    url:str = field(default=None)

@dataclass
class PolicyGroup(BaseClass):
    description: str = field(default=None)
    title: str = field(default=None)
    id: int = field(default=None)
    otype: str = field(default=None)
    ts_created: datetime = field(default=None)
    url: str = field(default=None)
    stewards: list[PolicyGroupStewardsField] = field(default=None)
    policies_count: int = field(default=None)

# class for REST API Get filter values
@dataclass
class PolicyGroupParams(BaseParams):
    id:int = field(default_factory = set)
    order_by:str = field(default = None)
    search:str = field(default = None)