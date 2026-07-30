"""Test the shared Alation Critical Data Manager (CDM / CDE) request handler."""
import pytest
import requests

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

    def test_no_circular_import(self):
        # Importing the core handler directly (before the methods package) must not
        # raise a circular ImportError.
        import importlib

        module = importlib.import_module("allie_sdk.core.cde_request_handler")
        assert hasattr(module, "CDERequestHandler")
