"""Test the Alation REST API Authentication Methods."""
import pytest

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


