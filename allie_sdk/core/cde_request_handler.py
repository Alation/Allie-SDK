"""Shared base handler for all Alation Critical Data Manager (CDM / CDE) API calls.

The CDE service authenticates differently from every other Alation API: instead of
the ``Token`` header injected by :class:`RequestHandler`, every CDE call must carry a
case-sensitive ``CDEToken`` header (and must NOT carry ``Token``). The CDE token is a
short-lived (24h) token obtained by exchanging an Alation API token at the CDE auth
endpoint.

This handler reuses :class:`RequestHandler`'s session/retry wiring and static loggers,
but performs its own HTTP calls so it can inject the ``CDEToken`` header. It also owns
the CDE token cache and the "re-exchange once on 401/403" behaviour, and provides a
CDE-specific job poller (the core :class:`~allie_sdk.methods.job.AlationJob` poller is
NOT reusable — CDE has its own job API).

See: https://developer.alation.com/dev/reference/cde-api-overview
"""

import json
import logging
import time
from time import sleep

import requests

from .request_handler import RequestHandler, SUCCESS_CODES

LOGGER = logging.getLogger("allie_sdk_logger")

# Base path shared by every CDE endpoint.
CDE_BASE = "/cde-service/integration"

# The CDE service caps the `limit` query parameter at 100 (unlike the core Alation API,
# whose default page size is 1000). Requesting more returns HTTP 422.
CDE_MAX_PAGE_SIZE = 100

# CDE job status vocabulary (distinct from the core Alation job API).
CDE_JOB_TERMINAL_STATUSES = ("FINISHED", "ERROR", "CANCELED")
CDE_JOB_ACTIVE_STATUSES = ("QUEUED", "IN_PROGRESS")

# Status codes that indicate the CDE token was rejected and should be re-exchanged.
CDE_REAUTH_STATUS_CODES = (401, 403)


