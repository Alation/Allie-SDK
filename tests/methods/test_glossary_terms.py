"""Test the Alation REST API Custom Field Methods."""

import requests_mock
import unittest
from allie_sdk.methods.glossary_term import *

MOCK_GLOSSARY_TERM = AlationGlossaryTerm(
    access_token='test', session=requests.session(), host='https://test.com'
)


class TestGlossaryTerm(unittest.TestCase):

    @requests_mock.Mocker()
    def test_success_get_glossary_terms(self, m):

        mock_params = GlossaryTermParams()
        mock_params.search = "Test"
        success_response = [
            {
                "id": 1663,
                "title": "Taha's Test Term",
                "description": "<p>I am demoing object creation. Feel free to discard.</p>",
                "ts_created": "2023-04-13T20:08:52.439026Z",
                "ts_updated": "2023-04-13T20:09:42.077421Z",
                "ts_deleted": None,
                "deleted": False,
                "template_id": 43,
                "glossary_ids": [],
                "custom_fields": [
                    {"value": "New", "field_id": 5, "field_name": "Status"},
                    {"value": [{"otype": "user", "oid": 22}], "field_id": 8, "field_name": "Steward"}
                ]
            }
        ]
        mock_terms = [GlossaryTerm.from_api_response(item) for item in success_response]
        m.register_uri('GET', '/integration/v2/term/', json=success_response)
        terms = MOCK_GLOSSARY_TERM.get_glossary_terms(mock_params)

        self.assertEqual(mock_terms, terms)

    @requests_mock.Mocker()
    def test_failed_get_glossary_terms(self, m):

        failed_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }
        m.register_uri('GET', '/integration/v2/term/', json=failed_response, status_code=403)
        
        # The method should now raise an HTTPError for non-200 status codes
        with self.assertRaises(requests.exceptions.HTTPError):
            MOCK_GLOSSARY_TERM.get_glossary_terms()

    @requests_mock.Mocker()
    def test_success_post_glossary_terms(self, m):

        mock_term_1 = GlossaryTermItem()
        mock_term_1.title = 'Testing'
        mock_term_1.description = 'Testing the API'

        mock_term_2 = GlossaryTermItem()
        mock_term_2.title = 'Testing #2'
        mock_term_2.description = 'Testing the API Part 2'

        mock_term_list = [mock_term_1, mock_term_2]

        async_response = {
            "job_id": 1
        }
        job_response = {
            "status": "successful",
            "msg": "Job finished in 0.110648 seconds at 2023-11-28 05:15:50.976697+00:00",
            "result": {
                "created_term_count": 2,
                "created_terms": [
                    {"id": 1, "title": "Testing"},
                    {"id": 2, "title": "Testing #2"}
                ]
            }
        }

        m.register_uri('POST', '/integration/v2/term/', json=async_response)
        m.register_uri('GET', '/api/v1/bulk_metadata/job/?id=1', json=job_response)

        async_result = MOCK_GLOSSARY_TERM.post_glossary_terms(mock_term_list)
        input_transformed = [JobDetailsDocumentPost(**job_response)]
        # self.assertTrue(async_result)
        self.assertEqual(input_transformed, async_result)

    @requests_mock.Mocker()
    def test_failed_post_glossary_terms(self, m):

        mock_term_1 = GlossaryTermItem()
        mock_term_1.title = 'Testing'
        mock_term_1.description = 'Testing the API'
        mock_term_list = [mock_term_1]

        failed_response = {
            "job_id": None,
            "invalid_terms": [
                {
                    "index": 0,
                    "errors": [
                        {
                            "title": [
                                "This field is required."
                            ]
                        }
                    ],
                    "term": {
                        "title": "Testing",
                        "description": "Testing the API"
                    }
                }
            ]
        }
        m.register_uri('POST', '/integration/v2/term/', json=failed_response, status_code=400)
        
        # Should raise HTTPError with 400 status
        with self.assertRaises(requests.exceptions.HTTPError):
            MOCK_GLOSSARY_TERM.post_glossary_terms(mock_term_list)

    @requests_mock.Mocker()
    def test_success_put_glossary_terms(self, m):

        mock_term_1 = GlossaryTermItem()
        mock_term_1.id = 1
        mock_term_1.title = "Updated Title"
        mock_term_list = [mock_term_1]

        async_response = {
            "job_id": 1
        }
        job_response = {
            "status": "successful",
            "msg": "Job finished in 1.18204 seconds at 2023-11-28 05:24:03.031535+00:00",
            "result": {
                "updated_term_count": 1,
                "updated_terms": [
                    {
                        "id": 1,
                        "title": "Updated Title"
                    }
                ]
            }
        }

        m.register_uri('PUT', '/integration/v2/term/', json=async_response)
        m.register_uri('GET', '/api/v1/bulk_metadata/job/?id=1', json=job_response)
        async_result = MOCK_GLOSSARY_TERM.put_glossary_terms(mock_term_list)

        input_transformed = [JobDetailsDocumentPut(**job_response)]
        # self.assertTrue(async_result)
        self.assertEqual(input_transformed, async_result)

    @requests_mock.Mocker()
    def test_failed_put_glossary_terms(self, m):

        mock_term_1 = GlossaryTermItem()
        mock_term_1.id = 1
        mock_term_1.title = "Updated Title"
        mock_term_list = [mock_term_1]

        failed_response = {
            "job_id": None,
            "invalid_terms": [
                {
                    "index": 0,
                    "errors": [
                        {
                            "id": [
                                "This field is required."
                            ]
                        }
                    ],
                    "term": {
                        "title": "Updated Title"
                    }
                }
            ]
        }
        m.register_uri('PUT', '/integration/v2/term/', json=failed_response, status_code=400)
        
        # Should raise HTTPError with 400 status
        with self.assertRaises(requests.exceptions.HTTPError):
            MOCK_GLOSSARY_TERM.put_glossary_terms(mock_term_list)

    @requests_mock.Mocker()
    def test_success_delete_glossary_terms(self, m):

        mock_term_1 = GlossaryTerm()
        mock_term_1.id = 1
        mock_term_list = [mock_term_1]

        success_response = {
            "deleted_term_ids": [
                1
            ],
            "deleted_term_count": 1
        }

        m.register_uri('DELETE', '/integration/v2/term/', json=success_response)
        delete_result = MOCK_GLOSSARY_TERM.delete_glossary_terms(mock_term_list)

        expected_result = JobDetailsTermDelete(
            status = 'successful'
            , msg = ''
            , result = JobDetailsTermDeleteResult(
                deleted_term_ids = [1]
                , deleted_term_count = 1
            )
        )

        self.assertEqual(expected_result, delete_result)

    @requests_mock.Mocker()
    def test_failed_delete_glossary_terms(self, m):

        mock_term_1 = GlossaryTerm()
        mock_term_1.id = 1
        mock_term_list = [mock_term_1]

        failed_response = {
            "id": [
                "Expected a list of items but got type \"int\"."
            ],
            "detail": {
                "id": [
                    "Expected a list of items but got type \"int\"."
                ]
            },
            "code": "400000"
        }

        m.register_uri('DELETE', '/integration/v2/term/', json=failed_response, status_code=400)
        async_response = MOCK_GLOSSARY_TERM.delete_glossary_terms(mock_term_list)

        expected_response = JobDetailsTermDelete(
            status='failed'
            , msg=None
            , result={
                'id': ['Expected a list of items but got type "int".']
                , 'detail': {'id': ['Expected a list of items but got type "int".']}
                , 'code': '400000'
            }
        )

        self.assertEqual(expected_response, async_response)


if __name__ == '__main__':
    unittest.main()
