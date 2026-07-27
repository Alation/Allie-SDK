"""Alation AI API Data Product Models."""

from dataclasses import dataclass, field
from datetime import datetime

from ..core.custom_exceptions import InvalidPostBody, validate_rest_payload
from ..core.data_structures import BaseClass, BaseParams


DEFAULT_ALATION_AI_REVISE_DATA_PRODUCT_MESSAGE = (
    "Maximize accuracy by making generic improvements to the data product which will fix the "
    "existing failures, and still apply to new, unseen questions. You can modify the data "
    "product a maximum of 3 times. Stop after getting a final evaluation result to demonstrate "
    "the improvements on the final data product."
)


@dataclass(kw_only=True)
class AlationAIDataProductTableColumnInfo(BaseClass):
    """Table and column identifiers used to build a data product."""

    table_id: int = field(default=None)
    column_ids: list[int] = field(default_factory=list)

    def generate_api_payload(self) -> dict:
        """Generate the API payload for a table and its columns."""

        if self.table_id is None:
            raise InvalidPostBody("'table_id' is a required field for Data Product payload bodies")
        if not self.column_ids:
            raise InvalidPostBody("'column_ids' is a required field for Data Product payload bodies")

        return {
            "table_id": self.table_id,
            "column_ids": self.column_ids,
        }


@dataclass(kw_only=True)
class AlationAIDataProductCreationInfo(BaseClass):
    """Payload used to create a data product."""

    table_column_info_list: list[AlationAIDataProductTableColumnInfo] = field(default_factory=list)
    existing_data_product: str = field(default=None)

    def generate_api_post_payload(self) -> dict:
        """Generate the API payload for creating a data product."""

        if not self.table_column_info_list:
            raise InvalidPostBody(
                "'table_column_info_list' is a required field for Data Product POST payload bodies"
            )

        validate_rest_payload(self.table_column_info_list, (AlationAIDataProductTableColumnInfo,))

        payload = {
            "table_column_info_list": [
                item.generate_api_payload() for item in self.table_column_info_list
            ]
        }

        if self.existing_data_product is not None:
            payload["existing_data_product"] = self.existing_data_product

        return payload


@dataclass(kw_only=True)
class AlationAIDataProductTask(BaseClass):
    """Task identifier returned for asynchronous data product workflows."""

    task_id: str = field(default=None)


@dataclass(kw_only=True)
class AlationAIDataProductToUpdate(BaseClass):
    """Payload used to update an existing data product description."""

    existing_data_product: str = field(default=None)

    def generate_api_put_payload(self) -> dict:
        """Generate the API payload for updating a data product description."""

        if self.existing_data_product is None:
            raise InvalidPostBody(
                "'existing_data_product' is a required field for Data Product PUT payload bodies"
            )

        return {"existing_data_product": self.existing_data_product}


@dataclass(kw_only=True)
class AlationAIAsyncTask(BaseClass):
    """Queued task metadata returned while an AI workflow is still running."""

    name: str = field(default=None)
    parameters: dict = field(default_factory=dict)
    id: str = field(default=None)
    tenant_id: str = field(default=None)
    user_id: str = field(default=None)
    context: dict = field(default_factory=dict)
    status: str = field(default=None)


@dataclass(kw_only=True)
class AlationAIReviseDataProductRequest(BaseClass):
    """Payload used to initiate a revise data product workflow."""

    message: str = field(default=DEFAULT_ALATION_AI_REVISE_DATA_PRODUCT_MESSAGE)

    def generate_api_post_payload(self) -> dict:
        """Generate the API payload for revising a data product."""

        if self.message is None:
            return {}

        return {"message": self.message}


@dataclass(kw_only=True)
class AlationAIReviseDataProductResponse(BaseClass):
    """Response returned when a revise data product workflow starts."""

    result_id: str = field(default=None)
    chat_id: str = field(default=None)


