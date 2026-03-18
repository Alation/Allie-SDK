"""Test the Alation REST API Tag Models."""

import pytest

from allie_sdk.core.custom_exceptions import InvalidPostBody
from allie_sdk.models.tag_model import Tag, TagItem, TagObjectItem, TagParams, TaggedObject, TaggedObjectParams


class TestTagModels:

    def test_tag_model(self):
        tag_response = {
            "id": 16,
            "name": "PII",
            "description": "Contains personally identifiable information",
            "number_of_objects_tagged": 3,
            "ts_created": "2024-07-11T18:48:06.377294Z",
            "url": "/tag/16/"
        }

        tag = Tag.from_api_response(tag_response)

        expected = Tag(
            id=16,
            name="PII",
            description="Contains personally identifiable information",
            number_of_objects_tagged=3,
            ts_created="2024-07-11T18:48:06.377294Z",
            url="/tag/16/"
        )

        assert tag == expected

    def test_tagged_object_model(self):
        subject_response = {
            "ts_tagged": "2024-07-11T18:48:10.377294Z",
            "object": {
                "url": "/data/2/",
                "otype": "data",
                "id": 2
            }
        }

        subject = TaggedObject.from_api_response(subject_response)

        expected = TaggedObject(
            ts_tagged="2024-07-11T18:48:10.377294Z",
            object={
                "url": "/data/2/",
                "otype": "data",
                "id": 2
            }
        )

        assert subject == expected

    def test_tag_object_post_payload(self):
        subject = TagObjectItem(oid=25, otype="article")

        assert subject.generate_api_post_payload() == {
            "oid": 25,
            "otype": "article"
        }

    def test_tag_object_post_payload_requires_oid(self):
        subject = TagObjectItem(otype="article")

        with pytest.raises(InvalidPostBody):
            subject.generate_api_post_payload()

    def test_tag_object_post_payload_requires_otype(self):
        subject = TagObjectItem(oid=25)

        with pytest.raises(InvalidPostBody):
            subject.generate_api_post_payload()

    def test_tag_patch_payload(self):
        tag = TagItem(name="Sensitive", description="Updated description")

        assert tag.generate_api_patch_payload() == {
            "name": "Sensitive",
            "description": "Updated description"
        }

    def test_tag_patch_payload_allows_empty_description(self):
        tag = TagItem(description="")

        assert tag.generate_api_patch_payload() == {
            "description": ""
        }

    def test_tag_patch_payload_requires_fields(self):
        tag = TagItem()

        with pytest.raises(InvalidPostBody):
            tag.generate_api_patch_payload()

    def test_tag_params_generate(self):
        params = TagParams(oid=2, otype="data", limit=10, order_by="name")

        assert params.generate_params_dict() == {
            "oid": 2,
            "otype": "data",
            "limit": 10,
            "order_by": "name"
        }

    def test_tagged_object_params_generate(self):
        params = TaggedObjectParams(limit=20, skip=5, order_by="-ts_tagged", exclude_deleted=True)

        assert params.generate_params_dict() == {
            "limit": 20,
            "skip": 5,
            "order_by": "-ts_tagged",
            "exclude_deleted": True
        }
