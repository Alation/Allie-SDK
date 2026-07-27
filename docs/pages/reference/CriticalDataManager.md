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

| Name        | Type     | Description                                              |
|-------------|----------|----------------------------------------------------------|
| id          | int      | The Critical Data Element ID.                            |
| key         | str      | The Critical Data Element key (uuid).                    |
| name        | str      | The Critical Data Element name.                          |
| description | str      | The Critical Data Element description.                   |
| status      | str      | Lifecycle status (e.g. `CANDIDATE`, `DRAFT`, `CERTIFIED`). |
| job_id      | int      | ID of the async job that created/updated the element.   |
| ts_created  | datetime | Creation timestamp.                                      |
| ts_updated  | datetime | Last-updated timestamp.                                  |

### CriticalDataElementParams
Filter parameters for `get_critical_data_elements`.

| Name     | Type | Description                                        |
|----------|------|----------------------------------------------------|
| search   | str  | Free-text search filter.                           |
| status   | str  | Filter by lifecycle status.                        |
| key      | str  | Filter by Critical Data Element key (uuid).        |
| job_id   | int  | Filter by the async job that produced the element. |
| order_by | str  | Sort order (e.g. `-ts_created`).                   |

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
