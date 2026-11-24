"""Test the Alation REST API Authentication Methods."""
import base64
from urllib.parse import parse_qs

import pytest
from requests_mock import Mocker

from allie_sdk.methods.authentication import *



class TestAuthentication:
    
    def setup_method(self):
        self.mock_user = AlationAuthentication(
            refresh_token='test',
            user_id=1,
            session=requests.session(),
            host='https://test.com'
        )

    def test_success_validate_refresh_token(self, requests_mock):

        success_response = {
            "user_id": 1,
            "created_at": "2022-11-15T21:52:48.116496Z",
            "token_expires_at": "2023-01-14T21:52:48.115754Z",
            "token_status": "ACTIVE",
            "last_used_at": None,
            "name": "Postman",
            "refresh_token": "test"
        }
        success_token = RefreshToken.from_api_response(success_response)
        requests_mock.register_uri('POST', '/integration/v1/validateRefreshToken/', json=success_response)
        test_token = self.mock_user.validate_refresh_token()

        assert success_token == test_token

    def test_failed_validate_refresh_token(self, requests_mock):
        failed_response = {
            "detail": "Refresh token provided is invalid.",
            "code": "401000"
        }
        requests_mock.register_uri('POST', '/integration/v1/validateRefreshToken/', json=failed_response, status_code=401)
        
        # Now we expect an HTTPError to be raised
        with pytest.raises(requests.exceptions.HTTPError) as context:
            self.mock_user.validate_refresh_token()
        
        # Verify the error response contains expected information
        assert context.value.response.status_code == 401

    def test_success_create_access_token(self, requests_mock):

        access_success_response = {
            "user_id": 1,
            "created_at": "2022-12-13T21:46:24.599775Z",
            "token_expires_at": "2022-12-14T21:46:24.594949Z",
            "token_status": "ACTIVE",
            "api_access_token": "test"
        }
        refresh_success_response = {
            "user_id": 1,
            "created_at": "2022-11-15T21:52:48.116496Z",
            "token_expires_at": "2023-01-14T21:52:48.115754Z",
            "token_status": "ACTIVE",
            "last_used_at": None,
            "name": "Postman",
            "refresh_token": "test"
        }
        success_token = AccessToken.from_api_response(access_success_response)
        requests_mock.register_uri('POST', '/integration/v1/createAPIAccessToken/', json=access_success_response)
        requests_mock.register_uri('POST', '/integration/v1/validateRefreshToken/', json=refresh_success_response)
        test_token = self.mock_user.create_access_token()

        assert success_token == test_token

    def test_failed_create_access_token(self, requests_mock):
        failed_response = {
            "detail": "Refresh token provided is invalid.",
            "code": "401000"
        }
        refresh_success_response = {
            "user_id": 1,
            "created_at": "2022-11-15T21:52:48.116496Z",
            "token_expires_at": "2023-01-14T21:52:48.115754Z",
            "token_status": "ACTIVE",
            "last_used_at": None,
            "name": "Postman",
            "refresh_token": "test"
        }
        requests_mock.register_uri('POST', '/integration/v1/createAPIAccessToken/', json=failed_response, status_code=401)
        requests_mock.register_uri('POST', '/integration/v1/validateRefreshToken/', json=refresh_success_response)
        
        # Now we expect an HTTPError to be raised
        with pytest.raises(requests.exceptions.HTTPError) as context:
            self.mock_user.create_access_token()
        
        # Verify the error response contains expected information
        assert context.value.response.status_code == 401

    def test_failed_create_access_token_expired_refresh_token(self, requests_mock):
        refresh_response = {
            "user_id": 1,
            "created_at": "2022-11-15T21:52:48.116496Z",
            "token_expires_at": "2023-01-14T21:52:48.115754Z",
            "token_status": "EXPIRED",
            "last_used_at": None,
            "name": "Postman",
            "refresh_token": "test"
        }
        requests_mock.register_uri('POST', '/integration/v1/validateRefreshToken/', json=refresh_response)
        
        # Now we expect an HTTPError to be raised
        with pytest.raises(requests.exceptions.HTTPError) as context:
            self.mock_user.create_access_token()
        
        # Verify the error response contains expected information
        assert context.value.response.status_code == 401

    def test_success_validate_access_token(self, requests_mock):

        success_response = {
            "user_id": 1,
            "created_at": "2022-12-13T21:46:24.599775Z",
            "token_expires_at": "2022-12-14T21:46:24.594949Z",
            "token_status": "ACTIVE",
            "api_access_token": "test"
        }
        success_token = AccessToken.from_api_response(success_response)
        requests_mock.register_uri('POST', '/integration/v1/validateAPIAccessToken/', json=success_response)
        test_token = self.mock_user.validate_access_token(success_token.api_access_token)

        assert success_token == test_token

    def test_failed_validate_access_token(self, requests_mock):
        failed_response = {
            "detail": "API Access Token provided is invalid.",
            "code": "401000"
        }
        requests_mock.register_uri('POST', '/integration/v1/validateAPIAccessToken/', json=failed_response,
                      status_code=401)
        
        # Now we expect an HTTPError to be raised
        with pytest.raises(requests.exceptions.HTTPError) as context:
            self.mock_user.validate_access_token('test')
        
        # Verify the error response contains expected information
        assert context.value.response.status_code == 401

    def test_success_revoke_access_tokens(self, requests_mock):

        success_response = {
            "detail": "Revoked active access tokens for refresh token: 'test' with id: 1"
        }
        requests_mock.register_uri('POST', '/integration/v1/revokeAPIAccessTokens/', json=success_response)
        actual_result = self.mock_user.revoke_access_tokens()

        expected_result = JobDetails(
            status='successful'
            , msg=''
            , result={'detail': "Revoked active access tokens for refresh token: 'test' with id: 1"}
        )

        assert expected_result == actual_result

    def test_failed_revoke_access_tokens(self, requests_mock):
        failed_response = {
            "detail": "Refresh token provided is invalid.",
            "code": "401000"
        }
        requests_mock.register_uri('POST', '/integration/v1/revokeAPIAccessTokens/', json=failed_response, status_code=401)
        
        # Now we expect an HTTPError to be raised
        with pytest.raises(requests.exceptions.HTTPError) as context:
            self.mock_user.revoke_access_tokens()
        
        # Verify the error response contains expected information
        assert context.value.response.status_code == 401


