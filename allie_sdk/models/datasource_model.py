
"""Alation REST API Datasource Data Models."""

import dataclasses
from dataclasses import dataclass, field

from ..core.data_structures import BaseClass, BaseParams
from ..core.custom_exceptions import InvalidPostBody

# DATA MODELS FOR OCF DATA SOURCES

@dataclass(kw_only=True)
class _OCFDatasourceBase(BaseClass):
    uri: str = field(default=None)
    connector_id: int = field(default=None)
    db_username: str = field(default=None)
    title: str = field(default=None)
    description: str = field(default=None)
    private: bool = field(default=None)
    # is_hidden: bool = field(default=None) => not available in PATCH request


@dataclass(kw_only=True)
class OCFDatasource(_OCFDatasourceBase):

    is_hidden:bool = field(default=False)
    id:int = field(default=None)
    supports_explain:bool = field(default=None)
    data_upload_disabled_message:str = field(default=None)
    is_gone:bool = field(default=None)
    supports_qli_diagnostics:bool = field(default=None)
    latest_extraction_time:str = field(default=None)
    negative_filter_words:list[str] = field(default=None)
    can_data_upload:bool = field(default=None)
    qualified_name:str = field(default=None)
    all_schemas:str = field(default=None)
    has_previewable_qli:bool = field(default=None)
    supports_qli_daterange:bool = field(default=None)
    latest_extraction_successful:bool = field(default=None)
    owner_ids:list[int] = field(default=None)
    favorited_by_list:bool = field(default=None)
    supports_compose:bool = field(default=None)
    enable_designated_credential:bool = field(default=None)
    deleted:bool = field(default=None)
    limit_schemas:str = field(default=None)
    obfuscate_literals:list[str] = field(default=None)
    remove_filtered_schemas:bool = field(default=None)
    profiling_tip:str = field(default=None)
    supports_profiling:str = field(default=None)
    icon:str = field(default=None)
    url:str = field(default=None)
    otype:str = field(default=None)
    exclude_schemas:str = field(default=None)
    exclude_additional_columns_in_qli:bool = field(default=None)
    can_toggle_ds_privacy:bool = field(default=None)
    supports_md_diagnostics:bool = field(default=None)
    supports_ocf_query_service_api:bool = field(default=None)
    uses_ocf_agent:bool = field(default=None)
    nosql_mde_sample_size:int = field(default=None)
    disable_auto_extraction:bool = field(default=None)
    unresolved_mention_fingerprint_method:bool = field(default=None)
    enable_default_schema_extraction:bool = field(default=None)
    enabled_in_compose:bool = field(default=None)
    builtin_datasource:str = field(default=None)
    cron_extraction:str = field(default=None)
    supports_default_schema_extraction:bool = field(default=None)

    def __post_init__(self):
        # convert to proper timestamps
        if isinstance(self.latest_extraction_time, str):
            self.latest_extraction_time = self.convert_timestamp(self.latest_extraction_time)


@dataclass(kw_only=True)
class OCFDatasourcePostItem(_OCFDatasourceBase):
    """Payload used to create a new OCF datasource."""

    is_hidden: bool = field(default=False)
    db_password: str = field(default=None)

    _MANDATORY_FIELDS = {
        "connector_id"
        , "title"
        , "db_username"
        , "uri"
    }

    def generate_post_payload(self) -> dict:

        if self.connector_id is None:
            raise InvalidPostBody("'connector_id' is required for the Datasource POST payload.")
        if self.title is None:
            raise InvalidPostBody("'title' is required for the Datasource POST payload.")
        if self.db_username is None:
            raise InvalidPostBody("'db_username' is required for the Datasource POST payload.")
        if self.uri is None:
            raise InvalidPostBody("'uri' is required for the Datasource POST payload.")

        payload = dataclasses.asdict(
            self,
            dict_factory=lambda values: {
                key: value for key, value in values
                if value is not None
            }
        )

        return payload


@dataclass(kw_only=True)
class OCFDatasourcePutItem(_OCFDatasourceBase):
    """Payload used when updating an existing OCF datasource."""

    db_password: str = field(default=None)
    compose_default_uri: str = field(default=None)

    def generate_put_payload(self) -> dict:

        payload = dataclasses.asdict(
            self,
            dict_factory=lambda values: {
                key: value for key, value in values
                if value is not None
            }
        )

        return payload

