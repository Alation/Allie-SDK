"""Alation REST API Query Data Models."""

from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime

from ..core.data_structures import BaseClass, BaseParams
from ..core.custom_exceptions import InvalidPostBody


# --- Auxiliary Models ---

@dataclass(kw_only=True)
class User(BaseClass):
    """Represents a user, typically the scheduler or owner."""
    username: str
    is_active: bool

@dataclass(kw_only=True)
class DBConnection(BaseClass):
    """Details for a specific database connection."""
    uri: str
    username: str
    ts_modified: str
    ts_last_used: str

    def __post_init__(self):
        self.ts_modified = self.convert_timestamp(self.ts_modified)
        self.ts_last_used = self.convert_timestamp(self.ts_last_used)

@dataclass(kw_only=True)
class LatestSession(BaseClass):
    """Details about the latest execution session of a schedule."""
    id: int
    client_session_id: str
    query_id: int
    ts_start: str
    sandbox_id: str
    batch_ids: list[int]

    def __post_init__(self):
        self.ts_start = self.convert_timestamp(self.ts_start)

@dataclass(kw_only=True)
class QuerySchedule(BaseClass):
    """Details for a single scheduled execution of the query."""
    enabled: bool
    cron_expression: str
    ts_last_attempt: str
    overdue: bool
    ts_next_run: str
    celery_queue: str
    celery_task_name: str
    user: dict
    db_connection: dict
    latest_session: dict

    def __post_init__(self):
        self.ts_last_attempt = self.convert_timestamp(self.ts_last_attempt)
        self.ts_next_run = self.convert_timestamp(self.ts_next_run)
        if isinstance(self.user, dict):
            self.user = User.from_api_response(self.user)
        if isinstance(self.db_connection, DBConnection):
            self.db_connection = DBConnection.from_api_response(self.db_connection)
        if isinstance(self.latest_session, LatestSession):
            self.latest_session = LatestSession.from_api_response(self.latest_session)

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
    schedules: list[QuerySchedule] = field(default=None)

    def __post_init__(self):
        if isinstance(self.ts_last_saved, str):
            self.ts_last_saved = self.convert_timestamp(self.ts_last_saved)

        if isinstance(self.domains, list):
            if len(self.domains) > 0:
                if not isinstance(self.domains[0], QueryDomain):
                    self.domains = [QueryDomain.from_api_response(domain) for domain in self.domains]

        if isinstance(self.tags, list):
            if len(self.tags) > 0:
                if not isinstance(self.tags[0], QueryTag):
                    self.tags = [QueryTag.from_api_response(tag) for tag in self.tags]

        if isinstance(self.datasource, dict):
            self.datasource = QueryDatasource.from_api_response(self.datasource)

        if isinstance(self.schedules, list):
            if len(self.schedules) > 0:
                if not isinstance(self.schedules[0], QuerySchedule):
                    self.schedules = [QuerySchedule.from_api_response(schedule) for schedule in self.schedules]


@dataclass(kw_only=True)
class QueryItem(BaseClass):
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


@dataclass
class QueryParams(BaseParams):
    """
    Data class representing the parameters for a URL query object.
    """

    # Core Query Parameters
    id: Optional[int] = None  # The numeric identifier of the query
    title: Optional[str] = None  # The query title
    description: Optional[str] = None  # The query description
    ts_last_saved: Optional[datetime] = None  # The date and time when the query was last saved
    autosave_content: Optional[str] = None  # Any unsaved content of the query
    content: Optional[str] = None  # The saved content of the query
    saved: Optional[bool] = None  # Whether the query has been saved
    published: Optional[bool] = None  # Whether the query has been published

    # Data Source Parameters
    datasource_id: Optional[int] = None  # The numeric identifer of the query's associated data source
    datasource_title: Optional[str] = None  # The title of the query's associated data source
    datasource_uri: Optional[str] = None  # The URI of the query's associated data source

    # Scheduling Parameters
    schedule_enabled: Optional[bool] = None  # Whether an associated schedule for the query is enabled
    schedule_cron_expression: Optional[str] = None  # The cron expression for a query's schedule
    schedule_ts_last_attempt: Optional[datetime] = None  # When a scheduled execution of a query was last attempted
    schedule_celery_task_name: Optional[str] = None  # The associated Celery task for the query's scheduled execution
    schedule_username: Optional[str] = None  # The name of the user who scheduled the query
    schedule_user_is_active: Optional[bool] = None  # Whether the user who scheduled the query is an active user
    schedule_db_uri: Optional[str] = None  # The URI to be used when the query is scheduled to execute
    schedule_db_ts_last_used: Optional[datetime] = None  # Last usage of db credentials for scheduled execution

    # Sorting Parameter
    order_by: Optional[str] = None  # Order results by field name