@dataclass(kw_only=True)
class AlationAIReviseDataProductJobsParams(BaseParams):
    """Optional filters for revise data product jobs."""

    status: list[str] = field(default=None)
    data_product_id: str = field(default=None)
    sql_eval_v2_result_id: str = field(default=None)
    limit: int = field(default=None)
    offset: int = field(default=None)

    def generate_params_dict(self) -> dict:
        """Generate query parameters for revise job browsing."""

        params = {}

        if self.status:
            params["status"] = self.status
        if self.data_product_id is not None:
            params["data_product_id"] = self.data_product_id
        if self.sql_eval_v2_result_id is not None:
            params["sql_eval_v2_result_id"] = self.sql_eval_v2_result_id
        if self.limit is not None:
            params["limit"] = self.limit
        if self.offset is not None:
            params["offset"] = self.offset

        return params


@dataclass(kw_only=True)
class AlationAIReviseDataProductResultSummary(BaseClass):
    """Summary details for a revise data product run."""

    result_id: str = field(default=None)
    chat_id: str = field(default=None)
    data_product_id: str = field(default=None)
    status: str = field(default=None)
    created_at: datetime | None = field(default=None)
    updated_at: datetime | None = field(default=None)

    def __post_init__(self):
        if isinstance(self.created_at, str):
            self.created_at = self.convert_timestamp(self.created_at)
        if isinstance(self.updated_at, str):
            self.updated_at = self.convert_timestamp(self.updated_at)


@dataclass(kw_only=True)
class AlationAIReviseDataProductResultsPage(BaseClass):
    """Paginated revise data product job response."""

    data: list[AlationAIReviseDataProductResultSummary] = field(default_factory=list)
    total: int = field(default=0)

    def __post_init__(self):
        if isinstance(self.data, list) and self.data:
            if not isinstance(self.data[0], AlationAIReviseDataProductResultSummary):
                self.data = [
                    AlationAIReviseDataProductResultSummary.from_api_response(item)
                    for item in self.data
                ]


@dataclass(kw_only=True)
class AlationAIReviseDataProductResultDetail(BaseClass):
    """Detailed details for a revise data product run."""

    result_id: str = field(default=None)
    chat_id: str = field(default=None)
    data_product_id: str = field(default=None)
    status: str = field(default=None)
    created_at: datetime | None = field(default=None)
    updated_at: datetime | None = field(default=None)
    message: str = field(default=None)
    summary: str = field(default=None)
    initial_data_product_yaml: str = field(default=None)
    final_data_product_yaml: str = field(default=None)

    def __post_init__(self):
        if isinstance(self.created_at, str):
            self.created_at = self.convert_timestamp(self.created_at)
        if isinstance(self.updated_at, str):
            self.updated_at = self.convert_timestamp(self.updated_at)


@dataclass(kw_only=True)
class AlationAISqlWithValidation(BaseClass):
    """SQL validation result."""

    sql: str = field(default=None)
    status: bool | None = field(default=None)
    error: list[str] = field(default=None)


@dataclass(kw_only=True)
class AlationAIMetricSource(BaseClass):
    """Source metadata associated with an extracted metric."""

    source_type: str = field(default=None)
    source_name: str = field(default=None)
    original_expression: str = field(default=None)
    extracted_at: datetime | None = field(default=None)
    source_url: str = field(default=None)
    catalog_url: str = field(default=None)

    def __post_init__(self):
        if isinstance(self.extracted_at, str):
            self.extracted_at = self.convert_timestamp(self.extracted_at)


@dataclass(kw_only=True)
class AlationAIMetricWithErrors(BaseClass):
    """Metric payload returned from SQL-based extraction."""

    displayName: str = field(default=None)
    description: str = field(default=None)
    expression: str = field(default=None)
    columns: list[str] = field(default=None)
    errors: list[str] = field(default=None)
    type: str = field(default=None)