@dataclass(kw_only=True)
class OCFDatasourceParams(BaseParams):
    include_hidden:bool = field(default=False)
    exclude_suspended:bool = field(default=False)


@dataclass(kw_only=True)
class OCFDatasourceGetParams(BaseParams):
    """Query parameters available when retrieving a datasource by id."""
    exclude_suspended:bool = field(default=False)

# ---------------------------------------------------------------------------#
# DATA MODELS FOR OLD NATIVE CONNECTORS AND RELATIONAL VIRTUAL DATA SOURCES
# ---------------------------------------------------------------------------#

@dataclass(kw_only=True)
class NativeDatasource(BaseClass):
    dbtype: str = field(default=None)
    host: str = field(default=None)
    port: int = field(default=None)
    uri: str = field(default=None)
    dbname: str = field(default=None)
    db_username: str = field(default=None)
    required: str = field(default=None)
    title: str = field(default=None)
    description: str = field(default=None)
    deployment_setup_complete: bool
    private: bool = field(default=None)
    is_virtual: bool = field(default=None)
    is_hidden: bool = field(default=None)
    id: int = field(default=None)
    supports_explain: bool = field(default=None)
    data_upload_disabled_message: str = field(default=None)
    hive_logs_source_type: int = field(default=None)
    metastore_uri: bool = field(default=None)
    is_hive: bool = field(default=None)
    is_gone: bool = field(default=None)
    webhdfs_server: str = field(default=None)
    supports_qli_diagnostics: bool = field(default=None)
    is_presto_hive: bool = field(default=None)
    latest_extraction_time: str = field(default=None)
    negative_filter_words: list[str] = field(default=None)
    has_hdfs_based_qli: bool = field(default=None)
    can_data_upload: bool = field(default=None)
    qualified_name: str = field(default=None)
    all_schemas: str = field(default=None)
    has_previewable_qli: bool = field(default=None)
    hive_tez_logs_source: str = field(default=None)
    has_metastore_uri: bool = field(default=None)
    webhdfs_port: int = field(default=None)
    supports_qli_daterange: bool = field(default=None)
    latest_extraction_successful: bool = field(default=None)
    owner_ids: list[int] = field(default=None)
    favorited_by_list: bool = field(default=None)
    supports_compose: bool = field(default=None)
    hive_logs_source: str = field(default=None)
    enable_designated_credential: bool = field(default=None)
    deleted: bool = field(default=None)
    limit_schemas: str = field(default=None)
    obfuscate_literals: list[str] = field(default=None)
    remove_filtered_schemas: bool = field(default=None)
    profiling_tip: str = field(default=None)
    supports_profiling: bool = field(default=None)
    webhdfs_username: str = field(default=None)
    icon: str = field(default=None)
    url: str = field(default=None)
    otype: str = field(default=None)
    exclude_schemas: str = field(default=None)
    qli_aws_region: str = field(default=None)
    has_aws_glue_metastore: bool = field(default=None)
    exclude_additional_columns_in_qli: bool = field(default=None)
    can_toggle_ds_privacy: bool = field(default=None)
    aws_region: str = field(default=None)
    aws_access_key_id: str = field(default=None)
    supports_md_diagnostics: bool = field(default=None)
    nosql_mde_sample_size: int = field(default=None)
    disable_auto_extraction: bool = field(default=None)
    metastore_type: str = field(default=None)
    unresolved_mention_fingerprint_method: str = field(default=None)
    qli_hive_connection_source: str = field(default=None)
    compose_oauth_enabled: bool = field(default=None)
    enable_default_schema_extraction: bool = field(default=None)
    enabled_in_compose: bool = field(default=None)
    builtin_datasource: str = field(default=None)
    has_aws_s3_based_qli: bool = field(default=None)
    qli_aws_access_key_id: str = field(default=None)
    jdbc_driver: str = field(default=None)
    cron_extraction: str = field(default=None)
    supports_default_schema_extraction: bool = field(default=None)

    def __post_init__(self):
        # convert to proper timestamps
        if isinstance(self.latest_extraction_time, str):
            self.latest_extraction_time = self.convert_timestamp(self.latest_extraction_time)
@dataclass(kw_only=True)
class NativeDatasourceParams(BaseParams):
    include_hidden:bool = field(default=False)
    include_undeployed:bool = field(default=False)
