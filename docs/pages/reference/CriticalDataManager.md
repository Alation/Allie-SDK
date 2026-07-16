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

## Examples

See `/examples/example_cdm_authentication.py`.
