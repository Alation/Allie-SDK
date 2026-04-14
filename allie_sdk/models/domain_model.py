
"""Alation REST API Domains Data Models."""

from dataclasses import dataclass, field

from ..core.data_structures import BaseClass, BaseParams
from ..core.custom_exceptions import InvalidPostBody

@dataclass(kw_only = True)
class DomainBase(BaseClass):
    title:str = field(default = None)
    description:str = field(default = None)
    parent_id:int = field(default = None)


@dataclass(kw_only = True)
class Domain(DomainBase):
    id:int = field(default = None)


@dataclass(kw_only = True)
class DomainItem(DomainBase):
    def generate_api_post_payload(self) -> dict:
        if self.title is None:
            raise InvalidPostBody("'title' is a required field for Domain POST payload body")

        payload = {"title": self.title}

        if self.description is not None:
            payload["description"] = self.description
        if self.parent_id is not None:
            payload["parent_id"] = self.parent_id

        return payload


@dataclass(kw_only = True)
class DomainDeleteItem(BaseClass):
    id:int = field(default = None)

    def generate_api_delete_payload(self) -> dict:
        if self.id is None:
            raise InvalidPostBody("'id' is a required field for Domain DELETE payload body")

        return {"id": self.id}


@dataclass(kw_only = True)
class DomainMoveItem(BaseClass):
    parent_id:int = field(default = None)

    def generate_api_patch_payload(self) -> dict:
        if self.parent_id is None:
            raise InvalidPostBody("'parent_id' is a required field for Domain PATCH payload body")

        return {"parent_id": self.parent_id}

# class serves both for the POST payload and the response
@dataclass(kw_only = True)
class DomainMembership(BaseClass):
    id:int = field(default = None)
    oid:list[int] = field(default_factory = list)
    otype:str = field(default = None)
    exclude: bool = field(default=False)
    recursive: bool = field(default=False)

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

# class for viewing membership rules applied on a domain
@dataclass(kw_only = True)
class DomainMembershipRuleRequest(BaseClass):
    domain_ids: list[int] = field(default_factory=list)
    exclude: bool | None = field(default=None)
    recursive: bool | None = field(default=None)

    def generate_api_post_payload(self) -> dict:
        if not self.domain_ids:
            raise InvalidPostBody(
                "'domain_id' is a required field for the DomainMembershipRuleRequest POST payload body"
            )

        if self.exclude is None:
            raise InvalidPostBody(
                "'exclude' is a required field for the DomainMembershipRuleRequest POST payload body"
            )

        payload = {
            "domain_id": self.domain_ids,
            "exclude": self.exclude,
        }

        if self.recursive is not None:
            payload["recursive"] = self.recursive

        return payload


@dataclass(kw_only = True)
class DomainMembershipRule(BaseClass):
    domain_id: int = field(default=None)
    exclude: bool = field(default=None)
    recursive: bool = field(default=None)
    otype: str = field(default=None)
    oid: int = field(default=None)

# class for REST API Get filter values
@dataclass(kw_only = True)
class DomainParams(BaseParams):
    parent_id:int = field(default = None)
