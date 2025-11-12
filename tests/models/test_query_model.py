"""Tests for the Query data models."""

import unittest
from datetime import datetime

from allie_sdk.models.query_model import *
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

        expected_result = Query(
            datasource_id=1
            , autosave_content='SELECT 1'
            , content='SELECT 1'
            , title='Test Query'
            , saved=True
            , published=False
            , description='Description'
            , url='/integration/v1/query/6/'
            , id=6
            , domains=[
                QueryDomain(
                    title='domain title'
                    , id=1
                    , description='domain description'
                )
            ]
            , tags=[
                QueryTag(
                    id=1
                    , name='@tag_name'
                    , description='tag description'
                    , ts_created=datetime(2024, 4, 12, 11, 58, 56, 176079)
                    , url='/tag/1/'
                    , ts_updated=datetime(2024, 4, 12, 12, 3, 40, 884535)
                )
            ]
            , datasource=QueryDatasource(
                id=1
                , title='OCF snowflake'
                , uri=''
                , url='/data/1/'
            )
            , ts_last_saved=datetime(2024, 4, 12, 12, 3, 40, 704437)
            , has_unsaved_changes=False
            , catalog_url='/query/6/'
            , compose_url='/compose/query/6/'
            , schedules=[]
        )
        assert expected_result == query

    def test_query_create_request_payload(self):
        create_request = QueryItem(
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

        expected_result = {
            'author': {'email': 'author@example.com'}
            , 'content': 'SELECT 1'
            , 'datasource_id': 1
            , 'description': 'Counts records'
            , 'domain_ids': [1, 2]
            , 'published': True
            , 'saved': True
            , 'tag_names': ['@zscaler']
            , 'title': 'Query Title'
        }

        assert expected_result == payload

    def test_query_create_request_optional_fields_omitted(self):
        create_request = QueryItem(
            datasource_id=9,
            content="SELECT 1",
        )

        payload = create_request.generate_api_post_payload()

        self.assertNotIn("title", payload)
        self.assertNotIn("description", payload)
        self.assertNotIn("tag_names", payload)
        self.assertNotIn("domain_ids", payload)

    def test_query_create_request_requires_identifiers(self):
        create_request = QueryItem(
            datasource_id=1,
            content="SELECT 1",
            author=QueryAuthor(),
        )

        with self.assertRaises(InvalidPostBody):
            create_request.generate_api_post_payload()

    def test_query_create_request_requires_fields(self):
        with self.assertRaises(InvalidPostBody):
            QueryItem(datasource_id=None, content="SELECT 1").generate_api_post_payload()

        with self.assertRaises(InvalidPostBody):
            QueryItem(datasource_id=1, content=None).generate_api_post_payload()

