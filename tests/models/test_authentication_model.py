"""Test the Alation REST API Authentication Methods."""

import pytest
from allie_sdk.methods.authentication import *

class TestAuthenticationModels:
    def test_refresh_token_model(self):

        refresh_response = {
            "user_id": 2,
            "created_at": "2022-11-15T21:52:48.116496Z",
            "token_expires_at": "2023-01-14T21:52:48.115754Z",
            "token_status": "ACTIVE",
            "last_used_at": None,
            "name": "Test Refresh Token",
            "refresh_token": "test_refresh_token"
        }
        refresh_token = RefreshToken.from_api_response(refresh_response)

        refresh_model = RefreshToken(
            user_id=2, created_at="2022-11-15T21:52:48.116496Z",
            token_expires_at="2023-01-14T21:52:48.115754Z",
            token_status="ACTIVE", last_used_at=None,
            name="Test Refresh Token", refresh_token="test_refresh_token"
        )

        assert refresh_token == refresh_model

    def test_access_access_token_model(self):

        access_response = {
            "user_id": 2,
            "created_at": "2022-12-13T21:24:20.647205Z",
            "token_expires_at": "2022-12-14T21:24:20.635180Z",
            "token_status": "ACTIVE",
            "api_access_token": "test_access_token"
        }
        access_token = AccessToken.from_api_response(access_response)

        access_model = AccessToken(
            user_id=2, created_at="2022-12-13T21:24:20.647205Z",
            token_expires_at="2022-12-14T21:24:20.635180Z",
            token_status="ACTIVE", api_access_token="test_access_token"
        )

        assert access_token == access_model

    def test_oauth_credentials_model(self):

        oauth_credentials_data = {
            "client_id": "test_client_id",
            "client_secret": "test_client_secret"
        }
        oauth_credentials = OAuthCredentials.from_api_response(oauth_credentials_data)

        oauth_model = OAuthCredentials(
            client_id="test_client_id",
            client_secret="test_client_secret"
        )

        assert oauth_credentials == oauth_model

    def test_oauth_token_model(self):

        oauth_token_response = {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": "read write",
            "created_at": "2026-03-26T10:30:00Z"
        }
        oauth_token = OAuthToken.from_api_response(oauth_token_response)

        oauth_model = OAuthToken(
            access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            token_type="Bearer",
            expires_in=3600,
            scope="read write",
            created_at="2026-03-26T10:30:00Z"
        )

        assert oauth_token == oauth_model
