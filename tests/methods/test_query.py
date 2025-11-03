"""Tests for the Alation Query methods."""

import unittest
from datetime import datetime
import requests
import requests_mock

from allie_sdk.methods.query import AlationQuery
from allie_sdk.models.query_model import *
from allie_sdk.models.job_model import *
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

        payload = QueryItem(
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

        result = self.query_methods.create_query(payload)

        expected_result = JobDetails(
            status='successful'
            , msg=''
            , result=Query(
                datasource_id=1
                , autosave_content='SELECT count(*) FROM users;'
                , content='SELECT count(*) FROM users;'
                , title='Top 10 Users'
                , saved=True
                , published=True
                , description='Counts the number of users and gives the top 10 users.'
                , url='/integration/v1/query/6/'
                , id=6
                , domains=[
                    QueryDomain(title='domain title', id=1, description='domain description')
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
        )

        assert  expected_result == result


    @requests_mock.Mocker()
    def test_get_query_sql_success(self, mock_requests):
        mock_requests.register_uri(
            method="GET",
            url="/integration/v1/query/6/sql/",
            text="SELECT count(*) FROM users;",
            status_code=200,
        )

        sql_text = self.query_methods.get_query_sql(query_id=6)

        self.assertEqual("SELECT count(*) FROM users;", sql_text)

    @requests_mock.Mocker()
    def test_get_query_success(self, mock_requests):

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

        mock_requests.register_uri(
            method="GET",
            url="/integration/v1/query/6/",
            json=api_response,
            status_code=200,
        )

        query = self.query_methods.get_query(query_id=6)

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

    @requests_mock.Mocker()
    def test_get_queries_success(self, mock_requests):
        api_response = [

            {
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
        ]

        mock_requests.register_uri(
            method="GET",
            url="/integration/v1/query/?datasource_id=1",
            json=api_response,
            status_code=200,
        )

        query = self.query_methods.get_queries(query_params=QueryParams(
            datasource_id=1
        ))

        expected_result = [
            Query(
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
        ]

        assert expected_result == query

