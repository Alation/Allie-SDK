"""Test the Alation REST API User Methods."""

import requests_mock
import unittest
from allie_sdk.methods.user import *

MOCK_USER = AlationUser(
    access_token='test', session=requests.session(), host='https://test.com'
)


class TestUser(unittest.TestCase):

    @requests_mock.Mocker()
    def test_success_get_users_v1(self, m):

        MOCK_USER.use_v2_endpoint = False
        success_response = [
            {
                "display_name": "Test User 1",
                "email": "test-user-1@alation.com",
                "id": 1,
                "profile_id": 1,
                "url": "/user/1/"
            },
            {
                "display_name": "Test User 2",
                "email": "test-user-2@alation.com",
                "id": 2,
                "profile_id": 2,
                "url": "/user/2/"
            },
            {
                "display_name": "Test User 3",
                "email": "test-user-3@alation.com",
                "id": 3,
                "profile_id": 3,
                "url": "/user/3/"
            }
        ]
        success_users = [User.from_api_response(user) for user in success_response]
        m.register_uri('GET', '/integration/v1/user/', json=success_response)
        users = MOCK_USER.get_users()

        self.assertEqual(success_users, users)

    @requests_mock.Mocker()
    def test_failed_get_users_v1(self, m):

        MOCK_USER.use_v2_endpoint = False
        failed_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }
        m.register_uri('GET', '/integration/v1/user/', json=failed_response, status_code=403)
        users = MOCK_USER.get_users()

        self.assertIsNone(users)

    @requests_mock.Mocker()
    def test_success_get_a_user_v1(self, m):

        MOCK_USER.use_v2_endpoint = False
        success_response = {
            "display_name": "Test User 1",
            "email": "test-user-1@alation.com",
            "id": 1,
            "profile_id": 1,
            "url": "/user/1/"
        }
        success_user = User.from_api_response(success_response)
        m.register_uri('GET', '/integration/v1/user/1/', json=success_response)
        user = MOCK_USER.get_a_user(1)

        self.assertEqual(success_user, user)

    @requests_mock.Mocker()
    def test_failed_get_a_user_v1(self, m):

        MOCK_USER.use_v2_endpoint = False
        failed_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }
        m.register_uri('GET', '/integration/v1/user/1/', json=failed_response, status_code=403)
        user = MOCK_USER.get_a_user(1)

        self.assertIsNone(user)

    @requests_mock.Mocker()
    def test_success_get_users_v2(self, m):

        MOCK_USER.use_v2_endpoint = True
        success_response = [
            {
                "display_name": "Test User 1",
                "email": "test-user-1@alation.com",
                "id": 1,
                "profile_id": 1,
                "url": "/user/1/",
                "last_login": "2022-06-16T20:43:47.772954Z",
                "ts_created": "2022-06-15T15:24:19.258558Z"
            },
            {
                "display_name": "Test User 2",
                "email": "test-user-2@alation.com",
                "id": 2,
                "profile_id": 2,
                "url": "/user/2/",
                "last_login": "2022-12-27T16:44:53.414125Z",
                "ts_created": "2022-06-15T17:01:37.741810Z"
            },
            {
                "display_name": "Test User 3",
                "email": "test-user-3@alation.com",
                "id": 3,
                "profile_id": 3,
                "url": "/user/3/",
                "last_login": "2022-10-26T02:04:14.943074Z",
                "ts_created": "2022-06-22T16:13:34.862449Z"
            }
        ]
        success_users = [User.from_api_response(user) for user in success_response]
        m.register_uri('GET', '/integration/v2/user/', json=success_response)
        users = MOCK_USER.get_users()

        self.assertEqual(success_users, users)

    @requests_mock.Mocker()
    def test_failed_get_users_v2(self, m):

        MOCK_USER.use_v2_endpoint = True
        failed_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }
        m.register_uri('GET', '/integration/v2/user/', json=failed_response, status_code=403)
        users = MOCK_USER.get_users()

        self.assertIsNone(users)

    @requests_mock.Mocker()
    def test_success_get_a_user_v2(self, m):

        MOCK_USER.use_v2_endpoint = True
        success_response = {
            "display_name": "Test User 1",
            "email": "test-user-1@alation.com",
            "id": 1,
            "profile_id": 1,
            "url": "/user/1/",
            "last_login": "2022-12-27T16:44:53.414125Z",
            "ts_created": "2022-06-15T17:01:37.741810Z"
        }
        success_user = User.from_api_response(success_response)
        m.register_uri('GET', '/integration/v2/user/1/', json=success_response)
        user = MOCK_USER.get_a_user(1)

        self.assertEqual(success_user, user)

    @requests_mock.Mocker()
    def test_failed_get_a_user_v1(self, m):

        MOCK_USER.use_v2_endpoint = True
        failed_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }
        m.register_uri('GET', '/integration/v2/user/1/', json=failed_response, status_code=403)
        user = MOCK_USER.get_a_user(1)

        self.assertIsNone(user)

    @requests_mock.Mocker()
    def test_success_get_authenticated_user(self, m):

        success_response = {
            "email": "test-user-1@alation.com",
            "first_name": "Test",
            "id": 1,
            "last_name": "User 1",
            "role": "SERVER_ADMIN",
            "title": "",
            "username": "test-user-1@alation.com",
        }
        success_details = User.from_api_response(success_response)
        m.register_uri('GET', '/integration/v1/userinfo/', json=success_response)
        details = MOCK_USER.get_authenticated_user()

        self.assertEqual(success_details, details)

    @requests_mock.Mocker()
    def test_failed_get_authenticated_user(self, m):

        failed_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }
        m.register_uri('GET', '/integration/v1/userinfo/', json=failed_response, status_code=403)
        details = MOCK_USER.get_authenticated_user()

        self.assertIsNone(details)


if __name__ == '__main__':
    unittest.main()
