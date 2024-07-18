
"""Alation REST API Domains Data Models."""

from dataclasses import dataclass, field
from ..core.data_structures import BaseClass, BaseParams
from ..core.custom_exceptions import validate_rest_payload, InvalidPostBody

@dataclass(kw_only = True)
class Domain(BaseClass):
    id:int = field(default = None)
    title:str = field(default = None)
    description:str = field(default = None)
    parent_id:int = field(default = None)

# class serves both for the POST payload and the response
@dataclass(kw_only = True)
class DomainMembership(BaseClass):
    id:int = field(default = None)
    exclude:bool = field(default = False)
    recursive: bool = field(default=False)
    oid:list[int] = field(default_factory = list)
    otype:str = field(default = None)

    # PREPARE PAYLOAD
    # make sure payload includes only fields with values
    def generate_api_post_payload(self) -> dict:
        if self.id is None or self.oid is None or self.otype is None:
            raise InvalidPostBody(f"id, oid and otype are required fields for the DomainMembership PUT payload body")
        payload = {
            "id": self.id
            , "oid": self.oid
            , "otype": self.otype
        }
        if self.exclude:
            payload['exclude'] = self.exclude
        if self.recursive:
            payload['recursive'] = self.recursive

        return payload

# class for REST API Get filter values
@dataclass(kw_only = True)
class DomainParams(BaseParams):
    parent_id:int = field(default = None)