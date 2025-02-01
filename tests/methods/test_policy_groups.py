"""Test the Alation REST API Policy Group Methods."""

import requests_mock
import unittest
from allie_sdk.methods.policy_group import *


class TestPolicyGroup(unittest.TestCase):

    def setUp(self):
        self.mock_user = AlationPolicyGroup(
            access_token='test',
            session=requests.session(),
            host='https://test.com'
        )

    @requests_mock.Mocker()
    def test_get_policy_groups(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the Get Policy request?
        policy_group_api_response = [
            {
                "description": "All Policies governing human resources",
                "title": "HR policies",
                "id": 2,
                "otype": "policy_group",
                "ts_created": "2022-11-16T07:04:32.888040Z",
                "url": "/policy_group/1/",
                "stewards": [],
                "policies_count": 0
            },
            {
                "description": "All Policies governing freelancers",
                "title": "HR policies",
                "id": 3,
                "otype": "policy_group",
                "ts_created": "2022-11-17T07:04:32.888040Z",
                "url": "/policy_group/1/",
                "stewards": [],
                "policies_count": 0
            }
        ]

        success_policy_groups = [PolicyGroup(**pg) for pg in policy_group_api_response]

        # Override the policy API call
        requests_mock.register_uri(
            method='GET',
            url='/integration/v1/policy_group',
            json=policy_group_api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        policy_groups = self.mock_user.get_policy_groups()

        self.assertEqual(success_policy_groups, policy_groups)