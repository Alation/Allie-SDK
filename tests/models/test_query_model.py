"""Tests for the Query data models."""

import unittest
from datetime import datetime

from allie_sdk.models.query_model import (
    Query,
    QueryAuthor,
    QueryCreateRequest,
)
from allie_sdk.core.custom_exceptions import InvalidPostBody


class TestQueryModel(unittest.TestCase):
    def test_query_from_api_response_maps_nested_objects(self):
        api_response = {
            "datasource_id": 1,
            "autosave_content": "SELECT 1",
            "content": "SELECT 1",
            "title": "Test Query",
            "saved": True,
            "published": False,
            "description": "Description",
            "url": "/integration/v1/query/6/",
            "id": 6,
            "domains": [
                {
                    "title": "domain title",
                    "id": 1,
                    "description": "domain description",
                }
            ],
            "tags": [
                {
                    "id": 1,
                    "name": "@tag_name",
                    "description": "tag description",
                    "ts_created": "2024-04-12T11:58:56.176079Z",
                    "url": "/tag/1/",
                    "ts_updated": "2024-04-12T12:03:40.884535Z",
                }
            ],
            "datasource": {
                "id": 1,
                "title": "OCF snowflake",
                "uri": "",
                "url": "/data/1/",
            },
            "ts_last_saved": "2024-04-12T12:03:40.704437Z",
            "has_unsaved_changes": False,
            "catalog_url": "/query/6/",
            "compose_url": "/compose/query/6/",
            "schedules": [],
        }

        query = Query.from_api_response(api_response)

        self.assertEqual(6, query.id)
        self.assertEqual("Test Query", query.title)
        self.assertIsInstance(query.ts_last_saved, datetime)
        self.assertEqual(1, len(query.domains))
        self.assertEqual("domain title", query.domains[0].title)
        self.assertEqual(1, len(query.tags))
        self.assertEqual("@tag_name", query.tags[0].name)
        self.assertIsInstance(query.tags[0].ts_created, datetime)
        self.assertEqual("OCF snowflake", query.datasource.title)

    def test_query_create_request_payload(self):
        create_request = QueryCreateRequest(
            datasource_id=1,
            content="SELECT 1",
            title="Query Title",
            description="Counts records",
            tag_names=["@zscaler"],
            domain_ids=[1, 2],
            author=QueryAuthor(email="author@example.com"),
            published=True,
        )

        payload = create_request.generate_api_post_payload()

        self.assertEqual(1, payload["datasource_id"])
        self.assertEqual("SELECT 1", payload["content"])
        self.assertTrue(payload["published"])
        self.assertEqual(["@zscaler"], payload["tag_names"])
        self.assertEqual({"email": "author@example.com"}, payload["author"])
        self.assertEqual([1, 2], payload["domain_ids"])

    def test_query_create_request_optional_fields_omitted(self):
        create_request = QueryCreateRequest(
            datasource_id=9,
            content="SELECT 1",
        )

        payload = create_request.generate_api_post_payload()

        self.assertNotIn("title", payload)
        self.assertNotIn("description", payload)
        self.assertNotIn("tag_names", payload)
        self.assertNotIn("domain_ids", payload)

    def test_query_create_request_requires_identifiers(self):
        create_request = QueryCreateRequest(
            datasource_id=1,
            content="SELECT 1",
            author=QueryAuthor(),
        )

        with self.assertRaises(InvalidPostBody):
            create_request.generate_api_post_payload()

    def test_query_create_request_requires_fields(self):
        with self.assertRaises(InvalidPostBody):
            QueryCreateRequest(datasource_id=None, content="SELECT 1").generate_api_post_payload()

        with self.assertRaises(InvalidPostBody):
            QueryCreateRequest(datasource_id=1, content=None).generate_api_post_payload()


if __name__ == "__main__":
    unittest.main()
