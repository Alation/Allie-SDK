"""Test the Alation REST API Authentication Methods."""

import unittest
from allie_sdk.methods.authentication import *


class TestAuthenticationModels(unittest.TestCase):

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

        self.assertEqual(refresh_token, refresh_model)

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

        self.assertEqual(access_token, access_model)


if __name__ == '__main__':
    unittest.main()
