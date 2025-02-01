"""Test the Alation REST API Group Methods."""

import requests_mock
import unittest
from allie_sdk.methods.group import *


class TestGroup(unittest.TestCase):

    def setUp(self):
        self.mock_user = AlationGroup(
            access_token='test',
            session=requests.session(),
            host='https://test.com'
        )

    @requests_mock.Mocker()
    def test_get_groups(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the Get Group request?
        group_api_response = [
            {
                "display_name": "Stewards",
                "email": "stewards@mycompany.com",
                "id": 10,
                "profile_id": 10,
                "url": "/group/10/"
            },
            {
                "display_name": "DataGov",
                "email": "datagov@mycompany.com",
                "id": 11,
                "profile_id": 11,
                "url": "/group/11/"
            }
        ]

        success_groups = [Group.from_api_response(item) for item in group_api_response]

        # Override the group API call
        requests_mock.register_uri(
            method='GET',
            url='/integration/v1/group/',
            json=group_api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        groups = self.mock_user.get_groups()

        self.assertEqual(success_groups, groups)