---
title: Critical Data Manager
parent: SDK Reference
---

# Critical Data Manager (CDM / CDE)
{:.no_toc}

* TOC
{:toc}

## Overview

The Critical Data Manager (CDM), served by the `cde-service`, uses a dedicated
authentication flow that differs from every other Alation API. Instead of passing an
Alation API token directly, you first exchange your Alation API token (refresh or access
token) for a short-lived **CDE token**. That CDE token is then passed in the `CDEToken`
request header for all subsequent CDE API calls.

Key points:

* The token exchange endpoint is `POST /cde-service/integration/auth/`.
* The Alation API token is passed in the `token` request header (not `Token`, not `Authorization`).
* The endpoint returns the CDE token as a plain string.
* The CDE token is valid for 24 hours. When it expires, exchange again for a new one.

See the Alation Developer Portal [CDE API Overview](https://developer.alation.com/dev/reference/cde-api-overview) for details.

## Models

### CDEToken
Represents a CDE token returned by exchanging an Alation API token. Returned by the
function `create_cde_token`.

Attributes:

| Name  | Type | Description                                                                                                        |
|-------|------|-------------------------------------------------------------------------------------------------------------------|
| token | str  | The plain-string CDE token, passed in the `CDEToken` header for all CDE API calls. Valid for 24 hours from creation. |

### CriticalDataElement
Represents a Critical Data Element returned by the CDE API. Returned by
`get_critical_data_elements` and `get_critical_data_element`.

Attributes:

| Name               | Type     | Description                                                                 |
|--------------------|----------|-----------------------------------------------------------------------------|
| id                 | int      | The Critical Data Element ID.                                               |
| key                | str      | The Critical Data Element key (uuid).                                       |
| id_no              | int      | Human-facing sequential number.                                            |
| name               | str      | The Critical Data Element name.                                            |
| description        | str      | The Critical Data Element description.                                     |
| version            | int      | Version number.                                                            |
| status             | str      | Lifecycle status (e.g. `CANDIDATE`, `DRAFT`, `CERTIFIED`).                  |
| cde_risk_level     | str      | Risk level label (list responses; e.g. `Low`/`Medium`/`High`).             |
| risk_level         | dict     | Risk object `{value, label, number_of_levels}` (get responses).            |
| risk_rationale     | str      | Rationale for the risk assessment.                                         |
| risk_confidence    | float    | Confidence of the risk assessment.                                         |
| domains            | list     | Associated domains, as raw object-reference dicts `{id, name, source_key}`. |
| stewards           | list     | Stewards, as raw object-reference dicts.                                   |
| owners             | list     | Owners, as raw object-reference dicts.                                     |
| sources            | list     | Sources, as raw object-reference dicts.                                    |
| approvers          | list     | Approvers, as raw object-reference dicts.                                  |
| contributors       | list     | Contributors, as raw object-reference dicts.                               |
| fields             | list     | Applied overlay-standard data (nested), as raw passthrough.                |
| data_assets_counts | dict     | PDE-relationship counts, e.g. `{all, control_points, related, suggested}`.  |
| quality_score      | float    | Data-quality score (nullable).                                             |
| curation_score     | float    | Curation score (nullable).                                                 |
| job_id             | int      | ID of the async job that created/updated the element.                      |
| ts_created         | datetime | Creation timestamp.                                                        |
| ts_updated         | datetime | Last-updated timestamp.                                                    |
| ts_deleted         | datetime | Deletion timestamp (soft delete).                                          |
| created_by         | dict     | Creating user, as a raw object-reference dict.                             |
| updated_by         | dict     | Last-updating user, as a raw object-reference dict.                        |
| deleted_by         | dict     | Deleting user, as a raw object-reference dict.                             |
| deleted            | bool     | Whether the element is soft-deleted.                                       |

The relationship/ownership arrays and audit objects are exposed as raw `list`/`dict`
values from the API payload (not typed sub-models); typed modelling of those workflows is
deferred. Each object-reference dict is shaped like
`{"id": <int>, "name": <str>, "source_key": "alation://<type>/<id>"}` (e.g.
`alation://user/123`, `alation://domain/10`).

### CriticalDataElementItem
The create/update payload for a Critical Data Element (used by
`create_critical_data_element`, `create_critical_data_elements_bulk`, and
`update_critical_data_element`). Only set fields are sent.

| Name             | Type | Description                                                                        |
|------------------|------|------------------------------------------------------------------------------------|
| name             | str  | The element name (required for create).                                            |
| description      | str  | The element description.                                                           |
| status           | str  | Creation status (`CANDIDATE`/`DRAFT`); ignored on update.                           |
| risk_level_value | int  | Risk level value.                                                                  |
| risk_level_label | str  | Risk level label.                                                                  |
| risk_rationale   | str  | Rationale for the risk assessment.                                                 |
| domains          | list | Domain object-references (raw), `source_key` as `alation://<type>/<id>`.            |
| stewards         | list | Steward object-references (raw).                                                   |
| owners           | list | Owner object-references (raw).                                                     |
| sources          | list | Source object-references (raw).                                                    |
| approvers        | list | Approver object-references (raw).                                                  |
| contributors     | list | Contributor object-references (raw).                                               |
| fields           | list | Applied overlay-standard data (nested, raw).                                       |
| pdes             | list | Physical-data-element mappings (nested, raw). Create only — omitted on update.      |

### CriticalDataElementParams
Filter parameters for `get_critical_data_elements`. Repeatable filters are sets,
serialized as repeated query parameters. Pagination (`skip`/`limit`) is handled by the
SDK and is not a parameter here.

| Name                  | Type | Description                                                              |
|-----------------------|------|--------------------------------------------------------------------------|
| search                | str  | Free-text search filter.                                                 |
| status                | set  | Filter by one or more lifecycle statuses.                                |
| risk_level            | set  | Filter by one or more integer risk-level codes (e.g. `1`, `2`).          |
| owner_key             | set  | Filter by owner key(s) (e.g. `alation://user/123`).                      |
| domain_keys           | set  | Filter by domain key(s) (serialized as `domain_keys[]`).                 |
| steward_key           | set  | Filter by steward key(s).                                                |
| version               | set  | Filter by one or more version numbers.                                   |
| key                   | set  | Filter by one or more Critical Data Element keys (uuid).                 |
| job_id                | int  | Filter by the async job that produced the element.                       |
| latest_only           | bool | Only the latest version of each element.                                 |
| latest_certified_only | bool | Only the latest certified version of each element.                       |
| order_by              | str  | Sort order (e.g. `status`, `-ts_created`).                               |

### CDEJob
Represents a Critical Data Manager background job (used for asynchronous operations such
as bulk-create). Returned by `get_cde_jobs`, `get_cde_job`, and `wait_for_cde_job`.

Attributes:

| Name       | Type          | Description                                                     |
|------------|---------------|-----------------------------------------------------------------|
| id         | int           | The job ID.                                                     |
| key        | str           | The job key (uuid) used to correlate an async write to its job. |
| type       | str           | The job type (e.g. `API_BULK_CREATION`).                        |
| status     | str           | `QUEUED`, `IN_PROGRESS`, `FINISHED`, `ERROR`, or `CANCELED`.    |
| result     | dict \| list  | Per-item outcomes / errors.                                     |
| ts_created | datetime      | Creation timestamp.                                             |
| ts_updated | datetime      | Last-updated timestamp.                                         |

Convenience properties: `is_terminal` (job reached `FINISHED`/`ERROR`/`CANCELED`) and
`is_successful` (job reached `FINISHED`).

### CDEJobParams
Filter parameters for `get_cde_jobs`.

| Name     | Type | Description                                     |
|----------|------|-------------------------------------------------|
| type     | str  | Filter by job type (e.g. `API_BULK_CREATION`).  |
| status   | str  | Filter by job status.                           |
| order_by | str  | Sort order (e.g. `-ts_created`).                |

## Methods

The CDM authentication methods are available on the `Alation` object under
`alation.cdm_authentication`.

### create_cde_token

```
create_cde_token(alation_token: str = None) -> CDEToken
```

Exchange an Alation API token for a CDE token. Calls
`POST /cde-service/integration/auth/`, passing the Alation API token in the `token`
request header, and returns the resulting CDE token (valid for 24 hours from creation).

Args:
* alation_token (str, optional): Alation API token to exchange. Defaults to the access
  token the `Alation` object authenticated with. Use an Alation **access** token — while
  the CDE docs mention refresh or access tokens, some `cde-service` deployments reject
  refresh tokens with `403 Access denied: Invalid Alation API token`.

Returns:
* `CDEToken`

Raises:
* `ValueError`: If no Alation API token is available to exchange.
* `requests.HTTPError`: If the CDE auth endpoint returns a non-success status code.

### Critical Data Element methods

The Critical Data Element methods are available on the `Alation` object under
`alation.cdm_critical_data_element`. The CDE token is obtained transparently on the
first call (minted from the Alation access token and re-exchanged automatically when it
expires), so no explicit token handling is required.

#### get_critical_data_elements

```
get_critical_data_elements(query_params: CriticalDataElementParams = None) -> list[CriticalDataElement]
```

Get (filter) Critical Data Elements. Calls `GET /cde-service/integration/cde/`, following
the service's `skip`/`limit` pagination to return all matching elements.

Args:
* query_params (CriticalDataElementParams, optional): REST API GET filter values.

Returns:
* `list[CriticalDataElement]`

Raises:
* `requests.HTTPError`: If the CDE API returns a non-success status code.

#### get_critical_data_element

```
get_critical_data_element(cde_id: int) -> CriticalDataElement
```

Get a single Critical Data Element by ID. Calls `GET /cde-service/integration/cde/{id}/`.

Args:
* cde_id (int): The Critical Data Element ID.

Returns:
* `CriticalDataElement`

Raises:
* `requests.HTTPError`: If the CDE API returns a non-success status code.

#### create_critical_data_element

```
create_critical_data_element(critical_data_element: CriticalDataElementItem) -> CriticalDataElement
```

Create a single Critical Data Element. Calls `POST /cde-service/integration/cde/`.

Args:
* critical_data_element (CriticalDataElementItem): The element to create (`name` is
  required; `status` should be a creation status such as `CANDIDATE` or `DRAFT`).
  Optional risk / relationship / overlay-standard `fields` / `pdes` are passed through if set.
* allow_duplicates (bool): Whether the server may create a name-duplicate element.

Returns:
* `CriticalDataElement`

Raises:
* `InvalidPostBody`: If required fields are missing.
* `UnsupportedPostBody`: If the payload is not a `CriticalDataElementItem`.
* `requests.HTTPError`: If the CDE API returns a non-success status code.

#### create_critical_data_elements_bulk

```
create_critical_data_elements_bulk(critical_data_elements: list[CriticalDataElementItem], allow_duplicates: bool = False, wait_for_completion: bool = True, poll_interval: int = 3, timeout: float = 300) -> CDEJob | str
```

Create up to 1000 Critical Data Elements in a single asynchronous request. Calls
`POST /cde-service/integration/cde/bulk/`, which returns a job `key`. By default the SDK
blocks until the job reaches a terminal state and returns the resulting `CDEJob`; pass
`wait_for_completion=False` to return the job `key` immediately instead.

Args:
* critical_data_elements (list[CriticalDataElementItem]): The elements to create (max 1000).
* allow_duplicates (bool): Whether the server may create name-duplicate elements.
* wait_for_completion (bool): Block for the job and return a `CDEJob` (default), or return the key.
* poll_interval (int): Seconds between polls while waiting.
* timeout (float): Maximum seconds to wait before raising `TimeoutError`. `None` disables it.

Returns:
* `CDEJob` (when waiting) or `str` (the job key).

Raises:
* `ValueError`: If more than 1000 elements are supplied, or no job key is returned.
* `UnsupportedPostBody`: If the payload contains non-`CriticalDataElementItem` items.
* `TimeoutError`: If the job does not complete within `timeout` (when waiting).
* `requests.HTTPError`: If the CDE API returns a non-success status code.

#### update_critical_data_element

```
update_critical_data_element(cde_id: int, critical_data_element: CriticalDataElementItem) -> CriticalDataElement
```

Update an existing Critical Data Element. Calls `PUT /cde-service/integration/cde/{id}/`
(synchronous) and returns the updated element. `status` is **not** an update field (use
the status-transition endpoint for that) and is ignored even if set on the item.

Args:
* cde_id (int): The Critical Data Element ID to update.
* critical_data_element (CriticalDataElementItem): The fields to change (`name` / `description`).

Returns:
* `CriticalDataElement`

Raises:
* `UnsupportedPostBody`: If the payload is not a `CriticalDataElementItem`.
* `requests.HTTPError`: If the CDE API returns a non-success status code.

#### delete_critical_data_element

```
delete_critical_data_element(cde_id: int) -> None
```

Delete a single Critical Data Element by ID. Calls `DELETE /cde-service/integration/cde/{id}/`.

Args:
* cde_id (int): The Critical Data Element ID.

Raises:
* `requests.HTTPError`: If the CDE API returns a non-success status code.

#### delete_critical_data_elements_bulk

```
delete_critical_data_elements_bulk(cde_ids: list[int]) -> None
```

Delete multiple Critical Data Elements by ID in a single synchronous request. Calls
`POST /cde-service/integration/cde/bulk_delete/` with a body of `{"ids": [...]}`.

Args:
* cde_ids (list[int]): The IDs of the Critical Data Elements to delete.

Raises:
* `ValueError`: If `cde_ids` is empty.
* `requests.HTTPError`: If the CDE API returns a non-success status code.

### Job methods

The Critical Data Manager job methods are available on the `Alation` object under
`alation.cdm_job`. CDE jobs track asynchronous operations and have their own status
vocabulary (distinct from the core Alation background-job API).

#### get_cde_jobs

```
get_cde_jobs(query_params: CDEJobParams = None) -> list[CDEJob]
```

Get (filter) CDE jobs. Calls `GET /cde-service/integration/job/`, following the service's
`skip`/`limit` pagination.

Args:
* query_params (CDEJobParams, optional): REST API GET filter values.

Returns:
* `list[CDEJob]`

Raises:
* `requests.HTTPError`: If the CDE API returns a non-success status code.

#### get_cde_job

```
get_cde_job(job_id: int) -> CDEJob
```

Get a single CDE job by its integer ID. Calls `GET /cde-service/integration/job/{id}/`.
Note this takes the integer `id`, not the uuid `key` returned by async writes — use
`wait_for_cde_job` to wait on a write by its key.

Args:
* job_id (int): The CDE job ID.

Returns:
* `CDEJob`

Raises:
* `requests.HTTPError`: If the CDE API returns a non-success status code.

#### cancel_cde_job

```
cancel_cde_job(job_id: int) -> None
```

Cancel a CDE job by its integer ID. Calls `POST /cde-service/integration/job/{id}/cancel/`.

Args:
* job_id (int): The CDE job ID.

Raises:
* `requests.HTTPError`: If the CDE API returns a non-success status code.

#### wait_for_cde_job

```
wait_for_cde_job(job_key: str | int, poll_interval: int = 3, timeout: float = 300, job_type: str = "API_BULK_CREATION") -> CDEJob
```

Block until the CDE job with the given uuid `key` reaches a terminal state
(`FINISHED`/`ERROR`/`CANCELED`). Polls `GET /cde-service/integration/job/` and matches the
`key` client-side (the list endpoint has no key filter).

Args:
* job_key (str | int): The job `key` returned by an asynchronous write.
* poll_interval (int): Seconds between polls.
* timeout (float): Maximum seconds to wait before raising `TimeoutError`. `None` disables it.
* job_type (str): CDE job `type` filter.

Returns:
* `CDEJob`

Raises:
* `TimeoutError`: If the job does not reach a terminal state within `timeout`.
* `requests.HTTPError`: If the CDE API returns a non-success status code.

## Examples

See `/examples/example_cdm_authentication.py`,
`/examples/example_cdm_critical_data_element.py`, and
`/examples/example_cdm_job.py`.
