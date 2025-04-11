"""Alation REST API BI Source Models."""

import inspect
from ..core.custom_exceptions import InvalidPostBody, validate_rest_payload
from dataclasses import dataclass, field, fields
from ..core.data_structures import BaseClass, BaseParams
from datetime import datetime


@dataclass(kw_only = True)
class BaseBISourceParams(BaseParams):
    oids: set = field(default_factory=set)
    keyField: set = field(default_factory=set)


@dataclass(kw_only = True)
class BISourceParams(BaseBISourceParams):
    limit: set = field(default_factory=set)
    offset: set = field(default_factory=set)


@dataclass(kw_only = True)
class BaseBISourceItem:
    def class_to_dict(self, cls):
        # Generate dict from class with only fields that are not None
        return {item.name: getattr(cls, item.name) for item in fields(cls) if getattr(cls, item.name) is not None}


@dataclass(kw_only = True)
class BaseBISourceItemWithSharedFields(BaseBISourceItem):
    name: str
    external_id: str
    source_url: str
    bi_object_type: str
    description_at_source: str | None


# BI Server
@dataclass(kw_only = True)
class BIServerParams(BaseParams):
    oids: set = field(default_factory=set)


@dataclass(kw_only = True)
class NameConfiguration(BaseClass):
    bi_report: str = field(default=None)
    bi_datasource: str = field(default=None)
    bi_folder: str = field(default=None)
    bi_connection: str = field(default=None)


@dataclass(kw_only = True)
class BIServer(BaseClass):
    # The Numeric ID of the server
    id: int = field(default=None)
    # undocumented property
    type: str = field(default=None)
    # The uri of the underlying BI server
    uri: str = field(default=None)
    # The title of the underlying BI server
    title: str = field(default=None)
    # The description of the underlying BI server
    description: str = field(default=None)
    # Key-Value pairs matching BI object names to new user defined names.
    name_configuration: NameConfiguration = field(default=None)
    # Boolean flag determining if the BI Server is private. Defaults to False.
    private: bool = field(default=None)

    def __post_init__(self):
        if isinstance(self.name_configuration, dict):
            self.name_configuration = NameConfiguration.from_api_response(self.name_configuration)


@dataclass(kw_only = True)
class BIServerItem(BaseBISourceItem):
    uri: str = field(default=None)
    title: str = field(default=None)
    description: str = field(default=None)
    name_configuration: NameConfiguration = field(default=None)

    def generate_api_payload(self, method: str):
        """
        method is a string that can be either post or patch
        """

        if method == 'post':
            for item in [self.uri, self.title]:
                if item is None:
                    raise InvalidPostBody(
                        "'uri', and 'title' are required fields for BI Servers POST payload body")
        if method == 'patch':
            if self.uri is None:
                raise InvalidPostBody(
                    "'uri' is a required field for BI Server PATCH payload body")

        payload = {'uri': self.uri}
        if self.title:
            payload['title'] = self.title
        if self.description:
            payload['description'] = self.description
        if self.name_configuration:
            # payload['name_configuration'] = {k: v for k,v in self.name_configuration.__dict__.items() if v is not None}
            payload['name_configuration'] = self.class_to_dict(self.name_configuration)

        return payload


@dataclass(kw_only = True)
class UpdateBIServersSuccessResponse(BaseClass):
    Status: str = field(default=None)


@dataclass(kw_only = True)
class CreateBIServersSuccessResponse(UpdateBIServersSuccessResponse):
    Count: int = field(default=None)
    ServerIDs: list = field(default=None)
    Errors: list = field(default=None)

    @classmethod
    def _from_api_response(cls, body_params: dict):
        return cls(**{
            k.replace(' ', ''): v for k, v in body_params.items()
            if k.replace(' ', '') in inspect.signature(cls).parameters
        })


# BI Folder
@dataclass(kw_only = True)
class BIFolder(BaseClass):
    id: int = field(default=None)
    name: str = field(default=None)
    external_id: str = field(default=None)
    source_url: str = field(default=None)
    bi_object_type: str = field(default=None)
    description_at_source: str = field(default=None)
    owner: str = field(default=None)
    created_at: datetime = field(default=None)
    last_updated: datetime = field(default=None)
    num_reports: int = field(default=None)
    num_report_accesses: int = field(default=None)
    parent_folder: str = field(default=None)
    popularity: str = field(default=None)
    subfolders: list = field(default=None)
    connections: list = field(default=None)
    reports: list = field(default=None)

    def __post_init__(self):
        if isinstance(self.created_at, str):
            self.created_at = self.convert_timestamp(self.created_at)
        if isinstance(self.last_updated, str):
            self.last_updated = self.convert_timestamp(self.last_updated)


@dataclass(kw_only = True)
class BIFolderItem(BaseBISourceItemWithSharedFields):
    owner: str
    created_at: datetime = field(default=None)
    last_updated: datetime = field(default=None)
    num_reports: int = field(default=None)
    num_report_accesses: int = field(default=None)
    parent_folder: str = field(default=None)

    def generate_api_payload(self):
        payload = self.class_to_dict(self)

        return payload


# BI Report
@dataclass(kw_only = True)
class BIReportItem(BaseBISourceItemWithSharedFields):
    owner: str
    report_type: str
    created_at: datetime = field(default=None)
    last_updated: datetime = field(default=None)
    num_accesses: int = field(default=None)
    popularity: int = field(default=None)
    parent_folder: str = field(default=None)
    parent_reports: list = field(default=None)
    parent_datasources: list = field(default=None)

    def generate_api_payload(self):
        payload = self.class_to_dict(self)

        return payload


@dataclass(kw_only = True)
class BIReport(BaseClass):
    id: int = field(default=None)
    name: str = field(default=None)
    external_id: str = field(default=None)
    source_url: str = field(default=None)
    bi_object_type: str = field(default=None)
    description_at_source: str = field(default=None)
    owner: str = field(default=None)
    report_type: str = field(default=None)
    created_at: datetime = field(default=None)
    last_updated: datetime = field(default=None)
    num_accesses: int = field(default=None)
    popularity: int = field(default=None)
    parent_folder: str = field(default=None)
    parent_reports: list = field(default=None)
    parent_datasources: list = field(default=None)
    sub_reports: list = field(default=None)
    report_columns: list = field(default=None)


# BI Report Column
@dataclass(kw_only = True)
class BIReportColumnItem(BaseBISourceItemWithSharedFields):
    data_type: str = field(default=None)
    role: str = field(default=None)
    expression: str = field(default=None)
    values: list = field(default=None)
    report: str = field(default=None)
    created_at: datetime = field(default=None)
    last_updated: datetime = field(default=None)
    parent_report_columns: list = field(default=None)
    parent_datasource_columns: list = field(default=None)

    def generate_api_payload(self):
        payload = self.class_to_dict(self)
        print(payload)

        return payload

