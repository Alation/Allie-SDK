"""Test the Alation Critical Data Manager (CDM / CDE) API Authentication Methods."""
import pytest
import requests
from requests_mock import Mocker

from allie_sdk.methods.cdm_authentication import *


CDE_TOKEN_STRING = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test_payload.test_signature"


class TestCDMAuthentication:

    def setup_method(self):
        self.cdm_auth = AlationCDMAuthentication(
            access_token="alation-access-token",
            session=requests.session(),
            host="https://test.com",
        )

    def test_success_create_cde_token_plain_string(self, requests_mock):
        requests_mock.register_uri(
            "POST", "/cde-service/integration/auth/", text=CDE_TOKEN_STRING
        )

        cde_token = self.cdm_auth.create_cde_token()

        assert cde_token.token == CDE_TOKEN_STRING

    def test_success_create_cde_token_json_quoted_string(self, requests_mock):
        # Some deployments JSON-encode the plain string (i.e. wrap it in quotes).
        requests_mock.register_uri(
            "POST", "/cde-service/integration/auth/", json=CDE_TOKEN_STRING
        )

        cde_token = self.cdm_auth.create_cde_token()

        assert cde_token.token == CDE_TOKEN_STRING

    def test_success_create_cde_token_sends_lowercase_token_header(self, requests_mock):
        requests_mock.register_uri(
            "POST", "/cde-service/integration/auth/", text=CDE_TOKEN_STRING
        )

        self.cdm_auth.create_cde_token()

        # The CDE auth endpoint expects the Alation token under the "token" header,
        # not the "Token" header used by every other Alation API.
        assert requests_mock.last_request.headers.get("token") == "alation-access-token"

    def test_success_create_cde_token_with_explicit_token_argument(self, requests_mock):
        requests_mock.register_uri(
            "POST", "/cde-service/integration/auth/", text=CDE_TOKEN_STRING
        )

        self.cdm_auth.create_cde_token(alation_token="override-token")

        assert requests_mock.last_request.headers.get("token") == "override-token"

    def test_failed_create_cde_token_unauthorized(self, requests_mock):
        failed_response = {
            "detail": "Alation token provided is invalid.",
            "code": "401000",
        }
        requests_mock.register_uri(
            "POST",
            "/cde-service/integration/auth/",
            json=failed_response,
            status_code=401,
        )

        with pytest.raises(requests.exceptions.HTTPError) as context:
            self.cdm_auth.create_cde_token()

        assert context.value.response.status_code == 401

    def test_failed_create_cde_token_empty_response(self, requests_mock):
        # Success status but no token in the body must not fail silently.
        requests_mock.register_uri(
            "POST", "/cde-service/integration/auth/", text=""
        )

        with pytest.raises(requests.exceptions.HTTPError) as context:
            self.cdm_auth.create_cde_token()

        assert context.value.response.status_code == 500

    def test_failed_create_cde_token_no_token_available(self):
        cdm_auth_no_token = AlationCDMAuthentication(
            session=requests.session(),
            host="https://test.com",
        )

        with pytest.raises(ValueError) as context:
            cdm_auth_no_token.create_cde_token()

        assert "No Alation API token available" in str(context.value)

    def test_exchange_overrides_default_authentication(self, requests_mock: Mocker) -> None:
        """Keep token exchange bodyless and separate from configured Bearer credentials.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Asserts the explicit exchange token is sent and defaults are unchanged.
        """
        self.cdm_auth.headers = {"Authorization": "Bearer inherited-token", "Content-Type": "application/json"}
        original_headers = self.cdm_auth.headers.copy()
        requests_mock.post("https://test.com/cde-service/integration/auth/", text=CDE_TOKEN_STRING)

        token = self.cdm_auth.create_cde_token(alation_token="explicit-token")

        assert token.token == CDE_TOKEN_STRING
        assert requests_mock.last_request.headers["token"] == "explicit-token"
        assert "Authorization" not in requests_mock.last_request.headers
        assert "CDEToken" not in requests_mock.last_request.headers
        assert "Content-Type" not in requests_mock.last_request.headers
        assert requests_mock.last_request.body is None
        assert self.cdm_auth.headers == original_headers

    @pytest.mark.parametrize("response_body", [{}, [], None, 42, "   "])
    def test_exchange_rejects_invalid_token_payloads(self, requests_mock: Mocker, response_body: object) -> None:
        """Reject success responses that do not contain a nonempty token string.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            response_body (object): Invalid JSON token response.

        Returns:
            None: Asserts token validation still raises the existing HTTP error.
        """
        requests_mock.post("https://test.com/cde-service/integration/auth/", json=response_body)

        with pytest.raises(requests.HTTPError) as exception:
            self.cdm_auth.create_cde_token()

        assert exception.value.response.status_code == 500
