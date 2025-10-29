"""Alation REST API Query Data Models."""

from dataclasses import dataclass, field, asdict
from datetime import datetime

from ..core.data_structures import BaseClass
from ..core.custom_exceptions import InvalidPostBody


@dataclass(kw_only=True)
class QueryAuthor(BaseClass):
    """Author details that can be assigned to a query."""

    id: int = field(default=None)
    email: str = field(default=None)
    username: str = field(default=None)

    def to_payload(self) -> dict:
        """Serialize the author values while removing empty entries."""

        payload = {key: value for key, value in asdict(self).items() if value is not None}
        if not payload:
            raise InvalidPostBody(
                "'author' requires at least one identifier field such as id, email, or username."
            )
        return payload


@dataclass(kw_only=True)
class QueryDomain(BaseClass):
    """Domain metadata associated with a query."""

    title: str = field(default=None)
    id: int = field(default=None)
    description: str = field(default=None)


@dataclass(kw_only=True)
class QueryTag(BaseClass):
    """Tag metadata associated with a query."""

    id: int = field(default=None)
    name: str = field(default=None)
    description: str = field(default=None)
    ts_created: datetime | None = field(default=None)
    url: str = field(default=None)
    ts_updated: datetime | None = field(default=None)

    def __post_init__(self):
        if isinstance(self.ts_created, str):
            self.ts_created = self.convert_timestamp(self.ts_created)
        if isinstance(self.ts_updated, str):
            self.ts_updated = self.convert_timestamp(self.ts_updated)


@dataclass(kw_only=True)
class QueryDatasource(BaseClass):
    """Datasource reference returned with a query."""

    id: int = field(default=None)
    title: str = field(default=None)
    uri: str = field(default=None)
    url: str = field(default=None)


@dataclass(kw_only=True)
class Query(BaseClass):
    """Query metadata as returned from the Alation API."""

    datasource_id: int = field(default=None)
    autosave_content: str = field(default=None)
    content: str = field(default=None)
    title: str = field(default=None)
    saved: bool = field(default=None)
    published: bool = field(default=None)
    description: str = field(default=None)
    url: str = field(default=None)
    id: int = field(default=None)
    domains: list[QueryDomain] = field(default=None)
    tags: list[QueryTag] = field(default=None)
    datasource: QueryDatasource = field(default=None)
    ts_last_saved: datetime | None = field(default=None)
    has_unsaved_changes: bool = field(default=None)
    catalog_url: str = field(default=None)
    compose_url: str = field(default=None)
    schedules: list = field(default=None)

    def __post_init__(self):
        if isinstance(self.ts_last_saved, str):
            self.ts_last_saved = self.convert_timestamp(self.ts_last_saved)

        if isinstance(self.domains, list):
            self.domains = [QueryDomain.from_api_response(domain) for domain in self.domains]

        if isinstance(self.tags, list):
            self.tags = [QueryTag.from_api_response(tag) for tag in self.tags]

        if isinstance(self.datasource, dict):
            self.datasource = QueryDatasource.from_api_response(self.datasource)


@dataclass(kw_only=True)
class QueryCreateRequest(BaseClass):
    """Payload used for creating a query."""

    datasource_id: int
    content: str
    saved: bool = field(default=True)
    published: bool = field(default=False)
    title: str = field(default=None)
    description: str = field(default=None)
    tag_names: list[str] = field(default=None)
    domain_ids: list[int] = field(default=None)
    author: QueryAuthor | None = field(default=None)

    def generate_api_post_payload(self) -> dict:
        """Generate the API payload for creating a query."""

        if self.datasource_id is None:
            raise InvalidPostBody("'datasource_id' is a required field for Query POST payload body")
        if self.content is None:
            raise InvalidPostBody("'content' is a required field for Query POST payload body")

        payload: dict = {
            "datasource_id": self.datasource_id,
            "content": self.content,
        }

        if self.saved is not None:
            payload["saved"] = self.saved
        if self.published is not None:
            payload["published"] = self.published
        if self.title:
            payload["title"] = self.title
        if self.description:
            payload["description"] = self.description
        if self.tag_names:
            payload["tag_names"] = self.tag_names
        if self.domain_ids:
            payload["domain_ids"] = self.domain_ids
        if self.author:
            payload["author"] = self.author.to_payload()

        return payload
