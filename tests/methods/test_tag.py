"""Test the Alation REST API Tag Methods."""

import pytest
from requests import HTTPError

from allie_sdk.methods.tag import *


class TestTag:

    def setup_method(self):
        self.mock_tag = AlationTag(
            access_token="test",
            session=requests.session(),
            host="https://test.com"
        )

    def test_get_tags(self, requests_mock):
        tag_api_response = [
            {
                "id": 16,
                "name": "PII",
                "description": "Contains personally identifiable information",
                "number_of_objects_tagged": 3,
                "ts_created": "2024-07-11T18:48:06.377294Z",
                "url": "/tag/16/"
            }
        ]

        success_tags = [Tag.from_api_response(item) for item in tag_api_response]

        requests_mock.register_uri(
            method="GET",
            url="/integration/tag/",
            json=tag_api_response,
            status_code=200
        )

        tags = self.mock_tag.get_tags()

        assert success_tags == tags

    def test_get_tags_with_query_params(self, requests_mock):
        tag_api_response = [
            {
                "id": 16,
                "name": "PII",
                "description": "Contains personally identifiable information",
                "number_of_objects_tagged": 1,
                "ts_created": "2024-07-11T18:48:06.377294Z",
                "url": "/tag/16/"
            }
        ]

        requests_mock.register_uri(
            method="GET",
            url="/integration/tag/",
            json=tag_api_response,
            status_code=200
        )

        tags = self.mock_tag.get_tags(TagParams(oid=2, otype="data"))

        assert tags == [Tag.from_api_response(tag_api_response[0])]
        assert requests_mock.last_request.qs == {"oid": ["2"], "otype": ["data"]}

    def test_get_a_tag(self, requests_mock):
        tag_api_response = {
            "id": 16,
            "name": "PII",
            "description": "Contains personally identifiable information",
            "number_of_objects_tagged": 3,
            "ts_created": "2024-07-11T18:48:06.377294Z",
            "url": "/tag/16/"
        }

        requests_mock.register_uri(
            method="GET",
            url="/integration/tag/16/",
            json=tag_api_response,
            status_code=200
        )

        tag = self.mock_tag.get_a_tag(16)

        assert tag == Tag.from_api_response(tag_api_response)

    def test_get_objects_tagged_with_specific_tag(self, requests_mock):
        subject_api_response = [
            {
                "ts_tagged": "2024-07-11T18:48:10.377294Z",
                "object": {
                    "url": "/data/2/",
                    "otype": "data",
                    "id": 2
                }
            }
        ]

        requests_mock.register_uri(
            method="GET",
            url="/integration/tag/PII/subject/",
            json=subject_api_response,
            status_code=200
        )

        subjects = self.mock_tag.get_objects_tagged_with_specific_tag("PII")

        assert subjects == [TaggedObject.from_api_response(subject_api_response[0])]

    def test_get_objects_tagged_with_specific_tag_url_encodes_tag_name(self, requests_mock):
        subject_api_response = []

        requests_mock.register_uri(
            method="GET",
            url="/integration/tag/Highly%20Sensitive/subject/",
            json=subject_api_response,
            status_code=200
        )

        subjects = self.mock_tag.get_objects_tagged_with_specific_tag(
            "Highly Sensitive",
            TaggedObjectParams(limit=10, order_by="-ts_tagged")
        )

        assert subjects == []
        assert requests_mock.last_request.qs == {"limit": ["10"], "order_by": ["-ts_tagged"]}

    def test_add_tag_to_object(self, requests_mock):
        tag_api_response = {
            "id": 16,
            "name": "PII",
            "description": "Contains personally identifiable information",
            "number_of_objects_tagged": 4,
            "ts_created": "2024-07-11T18:48:06.377294Z",
            "url": "/tag/16/"
        }

        requests_mock.register_uri(
            method="POST",
            url="/integration/tag/PII/subject/",
            json=tag_api_response,
            status_code=201
        )

        tag = self.mock_tag.add_tag_to_object("PII", TagObjectItem(oid=2, otype="data"))

        assert tag == Tag.from_api_response(tag_api_response)
        assert requests_mock.last_request.json() == {"oid": 2, "otype": "data"}

    def test_update_tag(self, requests_mock):
        tag_api_response = {
            "id": 16,
            "name": "Sensitive",
            "description": "Updated description",
            "number_of_objects_tagged": 4,
            "ts_created": "2024-07-11T18:48:06.377294Z",
            "url": "/tag/16/"
        }

        requests_mock.register_uri(
            method="PATCH",
            url="/integration/tag/16/",
            json=tag_api_response,
            status_code=200
        )

        tag = self.mock_tag.update_tag(
            16,
            TagItem(name="Sensitive", description="Updated description")
        )

        assert tag == Tag.from_api_response(tag_api_response)
        assert requests_mock.last_request.json() == {
            "name": "Sensitive",
            "description": "Updated description"
        }

    def test_remove_tag_from_object(self, requests_mock):
        requests_mock.register_uri(
            method="DELETE",
            url="/integration/tag/PII/subject/data/2/",
            text="",
            status_code=204
        )

        result = self.mock_tag.remove_tag_from_object("PII", "data", 2)

        assert result == JobDetails(status="successful", msg="", result="")

    def test_get_tags_http_error(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/integration/tag/",
            json={"detail": "Authentication credentials were not provided.", "code": "403000"},
            status_code=403
        )

        with pytest.raises(HTTPError) as context:
            self.mock_tag.get_tags()

        assert context.value.response.status_code == 403
