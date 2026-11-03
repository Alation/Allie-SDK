---
title: Alation AI Data Products
parent: SDK Reference
---


# Alation AI Data Products
{:.no_toc}

* TOC
{:toc}

The Data Product methods use the Alation AI API namespace at `/ai/api/v1/data_product/`.

All POST, PATCH, and PUT methods return `JobDetails`. Successful requests have
`status="successful"` and the method's typed response or payload in `result`.
For example, metric extraction returns its task ID at `job.result.task_id`.
This status describes the HTTP operation; use the task ID to check the asynchronous
workflow's progress.

## Models

### AlationAIDataProductTableColumnInfo

Python object used in `AlationAIGetUpstreamTablesFromBiObjectResponse`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| table_id | integer | Table identifier included in the data product. |
| column_ids | list[integer] | Column identifiers to include from the table. |

### AlationAIGenerateRelationshipsRequest

Python object used to generate JOIN relationships with `generate_relationships`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| spec_yaml | string | Required full data product spec as a YAML string. |

### AlationAIDataProductTask

Python object nested in `JobDetails.result` when a metrics workflow starts.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| task_id | string | Identifier of the queued AI task. |

### AlationAIGeneratedRelationship

Single generated relationship returned inside `AlationAIGenerateRelationshipsResponse`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| name | string | Generated relationship name. |
| left_table | string | Name of the left-side record set. |
| right_table | string | Name of the right-side record set. |
| expression | string | Generated JOIN expression. |
| sql_dialect | string | SQL dialect used for the expression. |
| cardinality | string | Optional inferred relationship cardinality. |
| left_nullable | bool | Whether the left-side join key can be null. |
| right_nullable | bool | Whether the right-side join key can be null. |
| notes | string | Optional notes describing the generated relationship. |

### AlationAIGenerateRelationshipsResponse

Python object nested in `JobDetails.result` by `generate_relationships`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| relationships | list[`AlationAIGeneratedRelationship`] | Generated relationships inferred from the supplied YAML spec. |

### AlationAIAsyncTask

Python object returned when a queued AI task is still running.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| id | string | Task identifier. |
| name | string | Task name. |
| status | string | Task status such as `pending`, `running`, or `failed`. |
| parameters | dict | Parameters submitted with the task. |
| context | dict | Additional task execution metadata. |
| tenant_id | string | Tenant identifier. |
| user_id | string | User identifier. |

### AlationAIReviseDataProductRequest

Python object used to start a revise workflow with `initiate_revise_data_product_workflow`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| message | string | Optional instruction sent to the reviser. The SDK defaults to the API's built-in revision prompt. |

### AlationAIReviseDataProductResponse

Python object nested in `JobDetails.result` when a revise workflow starts.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| result_id | string | Result identifier used to monitor the revise workflow. |
| chat_id | string | Chat identifier used by the revise workflow. |

### AlationAIReviseDataProductJobsParams

Optional query parameters used with `get_data_product_revision_jobs`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| status | list[string] | Optional list of run statuses to include. |
| data_product_id | string | Optional data product identifier filter. |
| sql_eval_v2_result_id | string | Optional SQL evaluation result identifier filter. |
| limit | integer | Maximum number of results to return. |
| offset | integer | Number of results to skip. |

### AlationAIReviseDataProductResultSummary

Summary object returned inside `AlationAIReviseDataProductResultsPage`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| result_id | string | Result identifier. |
| chat_id | string | Chat identifier. |
| data_product_id | string | Associated data product identifier. |
| status | string | Workflow status. |
| created_at | datetime | Workflow start timestamp. |
| updated_at | datetime | Latest update timestamp. |

### AlationAIReviseDataProductResultsPage

Paginated page returned by `get_data_product_revision_jobs`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| data | list[`AlationAIReviseDataProductResultSummary`] | Result page entries. |
| total | integer | Total number of matching results. |

### AlationAIReviseDataProductResultDetail

Detailed object returned by `get_data_product_revision_result`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| result_id | string | Result identifier. |
| chat_id | string | Chat identifier. |
| data_product_id | string | Associated data product identifier. |
| status | string | Workflow status. |
| created_at | datetime | Workflow start timestamp. |
| updated_at | datetime | Latest update timestamp. |
| message | string | Revision instruction. |
| summary | string | Summary of the changes made by the reviser. |
| initial_data_product_yaml | string | Initial data product YAML. |
| final_data_product_yaml | string | Final data product YAML. |

