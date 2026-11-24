"""Test the shared Alation Critical Data Manager (CDM / CDE) request handler."""
import logging
from unittest.mock import patch

import pytest
import requests
from requests_mock import Mocker

from allie_sdk.core.cde_request_handler import CDERequestHandler, CDE_BASE


CDE_TOKEN_STRING = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.cde_payload.cde_signature"
CDE_TOKEN_REFRESHED = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.refreshed.signature"


class TestCDERequestHandler:

    def setup_method(self):
        self.handler = CDERequestHandler(
            access_token="alation-access-token",
            session=requests.session(),
            host="https://test.com",
        )

    # --- token lifecycle + header routing --------------------------------

    def test_cde_get_sends_cdetoken_header_never_token(self, requests_mock):
        requests_mock.register_uri(
            "POST", "/cde-service/integration/auth/", text=CDE_TOKEN_STRING
        )
        requests_mock.register_uri(
            "GET", f"{CDE_BASE}/cde/", json=[]
        )

        self.handler._cde_get(f"{CDE_BASE}/cde/")

        # The last request is the data GET (not the auth POST).
        last = requests_mock.last_request
        assert last.headers.get("CDEToken") == CDE_TOKEN_STRING
        # The core "Token" header must never be sent on a CDE call.
        assert last.headers.get("Token") is None

    def test_cde_token_minted_lazily_once_and_cached(self, requests_mock):
        auth = requests_mock.register_uri(
            "POST", "/cde-service/integration/auth/", text=CDE_TOKEN_STRING
        )
        requests_mock.register_uri("GET", f"{CDE_BASE}/cde/", json=[])
        requests_mock.register_uri("GET", f"{CDE_BASE}/standard/", json=[])

        # No token exchanged until the first CDE call.
        assert auth.call_count == 0

        self.handler._cde_get(f"{CDE_BASE}/cde/")
        self.handler._cde_get(f"{CDE_BASE}/standard/")

        # Two data calls, but the token was minted (exchanged) exactly once.
        assert auth.call_count == 1

    def test_alation_token_changes_invalidate_cached_cde_credentials(self, requests_mock: Mocker) -> None:
        """Exchange fresh CDE credentials after replacing the underlying Alation token.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Asserts the new token is exchanged once and cached without credential mixing.
        """
        authentication = requests_mock.post(
            f"{self.handler.host}{CDE_BASE}/auth/",
            [{"text": CDE_TOKEN_STRING}, {"text": CDE_TOKEN_REFRESHED}],
        )
        requests_mock.get(f"{self.handler.host}{CDE_BASE}/cde/", json=[])
        self.handler._cde_get(f"{CDE_BASE}/cde/")

        self.handler.access_token = "replacement-alation-token"
        self.handler._cde_get(f"{CDE_BASE}/cde/")
        self.handler.access_token = "replacement-alation-token"
        self.handler._cde_get(f"{CDE_BASE}/cde/")

        assert authentication.call_count == 2
        exchange_requests = [
            request for request in requests_mock.request_history if request.url.endswith("/auth/")
        ]
        assert [request.headers["token"] for request in exchange_requests] == [
            "alation-access-token", "replacement-alation-token"
        ]
        assert requests_mock.last_request.headers["CDEToken"] == CDE_TOKEN_REFRESHED
        assert "Token" not in requests_mock.last_request.headers
        assert "Authorization" not in requests_mock.last_request.headers

    @pytest.mark.parametrize("cleared_token", [None, ""])
    def test_cleared_alation_token_cannot_reuse_cached_cde_credentials(
        self, requests_mock: Mocker, cleared_token: str | None
    ) -> None:
        """Discard cached CDE credentials when the Alation access token is removed.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            cleared_token (str | None): Empty value used to clear authentication.

        Returns:
            None: Asserts clearing credentials prevents another authenticated CDE request.
        """
        authentication = requests_mock.post(f"{self.handler.host}{CDE_BASE}/auth/", text=CDE_TOKEN_STRING)
        data_request = requests_mock.get(f"{self.handler.host}{CDE_BASE}/cde/", json=[])
        self.handler._cde_get(f"{CDE_BASE}/cde/")

        self.handler.access_token = cleared_token
        with pytest.raises(ValueError, match="No Alation API token available"):
            self.handler._cde_get(f"{CDE_BASE}/cde/")

        assert authentication.call_count == 1
        assert data_request.call_count == 1
        assert self.handler.access_token == cleared_token

    def test_401_triggers_single_reexchange_then_succeeds(self, requests_mock):
        requests_mock.register_uri(
            "POST",
            "/cde-service/integration/auth/",
            [{"text": CDE_TOKEN_STRING}, {"text": CDE_TOKEN_REFRESHED}],
        )
        # First data call 401s (stale token), retry after re-exchange succeeds.
        cde = requests_mock.register_uri(
            "GET",
            f"{CDE_BASE}/cde/",
            [{"status_code": 401, "json": {"detail": "expired"}}, {"json": [], "status_code": 200}],
        )

        result = self.handler._cde_get(f"{CDE_BASE}/cde/")

        assert result == []
        assert cde.call_count == 2
        # Second (retry) request carries the refreshed token.
        assert requests_mock.last_request.headers.get("CDEToken") == CDE_TOKEN_REFRESHED

    def test_second_401_propagates_as_httperror(self, requests_mock):
        requests_mock.register_uri(
            "POST", "/cde-service/integration/auth/", text=CDE_TOKEN_STRING
        )
        requests_mock.register_uri(
            "GET", f"{CDE_BASE}/cde/", status_code=401, json={"detail": "denied"}
        )

        with pytest.raises(requests.exceptions.HTTPError) as context:
            self.handler._cde_get(f"{CDE_BASE}/cde/")

        assert context.value.response.status_code == 401

    def test_403_triggers_reexchange(self, requests_mock):
        requests_mock.register_uri(
            "POST",
            "/cde-service/integration/auth/",
            [{"text": CDE_TOKEN_STRING}, {"text": CDE_TOKEN_REFRESHED}],
        )
        cde = requests_mock.register_uri(
            "GET",
            f"{CDE_BASE}/cde/",
            [{"status_code": 403, "json": {"detail": "denied"}}, {"json": [], "status_code": 200}],
        )

        self.handler._cde_get(f"{CDE_BASE}/cde/")

        assert cde.call_count == 2

    # --- pagination -------------------------------------------------------

    def test_cde_get_paginates_skip_limit(self, requests_mock):
        requests_mock.register_uri(
            "POST", "/cde-service/integration/auth/", text=CDE_TOKEN_STRING
        )
        # Force a small page size to exercise paging.
        self.handler.cde_page_size = 2
        full_page = [{"id": 1}, {"id": 2}]
        short_page = [{"id": 3}]

        def _responder(request, context):
            context.status_code = 200
            skip = int(request.qs.get("skip", ["0"])[0])
            return full_page if skip == 0 else short_page

        requests_mock.register_uri("GET", f"{CDE_BASE}/cde/", json=_responder)

        result = self.handler._cde_get(f"{CDE_BASE}/cde/")

        assert result == [{"id": 1}, {"id": 2}, {"id": 3}]

    def test_cde_get_caps_limit_at_service_maximum(self, requests_mock):
        requests_mock.register_uri(
            "POST", "/cde-service/integration/auth/", text=CDE_TOKEN_STRING
        )
        requests_mock.register_uri("GET", f"{CDE_BASE}/cde/", json=[])

        # Ask for more than the CDE service allows; it must be capped to 100.
        self.handler._cde_get(f"{CDE_BASE}/cde/", query_params={"limit": 1000})

        assert requests_mock.last_request.qs.get("limit") == ["100"]

    def test_cde_get_no_pagination_returns_raw(self, requests_mock):
        requests_mock.register_uri(
            "POST", "/cde-service/integration/auth/", text=CDE_TOKEN_STRING
        )
        requests_mock.register_uri(
            "GET", f"{CDE_BASE}/cde/1/", json={"id": 1, "name": "x"}
        )

        result = self.handler._cde_get(f"{CDE_BASE}/cde/1/", paginate=False)

        assert result == {"id": 1, "name": "x"}

    # --- response robustness helpers -------------------------------------

    def test_unwrap_list_bare_array(self):
        assert self.handler._unwrap_list([{"id": 1}]) == [{"id": 1}]

    def test_unwrap_list_wrapped_shapes(self):
        assert self.handler._unwrap_list({"items": [{"id": 1}]}) == [{"id": 1}]
        assert self.handler._unwrap_list({"results": [{"id": 2}]}) == [{"id": 2}]
        assert self.handler._unwrap_list({"data": [{"id": 3}]}) == [{"id": 3}]

    def test_unwrap_list_unknown_shape_returns_empty(self):
        assert self.handler._unwrap_list({"unexpected": {"id": 1}}) == []
        assert self.handler._unwrap_list(None) == []

    def test_extract_job_key_shapes(self):
        assert self.handler._extract_job_key("plain-key") == "plain-key"
        assert self.handler._extract_job_key({"job_key": "a"}) == "a"
        assert self.handler._extract_job_key({"key": "b"}) == "b"
        assert self.handler._extract_job_key({"id": 7}) == 7
        assert self.handler._extract_job_key({"job_id": 8}) == 8
        assert self.handler._extract_job_key({"nothing": 1}) is None
        assert self.handler._extract_job_key("") is None

    # --- import safety ----------------------------------------------------

    @pytest.mark.parametrize("method", ["GET", "POST", "PUT", "DELETE"])
    @pytest.mark.parametrize("rejected_status", [401, 403])
    def test_reauthentication_replays_request(
        self, requests_mock: Mocker, caplog: pytest.LogCaptureFixture, method: str, rejected_status: int
    ) -> None:
        """Replay a rejected CDE request once with its body, filters and fresh credentials.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            caplog (pytest.LogCaptureFixture): Captured log records.
            method (str): HTTP verb to exercise.
            rejected_status (int): Authentication rejection that triggers token refresh.

        Returns:
            None: Asserts request replay, isolated credentials and no premature error log.
        """
        caplog.set_level(logging.DEBUG, logger="allie_sdk_logger")
        authentication = requests_mock.post(
            f"{self.handler.host}{CDE_BASE}/auth/",
            [{"text": CDE_TOKEN_STRING}, {"text": CDE_TOKEN_REFRESHED}],
        )
        data_url = f"{self.handler.host}{CDE_BASE}/cde/"
        requests_mock.register_uri(
            method, data_url,
            [{"status_code": rejected_status, "json": {"detail": "expired"}}, {"json": {"job_key": "example"}}],
        )
        original_defaults = self.handler.headers.copy()
        body = {"name": "Example +&="}
        query_params = {"status": "CERTIFIED"}

        response = self.handler._cde_request(method, f"{CDE_BASE}/cde/", query_params=query_params, body=body)

        assert response.json() == {"job_key": "example"}
        assert authentication.call_count == 2
        data_requests = [request for request in requests_mock.request_history if request.url.split("?")[0] == data_url]
        assert len(data_requests) == 2
        for outgoing_request, expected_token in zip(data_requests, [CDE_TOKEN_STRING, CDE_TOKEN_REFRESHED]):
            assert outgoing_request.json() == body
            assert outgoing_request.qs == {"status": ["certified"]}
            assert outgoing_request.headers["CDEToken"] == expected_token
            assert "Token" not in outgoing_request.headers
            assert "Authorization" not in outgoing_request.headers
        assert query_params == {"status": "CERTIFIED"}
        assert self.handler.headers == original_defaults
        assert not [record for record in caplog.records if record.levelno >= logging.ERROR]

    @pytest.mark.parametrize("rejected_status", [401, 403])
    def test_reauthentication_is_bounded(
        self, requests_mock: Mocker, caplog: pytest.LogCaptureFixture, rejected_status: int
    ) -> None:
        """Raise and log only the final CDE authentication failure after one retry.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            caplog (pytest.LogCaptureFixture): Captured log records.
            rejected_status (int): Repeated authentication rejection.

        Returns:
            None: Asserts two exchanges and data requests, and one final error log.
        """
        caplog.set_level(logging.ERROR, logger="allie_sdk_logger")
        authentication = requests_mock.post(f"{self.handler.host}{CDE_BASE}/auth/", text=CDE_TOKEN_STRING)
        data_request = requests_mock.get(
            f"{self.handler.host}{CDE_BASE}/cde/", status_code=rejected_status, text="denied"
        )

        with pytest.raises(requests.HTTPError) as exception:
            self.handler._cde_get(f"{CDE_BASE}/cde/")

        assert exception.value.response.status_code == rejected_status
        assert authentication.call_count == 2
        assert data_request.call_count == 2
        assert len([record for record in caplog.records if record.levelno >= logging.ERROR]) == 1

    @pytest.mark.parametrize("status_code", [400, 500])
    def test_non_authentication_failure_does_not_refresh(self, requests_mock: Mocker, status_code: int) -> None:
        """Propagate ordinary CDE HTTP errors without refreshing credentials.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            status_code (int): Non-authentication error returned by the endpoint.

        Returns:
            None: Asserts the request fails without an extra token exchange.
        """
        authentication = requests_mock.post(f"{self.handler.host}{CDE_BASE}/auth/", text=CDE_TOKEN_STRING)
        data_request = requests_mock.get(f"{self.handler.host}{CDE_BASE}/cde/", status_code=status_code, text="failed")

        with pytest.raises(requests.HTTPError) as exception:
            self.handler._cde_get(f"{CDE_BASE}/cde/")

        assert exception.value.response.status_code == status_code
        assert authentication.call_count == 1
        assert data_request.call_count == 1

    @pytest.mark.parametrize(
        ("method_name", "response_body", "status_code", "expected"),
        [
            pytest.param("_cde_post", b'{"job_key": "example"}', 202, {"job_key": "example"}, id="post-object"),
            pytest.param("_cde_post", b"example", 202, "example", id="post-text"),
            pytest.param("_cde_put", b'"example"', 202, "example", id="put-json-string"),
            pytest.param("_cde_put", b'[1, 2]', 200, [1, 2], id="put-list"),
            pytest.param("_cde_put", b"\xff\x00", 200, b"\xff\x00", id="put-binary"),
            pytest.param("_cde_put", b"", 204, "", id="put-empty"),
            pytest.param("_cde_delete", b"", 204, None, id="delete-empty"),
            pytest.param("_cde_delete", b'{"deleted": true}', 200, None, id="delete-discard-body"),
        ],
    )
    def test_write_return_values(
        self, requests_mock: Mocker, method_name: str, response_body: bytes, status_code: int, expected: object
    ) -> None:
        """Preserve the CDE write wrappers' decoded payloads and DELETE's None result.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            method_name (str): CDE write helper.
            response_body (bytes): Raw server response.
            status_code (int): Successful response status.
            expected (object): Expected helper return value.

        Returns:
            None: Asserts return values, serialized bodies and isolated authentication.
        """
        requests_mock.post(f"{self.handler.host}{CDE_BASE}/auth/", text=CDE_TOKEN_STRING)
        requests_mock.register_uri(
            method_name.removeprefix("_cde_").upper(), f"{self.handler.host}{CDE_BASE}/cde/",
            content=response_body, status_code=status_code,
        )

        result = getattr(self.handler, method_name)(f"{CDE_BASE}/cde/", body=[{"id": 1}])

        assert result == expected
        assert requests_mock.last_request.json() == [{"id": 1}]
        assert requests_mock.last_request.headers["CDEToken"] == CDE_TOKEN_STRING
        assert "Token" not in requests_mock.last_request.headers
        assert "Authorization" not in requests_mock.last_request.headers

    @pytest.mark.parametrize("envelope", ["items", "results", "data"])
    def test_pagination_preserves_offsets_filters_and_refresh(self, requests_mock: Mocker, envelope: str) -> None:
        """Keep CDE paging state when a later wrapped page requires reauthentication.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            envelope (str): Response field wrapping the list of items.

        Returns:
            None: Asserts all pages, original query parameters and refreshed headers.
        """
        authentication = requests_mock.post(
            f"{self.handler.host}{CDE_BASE}/auth/",
            [{"text": CDE_TOKEN_STRING}, {"text": CDE_TOKEN_REFRESHED}],
        )
        requests_mock.get(
            f"{self.handler.host}{CDE_BASE}/cde/?skip=2&limit=2&status=CERTIFIED",
            json={envelope: [{"id": 3}, {"id": 4}]}, complete_qs=True,
        )
        later_page = requests_mock.get(
            f"{self.handler.host}{CDE_BASE}/cde/?skip=4&limit=2&status=CERTIFIED",
            [{"status_code": 401}, {"json": {envelope: [{"id": 5}]}}], complete_qs=True,
        )
        query_params = {"skip": 2, "limit": 2, "status": "CERTIFIED"}

        result = self.handler._cde_get(f"{CDE_BASE}/cde/", query_params=query_params)

        assert result == [{"id": 3}, {"id": 4}, {"id": 5}]
        assert query_params == {"skip": 2, "limit": 2, "status": "CERTIFIED"}
        assert later_page.call_count == 2
        assert authentication.call_count == 2
        assert requests_mock.last_request.headers["CDEToken"] == CDE_TOKEN_REFRESHED

    @pytest.mark.parametrize("terminal_status", ["FINISHED", "ERROR", "CANCELED"])
    def test_cde_job_terminal_results(self, requests_mock: Mocker, terminal_status: str) -> None:
        """Preserve CDE job polling and return each terminal record unchanged.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            terminal_status (str): CDE terminal status to exercise.

        Returns:
            None: Asserts matching by job key and the terminal job return value.
        """
        requests_mock.post(f"{self.handler.host}{CDE_BASE}/auth/", text=CDE_TOKEN_STRING)
        terminal_job = {"key": "wanted", "status": terminal_status}
        job_request = requests_mock.get(
            f"{self.handler.host}{CDE_BASE}/job/",
            [
                {"json": {"items": [{"key": "other", "status": "FINISHED"}, {"key": "wanted", "status": "IN_PROGRESS"}]}},
                {"json": {"items": [terminal_job]}},
            ],
        )

        result = self.handler._wait_for_cde_job("wanted", poll_interval=0)

        assert result == terminal_job
        assert job_request.call_count == 2
        assert requests_mock.last_request.qs["type"] == ["api_bulk_creation"]

    def test_cde_job_timeout(self, requests_mock: Mocker) -> None:
        """Retain the timeout when a CDE job never appears in the service's list.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Asserts the poller raises its original timeout exception.
        """
        requests_mock.post(f"{self.handler.host}{CDE_BASE}/auth/", text=CDE_TOKEN_STRING)
        requests_mock.get(f"{self.handler.host}{CDE_BASE}/job/", json=[])

        with patch("allie_sdk.core.cde_request_handler.time.monotonic", side_effect=[0.0, 301.0]):
            with pytest.raises(TimeoutError, match="wanted"):
                self.handler._wait_for_cde_job("wanted", poll_interval=0, timeout=300)

    def test_refresh_exchange_failure_propagates(self, requests_mock: Mocker) -> None:
        """Stop replaying a data request when refreshing the CDE token itself fails.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Asserts the exchange error propagates without another data request.
        """
        authentication = requests_mock.post(
            f"{self.handler.host}{CDE_BASE}/auth/",
            [{"text": CDE_TOKEN_STRING}, {"status_code": 401, "text": "exchange denied"}],
        )
        data_request = requests_mock.get(f"{self.handler.host}{CDE_BASE}/cde/", status_code=403)

        with pytest.raises(requests.HTTPError) as exception:
            self.handler._cde_get(f"{CDE_BASE}/cde/")

        assert exception.value.response.status_code == 401
        assert exception.value.response.url.endswith("/auth/")
        assert authentication.call_count == 2
        assert data_request.call_count == 1

    def test_no_circular_import(self):
        # Importing the core handler directly (before the methods package) must not
        # raise a circular ImportError.
        import importlib

        module = importlib.import_module("allie_sdk.core.cde_request_handler")
        assert hasattr(module, "CDERequestHandler")
