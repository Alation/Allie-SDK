"""Test the OAuth 2.0 API methods."""

import unittest

import requests
import requests_mock

from allie_sdk.methods.oauth2 import AlationOAuth2
from allie_sdk.models.oauth2_model import (
    ActiveIntrospectTokenResponse,
    ClientCredentialsGrantRequestPayload,
    InactiveIntrospectTokenResponse,
    JWKSetResponse,
    TokenIntrospectRequestPayload,
    TokenResponse,
)


MOCK_OAUTH2 = AlationOAuth2(session=requests.session(), host='https://test.com')


class TestOAuth2Methods(unittest.TestCase):

    @requests_mock.Mocker()
    def test_create_token_success(self, m):
        success_response = {
            "access_token": "abc",
            "token_type": "Bearer",
            "expires_in": 3600,
        }
        m.register_uri('POST', '/oauth/v2/token/', json=success_response)
        payload = ClientCredentialsGrantRequestPayload(grant_type='client_credentials')
        token = MOCK_OAUTH2.create_token(payload)
        expected = TokenResponse.from_api_response(success_response)
        self.assertEqual(token, expected)

    @requests_mock.Mocker()
    def test_create_token_failure(self, m):
        error_response = {"error": "invalid_client"}
        m.register_uri('POST', '/oauth/v2/token/', json=error_response, status_code=401)
        payload = ClientCredentialsGrantRequestPayload(grant_type='client_credentials')
        with self.assertRaises(requests.exceptions.HTTPError):
            MOCK_OAUTH2.create_token(payload)

    @requests_mock.Mocker()
    def test_introspect_token_active(self, m):
        active_response = {"active": True, "exp": 1, "iat": 1, "jti": "id", "nbf": 1}
        m.register_uri('POST', '/oauth/v2/introspect/', json=active_response)
        payload = TokenIntrospectRequestPayload(token='token')
        result = MOCK_OAUTH2.introspect_token(payload)
        expected = ActiveIntrospectTokenResponse.from_api_response(active_response)
        self.assertEqual(result, expected)

    @requests_mock.Mocker()
    def test_introspect_token_inactive(self, m):
        inactive_response = {"active": False}
        m.register_uri('POST', '/oauth/v2/introspect/', json=inactive_response)
        payload = TokenIntrospectRequestPayload(token='token')
        result = MOCK_OAUTH2.introspect_token(payload)
        expected = InactiveIntrospectTokenResponse.from_api_response(inactive_response)
        self.assertEqual(result, expected)

    @requests_mock.Mocker()
    def test_introspect_token_failure(self, m):
        error_response = {"error": "invalid_client"}
        m.register_uri('POST', '/oauth/v2/introspect/', json=error_response, status_code=401)
        payload = TokenIntrospectRequestPayload(token='token')
        with self.assertRaises(requests.exceptions.HTTPError):
            MOCK_OAUTH2.introspect_token(payload)

    @requests_mock.Mocker()
    def test_get_jwks(self, m):
        jwk_set = {
            "keys": [
                {"e": "AQAB", "kid": "1", "kty": "sig", "n": "mod", "use": "sig"}
            ]
        }
        m.register_uri('GET', '/oauth/v2/.well-known/jwks.json/', json=jwk_set)
        result = MOCK_OAUTH2.get_jwks()
        expected = JWKSetResponse.from_api_response(jwk_set)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