### AlationAISqlWithValidation

Python object returned in the list at `JobDetails.result` by `validate_sql`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| sql | string | Submitted SQL statement. |
| status | bool | Validation result when available. |
| error | list[string] | Validation errors, if any. |

### AlationAIMetricWithErrors

Nested metric object returned by `get_data_product_metrics_extraction_result`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| displayName | string | Metric display name. |
| description | string | Metric description. |
| expression | string | SQL metric expression. |
| columns | list[string] | Referenced columns. |
| errors | list[string] | Metric-specific extraction errors, if any. |
| type | string | Metric return type. |

### AlationAISqlMetricResult

Python object returned by `get_data_product_metrics_extraction_result` when extraction has completed.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| sql | string | Submitted SQL statement. |
| status | bool | Extraction success indicator. |
| error | list[string] | Top-level extraction errors, if any. |
| metrics | list[`AlationAIMetricWithErrors`] | Extracted metrics for the SQL statement. |

### AlationAIMetricSource

Nested source metadata returned by `get_data_product_metrics_extraction_result_with_source`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| source_type | string | BI source type such as `tableau` or `looker`. |
| source_name | string | BI source display name. |
| original_expression | string | Original expression from the BI asset. |
| extracted_at | datetime | Extraction timestamp. |
| source_url | string | External BI URL, when present. |
| catalog_url | string | Related Alation catalog URL, when present. |

### AlationAIMetricWithSource

Nested metric object returned by `get_data_product_metrics_extraction_result_with_source`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| displayName | string | Metric display name. |
| description | string | Metric description. |
| expression | string | SQL metric expression. |
| columns | list[string] | Referenced columns. |
| errors | list[string] | Metric-specific extraction errors, if any. |
| type | string | Metric return type. |
| confidenceLevel | string | Confidence label for the extracted metric. |
| confidenceExplanation | string | Optional explanation for the confidence value. |
| sources | list[`AlationAIMetricSource`] | BI sources that contributed the metric. |

### AlationAIMetricResultWithSource

Python object returned by `get_data_product_metrics_extraction_result_with_source` when extraction has completed.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| status | bool | Extraction success indicator. |
| error | list[string] | Top-level extraction errors, if any. |
| metrics | list[`AlationAIMetricWithSource`] | Extracted metrics with BI source metadata. |

### AlationAIExtractMetricsFromBIParams

Optional query parameters used with `extract_data_product_metrics_from_bi`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| dashboard_ids | list[integer] | Optional dashboard identifiers to restrict extraction. |
| lookml_model_folder_ids | list[integer] | Optional LookML model folder identifiers to restrict extraction. |

### AlationAIGetUpstreamTablesFromBiObjectParams

Required query parameters used with `get_upstream_tables_from_bi_object`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| type | string | BI object type. Supported values are `dashboard` and `lookml_folder`. |
| id | integer | BI object identifier. |

### AlationAIDatasourceTables

Nested datasource grouping returned inside `AlationAIGetUpstreamTablesFromBiObjectResponse`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| datasource_id | integer | Datasource identifier. |
| tables | list[`AlationAIDataProductTableColumnInfo`] | Upstream tables and column identifiers. |

### AlationAIGetUpstreamTablesFromBiObjectResponse

Python object returned by `get_upstream_tables_from_bi_object`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| datasources | list[`AlationAIDatasourceTables`] | Upstream tables grouped by datasource. |

## Methods

### get_data_product_creation_result

```
get_data_product_creation_result(
    self,
    task_id: str,
    poll_interval_seconds: float = 3,
    timeout_seconds: float | None = 300
) -> str
```

Poll a data product task every few seconds until the final YAML is returned.

Notes:
* While the backend reports a non-terminal status such as `pending` or `running`, the SDK waits
  `poll_interval_seconds` before polling again, capped to the remaining timeout.
* Polling raises `TimeoutError` after 300 seconds by default. Set `timeout_seconds` to a
  positive, finite value to change this deadline, or `None` to disable it. The deadline
  is checked between HTTP requests and does not interrupt an in-flight request.
* The task ID must be a non-empty string containing more than whitespace. The poll
  interval must be finite and greater than or equal to zero.