class TestOAuthAuthentication:
    """Test OAuth authentication methods."""
    
    def setup_method(self):
        """Set up OAuth authentication test instance."""
        self.oauth_auth = AlationAuthentication(
            session=requests.session(),
            host='https://test.com',
            client_id='test_client_id',
            client_secret='test_client_secret'
        )
        # Set access_token to None to prevent AttributeError in HTTP methods
        self.oauth_auth.access_token = None
        
        self.oauth_auth_no_creds = AlationAuthentication(
            session=requests.session(),
            host='https://test.com'
        )
        # Set access_token to None to prevent AttributeError in HTTP methods  
        self.oauth_auth_no_creds.access_token = None

    @pytest.mark.parametrize("use_basic_auth", [False, True], ids=["body-credentials", "basic-auth"])
    @pytest.mark.parametrize(
        ("client_id", "client_secret"),
        [
            pytest.param("test_client_id", "test_client_secret", id="plain-credentials"),
            pytest.param("client+id &=/?%#", "secret+value&key=1 /?%#:", id="special-characters"),
        ],
    )
    def test_success_create_oauth_token(
        self,
        requests_mock: Mocker,
        use_basic_auth: bool,
        client_id: str,
        client_secret: str,
    ) -> None:
        """Verify OAuth form encoding and credential placement in both modes.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            use_basic_auth (bool): Whether credentials belong in the Basic header.
            client_id (str): Client identifier, potentially containing reserved characters.
            client_secret (str): Client secret, potentially containing reserved characters.

        Returns:
            None: Asserts the token response and the outgoing request match the selected mode.
        """
        authentication = AlationAuthentication(
            host="https://test.com",
            session=requests.Session(),
            client_id=client_id,
            client_secret=client_secret,
        )
        oauth_success_response = {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test_payload.test_signature",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": "read write"
        }
        
        success_token = OAuthToken.from_api_response(oauth_success_response)
        requests_mock.register_uri('POST', '/oauth/v2/token', json=oauth_success_response)
        test_token = authentication.create_oauth_token(use_basic_auth=use_basic_auth)

        assert success_token.access_token == test_token.access_token
        assert success_token.token_type == test_token.token_type
        assert success_token.expires_in == test_token.expires_in

        outgoing_request = requests_mock.last_request
        assert outgoing_request.headers["Content-Type"] == "application/x-www-form-urlencoded"
        assert "Token" not in outgoing_request.headers
        form_fields = parse_qs(outgoing_request.text, strict_parsing=True)
        expected_form_fields = {"grant_type": ["client_credentials"]}
        if use_basic_auth:
            encoded_credentials = base64.b64encode(f"{client_id}:{client_secret}".encode("ascii")).decode("ascii")
            assert outgoing_request.headers["Authorization"] == f"Basic {encoded_credentials}"
        else:
            expected_form_fields.update({"client_id": [client_id], "client_secret": [client_secret]})
            assert "Authorization" not in outgoing_request.headers
        assert form_fields == expected_form_fields

    @pytest.mark.parametrize("use_basic_auth", [False, True], ids=["body-credentials", "basic-auth"])
    def test_failed_create_oauth_token_invalid_client(self, requests_mock: Mocker, use_basic_auth: bool) -> None:
        """Verify invalid credentials raise HTTPError in either OAuth mode.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            use_basic_auth (bool): Whether to authenticate using the Basic header.

        Returns:
            None: Asserts the HTTP authentication failure is preserved.
        """
        failed_response = {
            "error": "invalid_client",
            "error_description": "Client authentication failed"
        }
        
        requests_mock.register_uri('POST', '/oauth/v2/token', json=failed_response, status_code=401)
        
        # Expect HTTPError to be raised
        with pytest.raises(requests.exceptions.HTTPError) as context:
            self.oauth_auth.create_oauth_token(use_basic_auth=use_basic_auth)
        
        assert context.value.response.status_code == 401

    def test_create_oauth_token_missing_credentials(self):
        """Test OAuth token creation failure when credentials are missing."""
        # Expect ValueError when no client credentials are provided
        with pytest.raises(ValueError) as context:
            self.oauth_auth_no_creds.create_oauth_token()
        
        assert "Client ID and client secret are required" in str(context.value)

    def test_create_oauth_token_with_credentials_parameter(self, requests_mock):
        """Test OAuth token creation using OAuthCredentials parameter."""
        oauth_success_response = {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test_payload.test_signature",
            "token_type": "Bearer",
            "expires_in": 3600
        }
        
        credentials = OAuthCredentials(
            client_id='param_client_id',
            client_secret='param_client_secret'
        )
        
        requests_mock.register_uri('POST', '/oauth/v2/token', json=oauth_success_response)
        test_token = self.oauth_auth_no_creds.create_oauth_token(client_credentials=credentials)

        assert test_token.access_token == oauth_success_response["access_token"]
        assert parse_qs(requests_mock.last_request.text, strict_parsing=True) == {
            "grant_type": ["client_credentials"],
            "client_id": [credentials.client_id],
            "client_secret": [credentials.client_secret],
        }


