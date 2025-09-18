"""Test the OAuth 2.0 API V2 data models."""

import unittest

from allie_sdk.models.oauth2_model import (
    TokenResponse,
    ActiveIntrospectTokenResponse,
    InactiveIntrospectTokenResponse,
    JWKResponse,
    JWKSetResponse,
    ClientCredentialsGrantRequestPayload,
    TokenIntrospectRequestPayload,
    ErrorResponse,
)


class TestOAuth2Models(unittest.TestCase):

    def test_token_response_model(self):
        response = {
            "access_token": "2YotnFZFEjr1zCsicMWpAA",
            "token_type": "Bearer",
            "expires_in": 3600,
        }
        token = TokenResponse.from_api_response(response)
        expected = TokenResponse(
            access_token="2YotnFZFEjr1zCsicMWpAA",
            token_type="Bearer",
            expires_in=3600,
        )
        self.assertEqual(token, expected)

    def test_active_introspect_token_response_model(self):
        response = {
            "active": True,
            "client_id": "4e0dfdf0-1a77-41e5-9d7b-4cab6d926e02",
            "exp": 1643791003,
            "iat": 1643791003,
            "iss": "https://example.com",
            "jti": "f6a3a277-5006-4e35-84a6-ead3c2efe726",
            "nbf": 1643791003,
            "sub": "example@example.com",
            "unique_id": "f6a3a277-5006-4e35-84a6-ead3c2efe726",
        }
        introspection = ActiveIntrospectTokenResponse.from_api_response(response)
        expected = ActiveIntrospectTokenResponse(
            active=True,
            client_id="4e0dfdf0-1a77-41e5-9d7b-4cab6d926e02",
            exp=1643791003,
            iat=1643791003,
            iss="https://example.com",
            jti="f6a3a277-5006-4e35-84a6-ead3c2efe726",
            nbf=1643791003,
            sub="example@example.com",
            unique_id="f6a3a277-5006-4e35-84a6-ead3c2efe726",
        )
        self.assertEqual(introspection, expected)

    def test_inactive_introspect_token_response_model(self):
        response = {"active": False}
        introspection = InactiveIntrospectTokenResponse.from_api_response(response)
        expected = InactiveIntrospectTokenResponse(active=False)
        self.assertEqual(introspection, expected)

    def test_jwk_set_response_model(self):
        response = {
            "keys": [
                {
                    "e": "AQAB",
                    "kid": "1",
                    "kty": "sig",
                    "n": "modulus",
                    "use": "sig",
                }
            ]
        }
        jwk_set = JWKSetResponse.from_api_response(response)
        expected = JWKSetResponse(
            keys=[
                JWKResponse(e="AQAB", kid="1", kty="sig", n="modulus", use="sig")
            ]
        )
        self.assertEqual(jwk_set, expected)

    def test_request_payload_models(self):
        token_request = ClientCredentialsGrantRequestPayload(
            grant_type="client_credentials",
            client_id="s6BhdRkqt3",
            client_secret="P@s$w0rd!",
        )
        self.assertEqual(token_request.grant_type, "client_credentials")

        introspect_request = TokenIntrospectRequestPayload(
            token="token",
            token_type_hint="access_token",
            client_id="client",
            client_secret="secret",
        )
        self.assertEqual(introspect_request.token_type_hint, "access_token")

    def test_error_response_model(self):
        response = {
            "error": "invalid_client",
            "error_description": "Client credentials might be incorrect or client not found.",
            "code": "401",
        }
        error = ErrorResponse.from_api_response(response)
        expected = ErrorResponse(
            error="invalid_client",
            error_description="Client credentials might be incorrect or client not found.",
            code="401",
        )
        self.assertEqual(error, expected)


if __name__ == "__main__":
    unittest.main()
