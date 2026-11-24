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

## Token lifecycle

Each `Alation` instance owns one CDE token manager. Its CDM authentication client and
CDE method clients share that manager's in-memory cache. Constructing `Alation` does
not contact the CDE service; the first CDE request exchanges the configured Alation
access token, and later CDE requests reuse the result.

When a CDE request returns HTTP 401 or 403, the handler discards the cached token,
exchanges again, and retries the request once. The refreshed token is shared by all
CDE clients on that `Alation` instance. Exchange failures and failed retries raise
errors. Refresh is triggered by the service's rejection; the SDK does not run a
background refresh or schedule renewal based on token age.

An explicit call to `alation.cdm_authentication.create_cde_token()` always performs
a fresh exchange and updates the same cache. Passing `alation_token` equal to the
configured access token also updates it. Passing a different token returns that
identity's CDE token without replacing the configured credential or its cache.

Assigning a different `alation.access_token` immediately invalidates the shared CDE
cache; the next CDE call exchanges the replacement credential. Assigning the same
value preserves the cache. Assigning `None` or an empty string clears the cache and
prevents further CDE authentication until a credential is configured. With
`disable_authentication=True`, set `alation.access_token` before making a CDE call.

Tokens are kept in memory for the lifetime of the owning client. They are not saved
to disk or shared across `Alation` instances. Standalone CDM clients keep their own
isolated managers by default. Developers composing standalone clients can supply
the same `allie_sdk.core.cde_token_manager.CDETokenManager` through the optional
`token_manager` constructor argument. Such a manager must be used only for the same
Alation host and identity; if `access_token` is also supplied, it must match the
manager's configured credential.

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
This always performs an exchange. A result for the configured Alation credential
also replaces the shared CDE cache; a result for another credential is returned only
to the caller.

Args:
* alation_token (str, optional): Alation API token to exchange. Defaults to the access
  token currently configured for the `Alation` object's CDE clients. Use an Alation **access** token — while
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

## Examples

See `/examples/example_cdm_authentication.py` and
`/examples/example_cdm_critical_data_element.py`.