* If the backend reports `status="failed"`, the SDK raises `requests.exceptions.HTTPError`.
* This polls the `/ai/api/v1/data_product/get_data_product_result/{task_id}` endpoint.

### generate_relationships

```
generate_relationships(
    self,
    generate_relationships_request: AlationAIGenerateRelationshipsRequest
) -> JobDetails
```

Generate JOIN relationships between record sets in a data product specification.
The result contains an `AlationAIGenerateRelationshipsResponse`; access generated
relationships at `job.result.relationships`. Empty responses produce an empty
response model in `result`.

Notes:
* Pass the full YAML string in `data_product_spec_yaml`, typically the output returned by `get_data_product_creation_result`.
* This wraps the `/ai/api/v1/data_product/generate_relationships` endpoint.

### initiate_revise_data_product_workflow

```
initiate_revise_data_product_workflow(
    self,
    data_product_id: str,
    revise_request: AlationAIReviseDataProductRequest = None
) -> JobDetails
```

Start a revise data product workflow.
The result contains an `AlationAIReviseDataProductResponse` with `result_id` and
`chat_id`.

### get_data_product_revision_jobs

```
get_data_product_revision_jobs(
    self,
    query_params: AlationAIReviseDataProductJobsParams = None
) -> AlationAIReviseDataProductResultsPage
```

Browse revise data product jobs.

### get_data_product_revision_result

```
get_data_product_revision_result(
    self,
    result_id: str
) -> AlationAIReviseDataProductResultDetail
```

Fetch a single revise data product result.

### validate_sql

```
validate_sql(
    self,
    data_product_id: str,
    sql_statements: list[str]
) -> JobDetails
```

Validate one or more SQL statements against a data product.
`sql_statements` must be a non-empty list of strings; a bare string or another
container raises `UnsupportedPostBody` before an HTTP request is sent.
The result contains a list of `AlationAISqlWithValidation` objects, or an empty
list when the API response is empty.

### extract_metrics_from_sql_statements

```
extract_metrics_from_sql_statements(
    self,
    data_product_id: str,
    sql_statements: list[str]
) -> JobDetails
```

Start metric extraction from one or more SQL statements.
`sql_statements` must be a non-empty list of strings; a bare string or another
container raises `UnsupportedPostBody` before an HTTP request is sent.
The result contains an `AlationAIDataProductTask`; access its ID at `job.result.task_id`.

### extract_data_product_metrics_from_sample_queries

```
extract_data_product_metrics_from_sample_queries(
    self,
    data_product_id: str
) -> JobDetails
```

Start metric extraction from the sample queries stored on a data product.
The result contains an `AlationAIDataProductTask`; access its ID at `job.result.task_id`.

### extract_data_product_metrics_from_bi

```
extract_data_product_metrics_from_bi(
    self,
    data_product_id: str,
    query_params: AlationAIExtractMetricsFromBIParams = None
) -> JobDetails
```

Start metric extraction from downstream BI assets.
The result contains an `AlationAIDataProductTask`; access its ID at `job.result.task_id`.

### get_data_product_metrics_extraction_result

```
get_data_product_metrics_extraction_result(self, task_id: str) -> AlationAIAsyncTask | list[AlationAISqlMetricResult]
```

Fetch the current task status or completed SQL metric extraction results.

### get_data_product_metrics_extraction_result_with_source

```
get_data_product_metrics_extraction_result_with_source(self, task_id: str) -> AlationAIAsyncTask | list[AlationAIMetricResultWithSource]
```

Fetch the current task status or completed metric extraction results with source metadata.

### get_upstream_tables_from_bi_object

```
get_upstream_tables_from_bi_object(
    self,
    query_params: AlationAIGetUpstreamTablesFromBiObjectParams
) -> AlationAIGetUpstreamTablesFromBiObjectResponse
```

Resolve upstream tables for a BI dashboard or LookML model folder.

### create_data_product_from_bi_source

```
create_data_product_from_bi_source(
    self,
    datasource_id: int,
    create_product: bool = True
) -> JobDetails
```

Create a data product from a BI datasource, or return a preview spec when `create_product=False`.
The result contains the API payload, including the YAML string for a specification preview.

## Examples

See `/examples/example_alation_ai_data_product.py`.
