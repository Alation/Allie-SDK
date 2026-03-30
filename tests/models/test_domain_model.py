import pytest
from allie_sdk.methods.domain import *
from allie_sdk.core.custom_exceptions import InvalidPostBody


class TestDomainModels:

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

        assert input_transformed == output

    def test_domain_item_post_payload(self):
        domain = DomainItem(
            title="Finance",
            description="Finance owned assets",
            parent_id=5,
        )

        assert domain.generate_api_post_payload() == {
            "title": "Finance",
            "description": "Finance owned assets",
            "parent_id": 5,
        }

    def test_domain_delete_item_delete_payload(self):
        domain = DomainDeleteItem(id=7)

        assert domain.generate_api_delete_payload() == {"id": 7}

    def test_domain_move_item_patch_payload(self):
        domain = DomainMoveItem(parent_id=9)

        assert domain.generate_api_patch_payload() == {"parent_id": 9}

    def test_domain_item_requires_title(self):
        with pytest.raises(InvalidPostBody):
            DomainItem().generate_api_post_payload()

    def test_domain_delete_item_requires_id(self):
        with pytest.raises(InvalidPostBody):
            DomainDeleteItem().generate_api_delete_payload()

    def test_domain_move_item_requires_parent_id(self):
        with pytest.raises(InvalidPostBody):
            DomainMoveItem().generate_api_patch_payload()

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

        assert input_transformed == output

    def test_domain_membership_rule_request_payload(self):
        request = DomainMembershipRuleRequest(
            domain_ids=[1, 2],
            exclude=True,
            recursive=False,
        )

        expected = {
                "domain_id": [1, 2],
                "exclude": True,
                "recursive": False,
            }

        assert request.generate_api_post_payload() == expected

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

        assert rule == DomainMembershipRule(
                domain_id=1,
                exclude=False,
                recursive=True,
                otype="table",
                oid=42,
            )
