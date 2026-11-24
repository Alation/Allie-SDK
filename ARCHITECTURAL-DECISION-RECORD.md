# Architectural decision records

## ADR-001: Share CDE token management within each Alation instance

**Status:** Accepted  
**Date:** 2026-11-24

### Context

The Critical Data Manager (CDM / CDE) APIs require a separate CDE token obtained by
exchanging an Alation credential. CDE method clients send this token in the
`CDEToken` header and can recover from an authentication rejection by exchanging
again and retrying once.

Previously, every `CDERequestHandler` owned its own token cache and authentication
helper. Additional CDE method clients would consequently exchange and refresh
credentials independently. The public `alation.cdm_authentication` client was also
separate: calling `create_cde_token()` did not populate the cache used by CDE method
calls. Replacing `Alation.access_token` did not reach those existing clients.

We need one credential lifecycle per Alation client, while preserving lazy CDE
authentication, standalone method clients, the existing exchange API, and the
bounded retry behavior. Ordinary SDK initialization must remain usable without
access to the CDE service.

### Decision

`Alation` creates one `CDETokenManager` after its normal authentication flow and
injects it into its CDM authentication and CDE method clients. The manager owns the
current Alation credential and one cached CDE token. There is no global cache and
no disk persistence. The manager belongs to one Alation instance and host.

| Component | Responsibility |
| --- | --- |
| `Alation` | Create and share the manager; propagate parent access-token assignments into it. |
| `CDETokenManager` | Own the credential and cache, obtain a token lazily through an exchange callable, and invalidate or replace cached credentials. |
| `AlationCDMAuthentication` | Implement the HTTP exchange, parse and validate its response, and cache successful results for the configured identity. |
| `CDERequestHandler` | Obtain credentials from the manager, inject the CDE header, and refresh and retry once on HTTP 401/403. Retain CDE pagination and job polling. |

The manager accepts an exchange callable when a token is requested. It does not
import the methods package or implement endpoint-specific HTTP behavior. Existing
CDE handlers can retain an authentication helper for the exchange; those helpers
share the injected manager rather than holding independent credential caches.

#### Lifecycle

1. Construction initializes an empty cache and performs no CDE requests. The first
   CDE call exchanges the configured Alation credential. Later calls across CDE
   clients using that manager reuse the result.
2. `create_cde_token()` continues to perform a fresh HTTP exchange on every call and
   return a `CDEToken` model. A result for the configured Alation credential updates
   the shared cache, including when that credential is passed explicitly.
3. An explicit exchange for another credential returns its token without changing
   the configured identity or shared cache. This prevents per-call overrides from
   changing the identity used by subsequent CDE method calls.
4. A 401/403 response causes the handler to discard the cached token, request a fresh
   exchange through the manager, and retry once. The refreshed token is immediately
   available to other consumers of that manager. A failed exchange or retry raises;
   an exchange failure does not restore the rejected token. Other HTTP failures do
   not trigger a credential refresh.
5. Assigning a different `Alation.access_token` invalidates the CDE cache immediately.
   CDE consumers read their Alation credential from the manager, so existing clients
   use the replacement on their next exchange. Assigning the same value retains the
   cache. Clearing the credential with `None` or an empty string also discards the
   cache and prevents further CDE requests until credentials are supplied again.
6. A directly constructed CDM authentication client or CDE method client creates an
   isolated manager by default. The optional `token_manager` argument allows composed
   standalone clients to share one manager for the same host and identity. A
   conflicting constructor `access_token` raises `ValueError`. Direct assignments
   to a CDE consumer's `access_token` update its shared manager as well.

Renewal remains reactive to HTTP 401/403. This decision introduces no background
refresh, expiry timer, automatic renewal of the parent Alation access token, or
cross-process persistence. `disable_authentication=True` still skips initial
authentication; callers can subsequently set `Alation.access_token` before using
CDE methods. Credential handling for other API families is outside this decision.

### Alternatives considered

* **Keep a cache per CDE handler:** Simple for the current single CDE method client,
  but duplicates exchanges as additional clients are introduced and leaves explicit
  token creation disconnected from automatic authentication.
* **Move the complete exchange and retry implementation into `Alation`:** Centralizes
  state but mixes endpoint behavior into the facade and makes standalone clients
  depend on it. Composition keeps each responsibility in its existing layer.
* **Generate a CDE token during `Alation` construction:** Adds an unnecessary request
  and makes ordinary SDK initialization depend on CDE availability and permissions.
* **Use a global or disk cache:** Adds credential isolation, storage, and lifetime
  concerns that are unnecessary for sharing within a client instance.

### Consequences

* CDE clients under one `Alation` instance reuse credentials and observe refreshes
  and parent credential changes consistently.
* Existing exchange and method-call signatures remain compatible; the new manager
  parameter is optional. Explicit creation for the configured identity now has the
  intentional side effect of populating the cache used by automatic CDE calls.
* Separate Alation instances and default standalone clients stay isolated, even
  when they use identical credentials. Callers injecting a manager must scope it to
  one host and identity.
* Cached credentials live only as long as the owning object graph. Sharing a manager
  does not introduce a thread-safety guarantee for clients or their requests session.
* New CDE method clients must accept and forward the injected manager. They must not
  add another token cache or place the CDE token in shared session defaults.

### Verification

Mocked HTTP tests cover lazy construction across authentication modes, token reuse
across consumers, explicit exchanges, identity overrides, parent and direct consumer
credential replacement, clearing and restoring credentials, per-instance isolation,
shared 401/403 recovery, failed refresh recovery, and rejection of conflicting
constructor credentials. Existing CDE tests continue to cover bounded retries,
header isolation, pagination, response handling, and CDE job polling.

### Related files

* [Alation facade](alation.py)
* [CDE token manager](core/cde_token_manager.py)
* [CDE request handler](core/cde_request_handler.py)
* [CDM authentication](methods/cdm_authentication.py)
* [CDE reference documentation](../docs/pages/reference/CriticalDataManager.md)
