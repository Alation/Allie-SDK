"""Alation REST API BI Source Models."""
from ..core.custom_exceptions import InvalidPostBody, validate_rest_payload
from dataclasses import dataclass, field, fields, asdict
from ..core.data_structures import BaseClass, BaseParams
from datetime import datetime
from typing import Optional

@dataclass(kw_only = True)
class BIObjectBaseParams(BaseParams):
    keyField: str = field(default=None, metadata={'description':'The type of ID used in the ObjectIDs parameter. Can be either "id" or "external_id".'})
    oids: str = field(default=None, metadata={'description': 'A comma-separated list of ObjectIDs to fetch.'})

    def __post_init__(self):
        if self.oids:
            if isinstance(self.oids, list):
                self.oids = ','.join(map(str, self.oids))

@dataclass(kw_only = True)
class BIFolderParams(BIObjectBaseParams):
    pass

@dataclass(kw_only = True)
class BIReportParams(BIObjectBaseParams):
    pass

@dataclass(kw_only = True)
class BaseBISourceItemWithSharedFields(BaseClass):
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
class BIServerNameConfiguration(BaseClass):
    bi_report: str = field(default=None)
    bi_datasource: str = field(default=None)
    bi_folder: str = field(default=None)
    bi_connection: str = field(default=None)

    def generate_api_payload(self) -> dict:
        payload = dict()

        # API endpoint validator throws error if rendered_otype is not present
        # so we add it in any case:
        if self.bi_report:
            payload['bi_report'] = self.bi_report
        if self.bi_datasource:
            payload['bi_datasource'] = self.bi_datasource
        if self.bi_folder:
            payload['bi_folder'] = self.bi_folder
        if self.bi_connection:
            payload['bi_connection'] = self.bi_connection

        return payload


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
    name_configuration: BIServerNameConfiguration = field(default=None)
    # Boolean flag determining if the BI Server is private. Defaults to False.
    private: bool = field(default=None)

    def __post_init__(self):
        if isinstance(self.name_configuration, dict):
            self.name_configuration = BIServerNameConfiguration.from_api_response(self.name_configuration)


@dataclass(kw_only = True)
class BIServerItem(BaseClass):
    uri: str = field(default=None)
    title: str = field(default=None)
    description: str = field(default=None)
    name_configuration: BIServerNameConfiguration = field(default=None)

    def generate_api_payload(self, method: str):
        """
        method is a string that can be either post or patch
        """

        if method == 'post':
            for item in [self.uri, self.title]:
                if item is None:
                    raise InvalidPostBody(
                        "'uri', and 'title' are required fields for BI Servers POST payload body"
                    )
        if method == 'patch':
            if self.uri is None:
                raise InvalidPostBody(
                    "'uri' is a required field for BI Server PATCH payload body"
                )

        payload = {'uri': self.uri}
        if self.title:
            payload['title'] = self.title
        if self.description:
            payload['description'] = self.description
        if self.name_configuration:
            payload['name_configuration'] = BIServerNameConfiguration.generate_api_payload(self.name_configuration)

        return payload

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
    datasources: list = field(default=None) # not listed in docu or yaml spec, but return by request call

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
        payload = asdict(
            self,
            dict_factory=lambda values: {
                key: value for key, value in values
                if value is not None
            }
        )

        return payload


# BI Report

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
        payload = asdict(
            self,
            dict_factory=lambda values: {
                key: value for key, value in values
                if value is not None
            }
        )

        return payload

# BI REPORT COLUMNS

@dataclass(kw_only=True)
class BIObjectBase(BaseClass):
    """Common properties of a BI Object"""
    id: int = field(metadata={'description': 'The auto-generated id of the object'})
    name: str = field(metadata={'description': 'The user-friendly name of the object'})
    external_id: str = field(metadata={'description': 'The identifier of the object as generated by the BI Server. This is used as an identifier for bulk create/update operations.'})
    created_at: Optional[datetime] = field(default=None, metadata={'description': 'Date and time of object creation on the BI Server'})
    last_updated: Optional[datetime] = field(default=None, metadata={'description': 'Most recent update time of the object on the BI Server'})
    source_url: str = field(metadata={'description': 'Path to the object on the BI Server'})
    bi_object_type: str = field(metadata={'description': 'The type of the object, as defined by the BI Server'})
    description_at_source: str = field(metadata={'description': 'Object description on the BI Server'})

@dataclass(kw_only=True)
class BIColumnObjectBase(BIObjectBase):
    """Common properties of a BI Column Object"""
    data_type: str = field(default=None, metadata={'description': 'The type of the column data.'})
    role: str = field(default=None, metadata={'description': 'The role of the column.'})
    expression: str = field(default=None, metadata={'description': 'The expression used to transform the data into a column'})
    values: list[str] = field(default_factory=list, metadata={'description': 'Sample values from the column'})

@dataclass(kw_only=True)
class BIReportColumn(BIColumnObjectBase):
    """Properties of a Report Column Object"""
    report: Optional[str] = field(default=None, metadata={'description': 'external_id of the parent report. Note that the report must exist on Alation to properly update this'})
    parent_datasource_columns: list[str] = field(default_factory=list, metadata={'description': 'external_id of the parent datasource columns. Note that the columns must exist on Alation to properly update this'})
    parent_report_columns: list[str] = field(default_factory=list, metadata={'description': 'external_id of the parent report columns. Note that the columns must exist on Alation, or occur earlier in the POST payload, to properly update this'})
    derived_report_columns: list[str] = field(default_factory=list, metadata={'description': 'external_id of all report columns derived from this one.'})

@dataclass(kw_only = True)
class BIReportsColumns:
    """A list of Connection report columns"""
    reports: list[BIReportColumn] = field(default_factory=list)

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
        payload = asdict(
            self,
            dict_factory=lambda values: {
                key: value for key, value in values
                if value is not None
            }
        )
        print(payload)

        return payload

@dataclass(kw_only = True)
class BIReportColumnParams (BIObjectBaseParams):
    pass