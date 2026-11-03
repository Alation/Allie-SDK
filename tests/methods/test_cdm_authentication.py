"""Test the Alation Critical Data Manager (CDM / CDE) API Authentication Methods."""
import pytest
import requests

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
