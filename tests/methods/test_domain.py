"""Test the Alation REST API Domain Methods."""
import pytest
import allie_sdk as allie
from allie_sdk.methods.domain import *


class TestDomain:

    def setup_method(self):
        self.mock_user = AlationDomain(
            access_token='test',
            session=requests.session(),
            host='https://test.com'
        )

    
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

        assert success_domains == domains

    
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
        assert function_expected_result == create_domain_membership_result

    def test_create_domains(self, requests_mock):
        api_response = [
            {
                "id": 101,
                "title": "Finance",
                "description": "Finance owned assets",
                "parent_id": 10,
            }
        ]

        requests_mock.register_uri(
            method='POST',
            url='/integration/v2/domain/',
            json=api_response,
            status_code=201,
        )

        result = self.mock_user.create_domains(
            [
                DomainItem(
                    title="Finance",
                    description="Finance owned assets",
                    parent_id=10,
                )
            ]
        )

        expected = allie.JobDetails(
            status="successful",
            msg="",
            result=[
                Domain(
                    id=101,
                    title="Finance",
                    description="Finance owned assets",
                    parent_id=10,
                )
            ],
        )

        assert expected == result

    def test_delete_domains(self, requests_mock):
        api_response = {
            "status": "successful",
            "msg": "",
            "deleted_domain_count": 1,
            "deleted_domain_ids": [101],
        }

        requests_mock.register_uri(
            method='DELETE',
            url='/integration/v2/domain/',
            json=api_response,
            status_code=200,
        )

        result = self.mock_user.delete_domains(
            [DomainDeleteItem(id=101)]
        )

        expected = [
            allie.JobDetails(
                status="successful",
                msg="",
                result=None,
            )
        ]

        assert expected == result

    def test_move_domain(self, requests_mock):
        api_response = {
            "id": 101,
            "title": "Finance",
            "description": "Finance owned assets",
            "parent_id": 11,
        }

        requests_mock.register_uri(
            method='PATCH',
            url='/integration/v2/domain/101/',
            json=api_response,
            status_code=200,
        )

        result = self.mock_user.move_domain(
            101,
            DomainMoveItem(parent_id=11),
        )

        expected = allie.JobDetails(
            status="successful",
            msg="",
            result=Domain(
                id=101,
                title="Finance",
                description="Finance owned assets",
                parent_id=11,
            ),
        )

        assert expected == result

    
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

        assert expected_rules == rules

    def test_view_domain_membership_rules_with_pagination(self, requests_mock):
        first_page = [
            {
                "domain_id": 1,
                "exclude": False,
                "recursive": False,
                "otype": "table",
                "oid": 10,
            }
        ]
        second_page = [
            {
                "domain_id": 1,
                "exclude": False,
                "recursive": True,
                "otype": "schema",
                "oid": 11,
            }
        ]

        requests_mock.register_uri(
            method="POST",
            url="/integration/v2/domain/membership/view_rules/",
            json=first_page,
            headers={"X-Next-Page": "/integration/v2/domain/membership/view_rules/?skip=1&limit=1"},
            status_code=200,
        )
        requests_mock.register_uri(
            method="POST",
            url="/integration/v2/domain/membership/view_rules/?skip=1&limit=1",
            json=second_page,
            status_code=200,
        )

        rules = self.mock_user.get_domain_membership_rules(
            DomainMembershipRuleRequest(
                domain_ids=[1],
                exclude=False,
            )
        )

        assert rules == [
            DomainMembershipRule(
                domain_id=1,
                exclude=False,
                recursive=False,
                otype="table",
                oid=10,
            ),
            DomainMembershipRule(
                domain_id=1,
                exclude=False,
                recursive=True,
                otype="schema",
                oid=11,
            ),
        ]
        assert requests_mock.call_count == 2
        assert requests_mock.request_history[0].json() == {"domain_id": [1], "exclude": False}
        assert requests_mock.request_history[1].json() == {"domain_id": [1], "exclude": False}

    def test_view_domain_membership_rules_with_query_params(self, requests_mock):
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
            method="POST",
            url="/integration/v2/domain/membership/view_rules/",
            json=api_response,
            status_code=200,
        )

        rules = self.mock_user.get_domain_membership_rules(
            DomainMembershipRuleRequest(
                domain_ids=[1],
                exclude=False,
            ),
            DomainMembershipRuleParams(limit=50, skip=0),
        )

        assert rules == [
            DomainMembershipRule(
                domain_id=1,
                exclude=False,
                recursive=False,
                otype="table",
                oid=10,
            )
        ]
        assert requests_mock.last_request.qs == {"limit": ["50"], "skip": ["0"]}
