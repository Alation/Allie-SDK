import unittest
from allie_sdk.methods.domain import *


class TestDomainModels(unittest.TestCase):

    def test_domain_model(self):
        # Expected input
        input = {
          "id": 1,
          "title": "Sales",
          "description": "Relevant data and articles for Sales Analytics",
          "parent_id": 2
        }

        # Transformation
        input_transformed = Domain(**input)

        # Expected Output
        output = Domain(
            id=1,
            title = "Sales",
            description = "Relevant data and articles for Sales Analytics",
            parent_id = 2
        )

        self.assertEqual(input_transformed, output)

    def test_domain_membership_model(self):
        # Expected input
        input = DomainMembership(
            id = 179
            , oid = [21, 23]
            , otype = 'glossary_v3'
        )

        # Transformation
        input_transformed = DomainMembership.generate_api_post_payload(input)

        # Expected Output
        output = {
            "id": 179
            , "oid": [21, 23]
            , "otype": "glossary_v3"
        }

        self.assertEqual(input_transformed, output)

    def test_domain_membership_rule_request_payload(self):
        request = DomainMembershipRuleRequest(
            domain_ids=[1, 2],
            exclude=True,
            recursive=False,
        )

        self.assertEqual(
            request.generate_api_post_payload(),
            {
                "domain_id": [1, 2],
                "exclude": True,
                "recursive": False,
            },
        )

    def test_domain_membership_rule_from_response(self):
        rule = DomainMembershipRule.from_api_response(
            {
                "domain_id": 1,
                "exclude": False,
                "recursive": True,
                "otype": "table",
                "oid": 42,
            }
        )

        self.assertEqual(
            rule,
            DomainMembershipRule(
                domain_id=1,
                exclude=False,
                recursive=True,
                otype="table",
                oid=42,
            ),
        )
