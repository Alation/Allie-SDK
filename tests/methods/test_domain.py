"""Test the Alation REST API Domain Methods."""

import requests_mock
import unittest
import allie_sdk as allie
from allie_sdk.methods.domain import *


class TestDomain(unittest.TestCase):

    def setUp(self):
        self.mock_user = AlationDomain(
            access_token='test',
            session=requests.session(),
            host='https://test.com'
        )

    @requests_mock.Mocker()
    def test_get_domains(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the domain request?
        domain_api_response = [
            {
                "id": 1,
                "title": "Sales",
                "description": "Relevant data and articles for Sales Analytics",
                "parent_id": 2
            },
            {
                "id": 2,
                "title": "Marketing",
                "description": "Relevant data and articles for Marketing Analytics",
                "parent_id": 2
            }
        ]

        success_domains = [Domain.from_api_response(item) for item in domain_api_response]

        # Override the domain API call
        requests_mock.register_uri(
            method='GET',
            url='/integration/v2/domain/',
            json=domain_api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        domains = self.mock_user.get_domains()

        self.assertEqual(success_domains, domains)

    @requests_mock.Mocker()
    def test_assign_objects_to_domain(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        domain_api_response = {'exclude': False, 'id': 179, 'oid': [21, 23], 'otype': 'glossary_v3'}

        # Override the domain API call
        requests_mock.register_uri(
            method='POST',
            url='/integration/v2/domain/membership/',
            json=domain_api_response,
            status_code=201  # 202 if using async
        )

        # --- TEST THE FUNCTION --- #
        create_domain_membership_result = self.mock_user.assign_objects_to_domain(
            DomainMembership(
                id=179,
                oid=[21, 23],
                otype='glossary_v3'
            )
        )

        function_expected_result = [
            allie.JobDetails(
                status="successful",
                msg="",
                result=None
            )
        ]
        self.assertEqual(function_expected_result, create_domain_membership_result)

    @requests_mock.Mocker()
    def test_view_domain_membership_rules(self, requests_mock):
        api_response = [
            {
                "domain_id": 1,
                "exclude": False,
                "recursive": False,
                "otype": "table",
                "oid": 10,
            }
        ]

        requests_mock.register_uri(
            method='POST',
            url='/integration/v2/domain/membership/view_rules/',
            json=api_response,
            status_code=200,
        )

        rules = self.mock_user.get_domain_membership_rules(
            DomainMembershipRuleRequest(
                domain_ids=[1],
                exclude=False,
            )
        )

        expected_rules = [
            DomainMembershipRule(
                domain_id=1,
                exclude=False,
                recursive=False,
                otype="table",
                oid=10,
            )
        ]

        self.assertEqual(expected_rules, rules)