@dataclass(kw_only=True)
class AlationAIMetricWithSource(BaseClass):
    """Metric payload enriched with source metadata."""

    displayName: str = field(default=None)
    description: str = field(default=None)
    expression: str = field(default=None)
    columns: list[str] = field(default=None)
    errors: list[str] = field(default=None)
    type: str = field(default=None)
    confidenceLevel: str = field(default=None)
    confidenceExplanation: str = field(default=None)
    sources: list[AlationAIMetricSource] = field(default=None)

    def __post_init__(self):
        if isinstance(self.sources, list) and self.sources:
            if not isinstance(self.sources[0], AlationAIMetricSource):
                self.sources = [AlationAIMetricSource.from_api_response(item) for item in self.sources]


@dataclass(kw_only=True)
class AlationAISqlMetricResult(BaseClass):
    """Metric extraction result for a single SQL statement."""

    sql: str = field(default=None)
    status: bool = field(default=None)
    error: list[str] = field(default=None)
    metrics: list[AlationAIMetricWithErrors] = field(default=None)

    def __post_init__(self):
        if isinstance(self.metrics, list) and self.metrics:
            if not isinstance(self.metrics[0], AlationAIMetricWithErrors):
                self.metrics = [AlationAIMetricWithErrors.from_api_response(item) for item in self.metrics]


@dataclass(kw_only=True)
class AlationAIMetricResultWithSource(BaseClass):
    """Metric extraction result that includes source metadata."""

    status: bool = field(default=None)
    error: list[str] = field(default=None)
    metrics: list[AlationAIMetricWithSource] = field(default=None)

    def __post_init__(self):
        if isinstance(self.metrics, list) and self.metrics:
            if not isinstance(self.metrics[0], AlationAIMetricWithSource):
                self.metrics = [AlationAIMetricWithSource.from_api_response(item) for item in self.metrics]


@dataclass(kw_only=True)
class AlationAIExtractMetricsFromBIParams(BaseParams):
    """Optional filters for extracting metrics from BI sources."""

    dashboard_ids: list[int] = field(default=None)
    lookml_model_folder_ids: list[int] = field(default=None)

    def generate_params_dict(self) -> dict:
        """Generate query parameters for BI-based metrics extraction."""

        params = {}

        if self.dashboard_ids:
            params["dashboard_ids"] = self.dashboard_ids
        if self.lookml_model_folder_ids:
            params["lookml_model_folder_ids"] = self.lookml_model_folder_ids

        return params


@dataclass(kw_only=True)
class AlationAIGetTablesFromBIParams(BaseParams):
    """Required query parameters for resolving upstream tables from BI."""

    type: str = field(default=None)
    id: int = field(default=None)

    def generate_params_dict(self) -> dict:
        """Generate query parameters for BI table discovery."""

        if self.type is None:
            raise InvalidPostBody("'type' is a required field for Get Tables From BI query params")
        if self.id is None:
            raise InvalidPostBody("'id' is a required field for Get Tables From BI query params")

        return {
            "type": self.type,
            "id": self.id,
        }


@dataclass(kw_only=True)
class AlationAIDatasourceTables(BaseClass):
    """Tables grouped by datasource."""

    datasource_id: int = field(default=None)
    tables: list[AlationAIDataProductTableColumnInfo] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.tables, list) and self.tables:
            if not isinstance(self.tables[0], AlationAIDataProductTableColumnInfo):
                self.tables = [AlationAIDataProductTableColumnInfo.from_api_response(item) for item in self.tables]


@dataclass(kw_only=True)
class AlationAIUpstreamTablesResponse(BaseClass):
    """Upstream BI tables grouped by datasource."""

    datasources: list[AlationAIDatasourceTables] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.datasources, list) and self.datasources:
            if not isinstance(self.datasources[0], AlationAIDatasourceTables):
                self.datasources = [
                    AlationAIDatasourceTables.from_api_response(item) for item in self.datasources
                ]
