"""Test the Alation REST API User Models."""

import unittest
from allie_sdk.methods.user import *


class TestUserModels(unittest.TestCase):

    def test_v1_user_model(self):

        user_response = {
            "display_name": "SDK Test User",
            "email": "test-user@alation.com",
            "id": 2,
            "profile_id": 2,
            "url": "/user/2/"
        }
        user = User.from_api_response(user_response)

        user_model = User(
            display_name="SDK Test User", email="test-user@alation.com",
            id=2, profile_id=2, url="/user/2/"
        )

        self.assertEqual(user, user_model)

    def test_v2_user_model(self):

        user_response = {
            "display_name": "SDK Test User",
            "email": "test-user@alation.com",
            "id": 2,
            "profile_id": 2,
            "url": "/user/2/",
            "last_login": "2022-12-27T16:44:53.414125Z",
            "ts_created": "2022-06-15T17:01:37.741810Z"
        }
        user = User.from_api_response(user_response)

        user_model = User(
            display_name="SDK Test User", email="test-user@alation.com",
            id=2, profile_id=2, url="/user/2/", last_login="2022-12-27T16:44:53.414125Z",
            ts_created="2022-06-15T17:01:37.741810Z"
        )

        self.assertEqual(user, user_model)

    def test_user_details_model(self):

        details_response = {
            "email": "test-user@alation.com",
            "first_name": "SDK",
            "id": 2,
            "last_name": "Test User",
            "role": "SERVER_ADMIN",
            "title": "",
            "username": "test-user@alation.com"
        }
        user_details = User.from_api_response(details_response)

        details_model = User(
            email="test-user@alation.com", first_name="SDK", id=2,
            last_name="Test User", role="SERVER_ADMIN", title="",
            username="test-user@alation.com"
        )

        self.assertEqual(user_details, details_model)


if __name__ == '__main__':
    unittest.main()
