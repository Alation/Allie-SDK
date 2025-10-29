"""Tests for the Alation Query methods."""

import unittest

import requests
import requests_mock

from allie_sdk.methods.query import AlationQuery
from allie_sdk.models.query_model import QueryAuthor, QueryCreateRequest
from allie_sdk.core.custom_exceptions import InvalidPostBody


class TestQueryMethods(unittest.TestCase):
    def setUp(self):
        self.query_methods = AlationQuery(
            access_token="test",
            session=requests.session(),
            host="https://test.com",
        )

    @requests_mock.Mocker()
    def test_create_query_success(self, mock_requests):
        api_response = {
            "datasource_id": 1,
            "autosave_content": "SELECT count(*) FROM users;",
            "content": "SELECT count(*) FROM users;",
            "title": "Top 10 Users",
            "saved": True,
            "published": True,
            "description": "Counts the number of users and gives the top 10 users.",
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

        mock_requests.register_uri(
            method="POST",
            url="/integration/v1/query/",
            json=api_response,
            status_code=201,
        )

        payload = QueryCreateRequest(
            datasource_id=1,
            content="SELECT count(*) FROM users;",
            saved=True,
            published=True,
            title="Top 10 Users",
            description="Counts the number of users and gives the top 10 users.",
            tag_names=["@tag_name"],
            domain_ids=[1],
            author=QueryAuthor(id=1),
        )

        query = self.query_methods.create_query(payload)

        self.assertEqual(6, query.id)
        self.assertEqual("Top 10 Users", query.title)
        self.assertEqual("/query/6/", query.catalog_url)

        last_request = mock_requests.last_request
        self.assertIsNotNone(last_request)
        self.assertEqual(
            {
                "datasource_id": 1,
                "content": "SELECT count(*) FROM users;",
                "saved": True,
                "published": True,
                "title": "Top 10 Users",
                "description": "Counts the number of users and gives the top 10 users.",
                "tag_names": ["@tag_name"],
                "domain_ids": [1],
                "author": {"id": 1},
            },
            last_request.json(),
        )

    @requests_mock.Mocker()
    def test_create_query_http_error(self, mock_requests):
        mock_requests.register_uri(
            method="POST",
            url="/integration/v1/query/",
            json={"detail": "Unauthorized"},
            status_code=403,
        )

        payload = QueryCreateRequest(datasource_id=1, content="SELECT 1")

        with self.assertRaises(requests.exceptions.HTTPError):
            self.query_methods.create_query(payload)

    def test_create_query_requires_payload(self):
        with self.assertRaises(InvalidPostBody):
            self.query_methods.create_query(None)

    @requests_mock.Mocker()
    def test_get_query_sql_success(self, mock_requests):
        mock_requests.register_uri(
            method="GET",
            url="/integration/v1/query/6/sql/",
            text="SELECT count(*) FROM users;",
            status_code=200,
        )

        sql_text = self.query_methods.get_query_sql(6)

        self.assertEqual("SELECT count(*) FROM users;", sql_text)

    def test_get_query_sql_requires_id(self):
        with self.assertRaises(InvalidPostBody):
            self.query_methods.get_query_sql(None)


if __name__ == "__main__":
    unittest.main()
