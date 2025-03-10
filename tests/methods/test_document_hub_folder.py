"""Test the Alation REST API Document Hub Folder Methods."""

import requests_mock
import unittest
from allie_sdk.methods.document_hub_folder import *


class TestDocumentHubFolder(unittest.TestCase):

    def setUp(self):
        self.mock_user = AlationDocumentHubFolder(
            access_token='test',
            session=requests.session(),
            host='https://test.com'
        )

    @requests_mock.Mocker()
    def test_get_document_hub_folders(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the document request?
        document_hub_folder_api_response = [
            {
                "id": 1,
                "deleted": False,
                "ts_deleted": "2022-07-05T15:09:40.421916Z",
                "ts_created": "2022-07-05T15:09:40.421916Z",
                "ts_updated": "2022-07-05T15:09:40.421916Z",
                "title": "Sales",
                "description": "Relevant data and articles for Sales Analytics",
                "template_id": 47,
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

        success_document_hub_folders = [DocumentHubFolder.from_api_response(item) for item in document_hub_folder_api_response]

        # Override the document hub API call
        requests_mock.register_uri(
            method='GET',
            url='/integration/v2/folder/',
            json=document_hub_folder_api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        document_hub_folders = self.mock_user.get_document_hub_folders()

        self.assertEqual(success_document_hub_folders, document_hub_folders)

    @requests_mock.Mocker()
    def test_create_document_hub_folders(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the create document request?
        document_hub_folder_api_response = {
            "job_id": 27807
        }

        # Override the document API call
        requests_mock.register_uri(
            method='POST',
            url='/integration/v2/folder/',
            json=document_hub_folder_api_response,
            status_code=202
        )

        # What does the response look like for the Job?
        job_api_response = {
            'status': 'successful',
            'msg': 'Job finished in 0.242215 seconds at 2024-06-20 13:23:02.698215+00:00',
            'result': {
                'created_folder_count': 2,
                'created_folders': [
                    {'id': 10, 'title': 'My Doc Hub Folder 1'},
                    {'id': 11, 'title': 'My Doc Hub Folder 2'}
                ]
            }
        }

        # Override the job API call
        # Note: The id in the job URL corresponds to the task id in document_hub_folder_api_response defined above
        requests_mock.register_uri(
            method='GET',
            url='/api/v1/bulk_metadata/job/?id=27807',
            json=job_api_response
        )

        # --- TEST THE FUNCTION --- #
        create_document_hub_folders_result = self.mock_user.create_document_hub_folders(
            [
                DocumentHubFolderPostItem(
                    title="My Doc Hub Folder 1",
                    description="This is the description for Doc Hub Folder 1",
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
                DocumentHubFolderPostItem(
                    title="My Doc Hub Folder 2",
                    description="This is the description for Doc Hub Folder 2",
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
            JobDetailsDocumentHubFolderPost(
                status='successful',
                msg='Job finished in 0.242215 seconds at 2024-06-20 13:23:02.698215+00:00',
                result=JobDetailsDocumentHubFolderPostResult(
                    created_folder_count=2,
                    created_folders=[
                        JobDetailsDocumentHubFolderPostResultCreatedFolder(
                            id=10,
                            title="My Doc Hub Folder 1"
                        ),
                        JobDetailsDocumentHubFolderPostResultCreatedFolder(
                            id=11,
                            title="My Doc Hub Folder 2"
                        )
                    ]
                )
            )
        ]
        self.assertEqual(function_expected_result, create_document_hub_folders_result)

    @requests_mock.Mocker()
    def test_create_document_hub_folders_fail(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #
        
        # What does the response look like for the failed document hub folder request?
        error_response = {
            "detail": "Bad request: validation error",
            "errors": ["title is required"],
            "code": "400400"
        }
        
        # Override the document hub folder API call to return an error
        requests_mock.register_uri(
            method='POST',
            url='/integration/v2/folder/',
            json=error_response,
            status_code=400
        )
        
        # --- TEST THE FUNCTION --- #
        # Test with a folder that will trigger the API error - should raise an HTTPError
        with self.assertRaises(requests.exceptions.HTTPError):
            self.mock_user.create_document_hub_folders(
                [
                    DocumentHubFolderPostItem(
                        # Include required fields to pass local validation
                        title="Test folder with validation error",
                        description="This folder will trigger a 400 error on the API",
                        document_hub_id=2
                    )
                ]
            )

    @requests_mock.Mocker()
    def test_update_document_hub_folders(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the update document request?
        document_hub_folder_api_response = {
            "job_id": 27811
        }

        # Override the policy API call
        requests_mock.register_uri(
            method='PUT',
            url='/integration/v2/folder/',
            json=document_hub_folder_api_response,
            status_code=202
        )

        # What does the response look like for the Job?
        job_api_response = {
            'msg': 'Job finished in 0.075303 seconds at 2024-06-21 13:16:42.261763+00:00',
            'result': {
                'updated_folder_count': 2,
                'updated_folders': [
                    {'id': 10, 'title': 'My Doc Hub Folder 1'},
                    {'id': 11, 'title': 'My Doc Hub Folder 2'}
                ]
            },
            'status': 'successful'
        }

        # Override the job API call
        # Note: The id in the job URL corresponds to the task id in document_hub_folder_response defined above
        requests_mock.register_uri(
            method='GET',
            url='/api/v1/bulk_metadata/job/?id=27811',
            json=job_api_response
        )

        # --- TEST THE FUNCTION --- #
        update_document_hub_folders_result = self.mock_user.update_document_hub_folders(
            [
                DocumentHubFolderPutItem(
                    id=10,
                    title="My Doc Hub Folder 1",
                    description="This is the description for Doc Hub Folder 1",
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
                DocumentHubFolderPutItem(
                    id=11,
                    title="My Doc Hub Folder 2",
                    description="This is the description for Doc Hub Folder 2",
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
            JobDetailsDocumentHubFolderPut(
                status='successful',
                msg='Job finished in 0.075303 seconds at 2024-06-21 13:16:42.261763+00:00',
                result=JobDetailsDocumentHubFolderPutResult(
                    updated_folder_count=2,
                    updated_folders=[
                        JobDetailsDocumentHubFolderPutResultUpdatedFolder(
                            id=10,
                            title="My Doc Hub Folder 1"
                        ),
                        JobDetailsDocumentHubFolderPutResultUpdatedFolder(
                            id=11,
                            title="My Doc Hub Folder 2"
                        )
                    ]
                )
            )
        ]

        self.assertEqual(function_expected_result, update_document_hub_folders_result)

    @requests_mock.Mocker()
    def test_update_document_hub_folders_fail(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #
        
        # What does the response look like for the failed document hub folder update request?
        error_response = {
            "detail": "Bad request: validation error",
            "errors": ["folder not found"],
            "code": "400400"
        }
        
        # Override the document hub folder API call to return an error
        requests_mock.register_uri(
            method='PUT',
            url='/integration/v2/folder/',
            json=error_response,
            status_code=400
        )
        
        # --- TEST THE FUNCTION --- #
        # Update a folder that will trigger an error on the server - should raise an HTTPError
        with self.assertRaises(requests.exceptions.HTTPError):
            self.mock_user.update_document_hub_folders(
                [
                    DocumentHubFolderPutItem(
                        id=9999, # Folder that doesn't exist
                        title="Folder with non-existent ID",
                        description="This folder will trigger a 400 error on the API",
                        document_hub_id=2
                    )
                ]
            )

    @requests_mock.Mocker()
    def test_delete_document_hub_folders(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the delete document request?
        document_hub_folder_api_response = {
            "deleted_folder_count": 2,
            "deleted_folder_ids": [
                1, 2
            ]
        }

        # Override the document API call
        requests_mock.register_uri(
            method='DELETE',
            url='/integration/v2/folder/',
            json=document_hub_folder_api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        delete_document_hub_folder_result = self.mock_user.delete_document_hub_folders(
            [
                DocumentHubFolder(
                    id=1
                ),
                DocumentHubFolder(
                    id=2
                )
            ]
        )

        function_expected_result = JobDetailsDocumentHubFolderDelete(
            status="successful",
            msg="",
            result=JobDetailsDocumentHubFolderDeleteResult(
                deleted_folder_count=2,
                deleted_folder_ids=[
                    1, 2
                ]
            )
        )
        self.assertEqual(function_expected_result, delete_document_hub_folder_result)