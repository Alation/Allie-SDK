"""Alation REST API Tag Data Models."""

from dataclasses import dataclass, field
from datetime import datetime

from ..core.custom_exceptions import InvalidPostBody
from ..core.data_structures import BaseClass, BaseParams


@dataclass
class Tag(BaseClass):
    """Tag metadata returned by the Tags API."""

    id: int = field(default=None)
    name: str = field(default=None)
    description: str = field(default=None)
    number_of_objects_tagged: int = field(default=None)
    ts_created: datetime = field(default=None)
    url: str = field(default=None)

    def __post_init__(self):
        if isinstance(self.ts_created, str):
            self.ts_created = self.convert_timestamp(self.ts_created)


@dataclass
class TaggedObjectRef(BaseClass):
    """Reference to an Alation object tagged with a specific tag."""

    url: str = field(default=None)
    otype: str = field(default=None)
    id: int | str = field(default=None)


@dataclass
class TaggedObject(BaseClass):
    """Tagged object response item."""

    ts_tagged: datetime = field(default=None)
    subject: TaggedObjectRef = field(default=None)

    def __post_init__(self):
        if isinstance(self.ts_tagged, str):
            self.ts_tagged = self.convert_timestamp(self.ts_tagged)
        if isinstance(self.subject, dict):
            self.subject = TaggedObjectRef.from_api_response(self.subject)


@dataclass
class TagObjectItem(BaseClass):
    """Request payload for adding a tag to an object."""

    oid: int | str = field(default=None)
    otype: str = field(default=None)

    def generate_api_post_payload(self) -> dict:
        if self.oid is None:
            raise InvalidPostBody("'oid' is a required field for Tag POST payload body")
        if self.otype is None:
            raise InvalidPostBody("'otype' is a required field for Tag POST payload body")

        return {
            "oid": self.oid,
            "otype": self.otype,
        }


@dataclass
class TagItem(BaseClass):
    """Request payload for updating a tag."""

    name: str = field(default=None)
    description: str = field(default=None)

    def generate_api_patch_payload(self) -> dict:
        payload = {}

        if self.name:
            payload["name"] = self.name
        if self.description is not None:
            payload["description"] = self.description

        if not payload:
            raise InvalidPostBody(
                "At least one of 'name' or 'description' is required for Tag PATCH payload body"
            )

        return payload


@dataclass
class TagParams(BaseParams):
    """Query parameters for listing tags."""

    oid: int | str = field(default=None)
    otype: str = field(default=None)
    limit: int = field(default=None)
    skip: int = field(default=None)
    order_by: str = field(default=None)


@dataclass
class TaggedObjectParams(BaseParams):
    """Query parameters for listing objects that have a specific tag."""

    limit: int = field(default=None)
    skip: int = field(default=None)
    order_by: str = field(default=None)
    exclude_deleted: bool = field(default=None)
