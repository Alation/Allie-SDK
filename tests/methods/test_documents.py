"""Test the Alation REST API Document Methods."""

import requests_mock
import unittest
from allie_sdk.methods.document import *


class TestDocument(unittest.TestCase):

    def setUp(self):
        self.mock_user = AlationDocument(
            access_token='test',
            session=requests.session(),
            host='https://test.com'
        )

    @requests_mock.Mocker()
    def test_get_documents(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the document request?
        document_api_response = [
            {
                "id": 1,
                "deleted": False,
                "ts_deleted": "2022-07-05T15:09:40.421916Z",
                # "is_public": True,  => was removed Apr 2024
                "ts_created": "2022-07-05T15:09:40.421916Z",
                "ts_updated": "2022-07-05T15:09:40.421916Z",
                # "otype": "glossary_term",  => was removed Apr 2024
                "title": "Sales",
                "description": "Relevant data and articles for Sales Analytics",
                "template_id": 47,
                "parent_folder_id": 1,
                "parent_document_id": 99,
                "nav_link_folder_ids": [
                    14,
                    165
                ],
                "document_hub_id": 1,
                "custom_fields": [
                    {
                    "field_id": 0,
                    "title": "My text field",
                    "value": "sample text"
                    },
                    {
                        "field_id": 1,
                        "title": "My multi-select field",
                        "value": ["red", "orange", "green"]
                    }
                ]
            }
        ]

        success_documents = [Document.from_api_response(item) for item in document_api_response]

        # Override the document API call
        requests_mock.register_uri(
            method='GET',
            url='/integration/v2/document/',
            json=document_api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        documents = self.mock_user.get_documents()

        self.assertEqual(success_documents, documents)
        
    @requests_mock.Mocker()
    def test_empty_get_documents(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #
        empty_response = []

        # Override the document API call
        requests_mock.register_uri(
            method='GET',
            url='/integration/v2/document/',
            json=empty_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        documents = self.mock_user.get_documents()

        self.assertEqual([], documents)
        
    @requests_mock.Mocker()
    def test_failed_get_documents(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #
        error_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }

        # Override the document API call with error response
        requests_mock.register_uri(
            method='GET',
            url='/integration/v2/document/',
            json=error_response,
            status_code=403
        )

        # --- TEST THE FUNCTION --- #
        with self.assertRaises(requests.exceptions.HTTPError) as context:
            self.mock_user.get_documents()
            
        self.assertEqual(context.exception.response.status_code, 403)

    @requests_mock.Mocker()
    def test_create_documents(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the create document request?
        document_api_response = {
            "job_id": 27809
        }

        # Override the document API call
        requests_mock.register_uri(
            method='POST',
            url='/integration/v2/document/',
            json=document_api_response,
            status_code=202
        )

        # What does the response look like for the Job?
        job_api_response = {
            'status': 'successful',
            'msg': 'Job finished in 0.242215 seconds at 2024-06-20 13:23:02.698215+00:00',
            'result': {
                'created_term_count': 2,
                'created_terms': [
                    {'id': 1325, 'title': 'My KPI 1'},
                    {'id': 1326, 'title': 'My KPI 2'}
                ]
            }
        }

        # Override the job API call
        # Note: The id in the job URL corresponds to the task id in document_api_response defined above
        requests_mock.register_uri(
            method='GET',
            url='/api/v1/bulk_metadata/job/?id=27809',
            json=job_api_response
        )

        # --- TEST THE FUNCTION --- #
        create_documents_result = self.mock_user.create_documents(
            [
                DocumentPostItem(
                    title="My KPI 1",
                    description="This is the description for KPI 1",
                    template_id=12,
                    parent_folder_id=1,
                    nav_link_folder_ids=[6],
                    document_hub_id=2,
                    custom_fields=[
                        CustomFieldValueItem(
                            field_id=1323,
                            value=[
                                CustomFieldDictValueItem(
                                    otype="glossary_term",
                                    oid=159
                                )
                            ]
                        )
                    ]
                ),
                DocumentPostItem(
                    title="My KPI 2",
                    description="This is the description for KPI 2",
                    template_id=12,
                    parent_folder_id=1,
                    nav_link_folder_ids=[6],
                    document_hub_id=2,
                    custom_fields=[
                        CustomFieldValueItem(
                            field_id=1323,
                            value=[
                                CustomFieldDictValueItem(
                                    otype="glossary_term",
                                    oid=160
                                )
                            ]
                        )
                    ]
                )
            ]
        )

        function_expected_result = [
            JobDetailsDocumentPost(
                status='successful',
                msg='Job finished in 0.242215 seconds at 2024-06-20 13:23:02.698215+00:00',
                result=JobDetailsDocumentPostResult(
                    created_term_count=2,
                    created_terms=[
                        JobDetailsDocumentPostResultDetails(id=1325, title='My KPI 1'),
                        JobDetailsDocumentPostResultDetails(id=1326, title='My KPI 2')
                    ]
                )
            )
        ]
        self.assertEqual(function_expected_result, create_documents_result)

    @requests_mock.Mocker()
    def test_create_documents_fail(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #
        
        # What does the response look like for the failed document request?
        error_response = {
            "detail": "Bad request: validation error",
            "errors": ["title is required"],
            "code": "400400"
        }
        
        # Override the document API call to return an error
        requests_mock.register_uri(
            method='POST',
            url='/integration/v2/document/',
            json=error_response,
            status_code=400
        )
        
        # --- TEST THE FUNCTION --- #
        # Test with a document that will trigger the API error - should raise an HTTPError
        with self.assertRaises(requests.exceptions.HTTPError):
            self.mock_user.create_documents(
                [
                    DocumentPostItem(
                        # Include all required fields to avoid the validation error in our code
                        title="Test document with validation error",
                        description="This document will trigger a 400 error on the API",
                        template_id=12,
                        parent_folder_id=1,
                        nav_link_folder_ids=[6],
                        document_hub_id=2
                    )
                ]
            )

    @requests_mock.Mocker()
    def test_update_documents(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the update document request?
        document_api_response = {
            "job_id": 27811
        }

        # Override the document API call
        requests_mock.register_uri(
            method='PUT',
            url='/integration/v2/document/',
            json=document_api_response,
            status_code=202
        )

        # What does the response look like for the Job?
        job_api_response = {
            'msg': 'Job finished in 0.075303 seconds at 2024-06-21 13:16:42.261763+00:00',
            'result': {
                'updated_term_count': 2,
                'updated_terms': [
                    {'id': 1334},
                    {'id': 1335}
                ]
            },
            'status': 'successful'
        }

        # Override the job API call
        # Note: The id in the job URL corresponds to the task id in document_response defined above
        requests_mock.register_uri(
            method='GET',
            url='/api/v1/bulk_metadata/job/?id=27811',
            json=job_api_response
        )

        # --- TEST THE FUNCTION --- #
        update_documents_result = self.mock_user.update_documents(
            [
                DocumentPutItem(
                    id=1334,
                    title="My KPI 1",
                    description="This is the description for KPI 1",
                    template_id=12,
                    parent_folder_id=1,
                    nav_link_folder_ids=[6],
                    document_hub_id=2,
                    custom_fields=[
                        CustomFieldValueItem(
                            field_id=1323,
                            value=[
                                CustomFieldDictValueItem(
                                    otype="glossary_term",
                                    oid=159
                                )
                            ]
                        )
                    ]
                ),
                DocumentPutItem(
                    id=1335,
                    title="My KPI 2",
                    description="This is the description for KPI 2",
                    template_id=12,
                    parent_folder_id=1,
                    nav_link_folder_ids=[6],
                    document_hub_id=2,
                    custom_fields=[
                        CustomFieldValueItem(
                            field_id=1323,
                            value=[
                                CustomFieldDictValueItem(
                                    otype="glossary_term",
                                    oid=160
                                )
                            ]
                        )
                    ]
                )
            ]
        )

        function_expected_result = [
            JobDetailsDocumentPut(
                status='successful',
                msg='Job finished in 0.075303 seconds at 2024-06-21 13:16:42.261763+00:00',
                result=JobDetailsDocumentPutResult(
                    updated_term_count=2,
                    updated_terms=[
                        JobDetailsDocumentPutResultDetails(id=1334),
                        JobDetailsDocumentPutResultDetails(id=1335)
                    ]
                )
            )
        ]

        self.assertEqual(function_expected_result, update_documents_result)

    @requests_mock.Mocker()
    def test_update_documents_fail(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #
        
        # What does the response look like for the failed document update request?
        error_response = {
            "detail": "Bad request: validation error",
            "errors": ["document not found"],
            "code": "400400"
        }
        
        # Override the document API call to return an error
        requests_mock.register_uri(
            method='PUT',
            url='/integration/v2/document/',
            json=error_response,
            status_code=400
        )
        
        # --- TEST THE FUNCTION --- #
        # Update a document that will trigger an error on the server - should raise an HTTPError
        with self.assertRaises(requests.exceptions.HTTPError):
            self.mock_user.update_documents(
                [
                    DocumentPutItem(
                        id=9999, # Document that doesn't exist
                        title="My KPI with non-existent ID",
                        description="This is a description for a document that doesn't exist",
                        template_id=12,
                        parent_folder_id=1,
                        nav_link_folder_ids=[6],
                        document_hub_id=2
                    )
                ]
            )

    @requests_mock.Mocker()
    def test_delete_documents(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the delete document request?
        document_api_response = {
            "deleted_document_count": 2,
            "deleted_document_ids": [
                1, 2
            ]
        }

        # Override the document API call
        requests_mock.register_uri(
            method='DELETE',
            url='/integration/v2/document/',
            json=document_api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        delete_document_result = self.mock_user.delete_documents(
            [
                Document(
                    id=1
                ),
                Document(
                    id=2
                )
            ]
        )

        function_expected_result = JobDetailsDocumentDelete(
            status="successful",
            msg="",
            result=JobDetailsDocumentDeleteResult(
                deleted_document_count=2,
                deleted_document_ids=[
                    1, 2
                ]
            )
        )
        self.assertEqual(function_expected_result, delete_document_result)
        
    @requests_mock.Mocker()
    def test_failed_delete_documents(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #
        error_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }

        # Override the document API call with error response
        requests_mock.register_uri(
            method='DELETE',
            url='/integration/v2/document/',
            json=error_response,
            status_code=403
        )

        # --- TEST THE FUNCTION --- #
        with self.assertRaises(requests.exceptions.HTTPError) as context:
            self.mock_user.delete_documents([Document(id=1), Document(id=2)])
            
        self.assertEqual(context.exception.response.status_code, 403)