class CDERequestHandler(RequestHandler):
    """Base class for all CDE (Critical Data Manager) method classes.

    Subclasses inherit CDE-flavoured request helpers (``_cde_get`` / ``_cde_post`` /
    ``_cde_put`` / ``_cde_delete``) and a CDE job poller (``_wait_for_cde_job``). The
    ``CDEToken`` header and token lifecycle are handled transparently: the CDE token is
    minted lazily on the first CDE call, cached, and re-exchanged once on a 401/403.
    """

    def __init__(self, access_token: str = None, session: requests.Session = None,
                 host: str = None):
        """Create an instance of the CDE request handler.

        Args:
            access_token (str, optional): Alation REST API Access Token, exchanged for a
                CDE token on first use.
            session (requests.Session): Python requests common session.
            host (str): Alation URL.

        """
        super().__init__(session=session, host=host, access_token=access_token)
        # Compose (rather than re-implement) the token-exchange mechanics, which are
        # already implemented and tested in AlationCDMAuthentication. Imported lazily to
        # avoid a circular import: this core module would otherwise pull in the whole
        # ``methods`` package while it is still being initialised.
        from ..methods.cdm_authentication import AlationCDMAuthentication

        self._cdm_auth = AlationCDMAuthentication(
            access_token=access_token, session=session, host=host
        )
        self._cde_token: str | None = None
        # CDE endpoints cap `limit` at 100 (the inherited RequestHandler.page_size of
        # 1000 is rejected with HTTP 422), so CDE pagination uses its own page size.
        self.cde_page_size = CDE_MAX_PAGE_SIZE

    # --- token lifecycle ---------------------------------------------------

    def _get_cde_token(self, force: bool = False) -> str:
        """Return the cached CDE token, minting one on first use (or when forced).

        Args:
            force (bool): If True, always exchange for a fresh CDE token.

        Returns:
            str: The CDE token to place in the ``CDEToken`` header.

        """
        if force or not self._cde_token:
            self._cde_token = self._cdm_auth.create_cde_token().token
        return self._cde_token

    def _cde_headers(self) -> dict:
        """Build the request headers for a CDE call.

        Returns:
            dict: Headers carrying the case-sensitive ``CDEToken`` (never ``Token``).

        """
        return {
            "Content-Type": "application/json; charset=utf-8",
            "CDEToken": self._get_cde_token(),
        }

    # --- core request with single re-auth retry ----------------------------

    def _cde_request(self, method: str, path: str, query_params: dict = None,
                     body: any = None, _reauth: bool = True) -> requests.Response:
        """Perform a single CDE HTTP request, injecting the ``CDEToken`` header.

        On a 401/403 the CDE token is re-exchanged exactly once and the request is
        retried. Any non-success status (including a second 401/403) raises.

        Args:
            method (str): HTTP method (GET/POST/PUT/DELETE).
            path (str): Request path (appended to the host).
            query_params (dict): Query string parameters.
            body (any): Request body (dict/list are JSON-encoded).
            _reauth (bool): Internal flag; when True a 401/403 triggers one re-exchange.

        Returns:
            requests.Response: The raw response (already status-checked).

        Raises:
            requests.HTTPError: If the CDE API returns a non-success status code.

        """
        request_url = self.host + path
        data = json.dumps(body, default=str) if isinstance(body, (dict, list)) else body

        api_response = self.s.request(
            method, request_url, params=query_params, data=data,
            headers=self._cde_headers(),
        )

        # The CDE token may have expired (24h TTL) — re-exchange once and retry.
        if api_response.status_code in CDE_REAUTH_STATUS_CODES and _reauth:
            LOGGER.debug(
                "CDE token rejected (%s); re-exchanging the CDE token and retrying once.",
                api_response.status_code,
            )
            self._get_cde_token(force=True)
            return self._cde_request(
                method, path, query_params=query_params, body=body, _reauth=False
            )

        log_url = self._format_log_url(api_response.url)
        log_details = {
            "Method": method,
            "URL": api_response.url,
            "Response": api_response.status_code,
        }

        if api_response.status_code not in SUCCESS_CODES:
            try:
                error_data = api_response.json()
            except requests.exceptions.JSONDecodeError:
                error_data = api_response.text
            self._log_error(
                error_data, log_details,
                message=f"Error submitting the CDE {method} Request to: {log_url}",
            )
            api_response.raise_for_status()

        self._log_success(
            log_details,
            message=f"Successfully submitted the CDE {method} Request to: {log_url}",
        )
        return api_response

    # --- verb wrappers ------------------------------------------------------

    def _cde_get(self, path: str, query_params: dict = None,
                 paginate: bool = True) -> list | dict:
        """Perform a CDE GET request, following skip/limit pagination.

        The CDE service paginates via ``skip``/``limit`` query parameters (it does not
        emit the ``X-Next-Page`` header the core Alation API uses). List responses may be
        a bare array or wrapped in ``items`` / ``results`` / ``data``.

        Args:
            path (str): Request path.
            query_params (dict): Query string parameters. A caller-supplied ``limit``
                sets the page size; ``skip`` sets the starting offset.
            paginate (bool): If True, fetch all pages; if False, return the single
                response body as-is.

        Returns:
            list | dict: The concatenated list of items (paginated) or the raw response
            body (non-paginated).

        """
        query_params = dict(query_params or {})

        if not paginate:
            return self._parse_response(self._cde_request("GET", path, query_params=query_params))

        requested_limit = int(query_params.pop("limit", self.cde_page_size))
        # The CDE service rejects limit > 100 with HTTP 422; cap it (pagination still
        # returns every matching item, just in smaller pages).
        limit = min(requested_limit, CDE_MAX_PAGE_SIZE)
        if requested_limit > CDE_MAX_PAGE_SIZE:
            LOGGER.debug(
                "Requested CDE page limit %s exceeds the service maximum %s; capping to %s.",
                requested_limit, CDE_MAX_PAGE_SIZE, CDE_MAX_PAGE_SIZE,
            )
        skip = int(query_params.pop("skip", 0))
        items: list = []

        while True:
            page_params = {**query_params, "skip": skip, "limit": limit}
            page = self._unwrap_list(
                self._parse_response(self._cde_request("GET", path, query_params=page_params))
            )
            items.extend(page)

            # A short (or empty) page means we have reached the last page.
            if len(page) < limit:
                break
            skip += limit

        return items

    def _cde_post(self, path: str, body: any = None, query_params: dict = None) -> dict | list:
        """Perform a CDE POST request.

        Args:
            path (str): Request path.
            body (any): Request body.
            query_params (dict): Query string parameters.

        Returns:
            dict | list: The parsed response body.

        """
        return self._parse_response(
            self._cde_request("POST", path, query_params=query_params, body=body)
        )

    def _cde_put(self, path: str, body: any = None, query_params: dict = None) -> dict | list:
        """Perform a CDE PUT request.

        Args:
            path (str): Request path.
            body (any): Request body.
            query_params (dict): Query string parameters.

        Returns:
            dict | list: The parsed response body.

        """
        return self._parse_response(
            self._cde_request("PUT", path, query_params=query_params, body=body)
        )

    def _cde_delete(self, path: str, body: any = None, query_params: dict = None) -> None:
        """Perform a CDE DELETE request (expects a 204 No Content response).

        Args:
            path (str): Request path.
            body (any): Request body.
            query_params (dict): Query string parameters.

        """
        self._cde_request("DELETE", path, query_params=query_params, body=body)

    # --- response robustness helpers ---------------------------------------

    @staticmethod
    def _parse_response(api_response: requests.Response) -> any:
        """Parse a CDE response body as JSON, falling back to decoded text.

        Args:
            api_response (requests.Response): The response to parse.

        Returns:
            any: Parsed JSON, or decoded text/bytes when the body is not JSON.

        """
        try:
            return api_response.json()
        except requests.exceptions.JSONDecodeError:
            try:
                return api_response.content.decode("utf-8")
            except UnicodeDecodeError:
                return api_response.content

    @staticmethod
    def _unwrap_list(payload: any) -> list:
        """Return the list of items from a CDE list response.

        Handles both a bare array and the common wrapper shapes
        (``items`` / ``results`` / ``data``).

        Args:
            payload (any): The parsed response body.

        Returns:
            list: The list of items (empty if none could be found).

        """
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            for key in ("items", "results", "data"):
                if isinstance(payload.get(key), list):
                    return payload[key]
        return []

    @staticmethod
    def _extract_job_key(payload: any) -> str | int | None:
        """Extract the async job identifier from a CDE write response.

        The identifier may be returned as a plain string or under any of
        ``job_key`` / ``key`` / ``id`` / ``job_id``.

        Args:
            payload (any): The parsed response body.

        Returns:
            str | int | None: The job key, or None if none could be found.

        """
        if isinstance(payload, str):
            return payload.strip() or None
        if isinstance(payload, dict):
            for key in ("job_key", "key", "id", "job_id"):
                if payload.get(key) is not None:
                    return payload[key]
        return None

    # --- CDE job poller (NOT the core AlationJob) --------------------------

    def _wait_for_cde_job(self, job_key: str | int, poll_interval: int = 3,
                          timeout: float = 300,
                          job_type: str = "API_BULK_CREATION") -> dict:
        """Poll the CDE job endpoint until the given job reaches a terminal state.

        The CDE job list endpoint has no key filter, so the uuid ``key`` is matched
        client-side (mirroring how the core :class:`AlationJob` poller blocks until
        completion, but against the CDE job API and its status vocabulary).

        Args:
            job_key (str | int): The job ``key`` returned by the write operation.
            poll_interval (int): Seconds to wait between polls.
            timeout (float): Maximum seconds to wait before raising. None disables it.
            job_type (str): CDE job ``type`` filter (e.g. ``API_BULK_CREATION``).

        Returns:
            dict: The terminal job record.

        Raises:
            TimeoutError: If the job does not reach a terminal state within ``timeout``.

        """
        start = time.monotonic()
        while True:
            jobs = self._cde_get(
                f"{CDE_BASE}/job/",
                query_params={"type": job_type, "order_by": "-ts_created"},
                paginate=True,
            )
            match = next(
                (job for job in jobs if str(job.get("key")) == str(job_key)), None
            )
            if match and str(match.get("status", "")).upper() in CDE_JOB_TERMINAL_STATUSES:
                LOGGER.debug("CDE job %s reached terminal status %s", job_key, match.get("status"))
                return match

            if timeout is not None and (time.monotonic() - start) > timeout:
                error_message = (
                    f"CDE job {job_key} did not reach a terminal state "
                    f"({', '.join(CDE_JOB_TERMINAL_STATUSES)}) within {timeout} seconds."
                )
                LOGGER.error(error_message)
                raise TimeoutError(error_message)

            sleep(poll_interval)
