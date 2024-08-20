import requests_mock
from allie_sdk.methods.document import *



MOCK_USER = AlationDocument(
    access_token='test'
    , session=requests.session()
    , host='https://test.com'
)

def test_get_documents(requests_mock):

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
            "folder_ids": [
                14,
                165
            ],
            "document_hub_id": 1,
            "custom_fields": [
                {
                "field_id": 0,
                "title": "My text field",
                "value": "sample text"
                }
                , {
                    "field_id": 1,
                    "title": "My multi-select field",
                    "value": ["red", "orange", "green"]
                }
            ]
        }
    ]

    success_documents = [ Document.from_api_response(item) for item in document_api_response ]

    # Override the policy API call
    requests_mock.register_uri(
        method = 'GET'
        , url = '/integration/v2/document/'
        , json = document_api_response
        , status_code = 200
    )

    # --- TEST THE FUNCTION --- #
    documents = MOCK_USER.get_documents()

    assert success_documents == documents

def test_create_documents(requests_mock):

    # --- PREPARE THE TEST SETUP --- #

    # What does the response look like for the create document request?
    document_api_response = {
        'task': {
            'id': 23739
            , 'type': 'DOCUMENTS_BULK_CREATE'
            , 'state': 'QUEUED'
            , 'status': 'NA'
            , 'ts_started': '2023-12-08T10:08:35.974963Z'
            , 'links': []
        }    
    }

    # Override the document API call
    requests_mock.register_uri(
        method='POST'
        , url='/integration/v2/document/'
        , json=document_api_response
        , status_code=202
    )

    # What does the response look like for the Job?
    job_api_response = {
        'status': 'successful'
        , 'msg': 'Job finished in 0.242215 seconds at 2024-06-20 13:23:02.698215+00:00'
        , 'result': {
            'created_term_count': 2
            , 'created_terms': [
                {'id': 1325, 'title': 'My KPI 1'}
                , {'id': 1326, 'title': 'My KPI 2'}
            ]
        }
    }


    # Override the job API call
    # Note: The id in the job URL corresponds to the task id in document_api_response defined above
    requests_mock.register_uri(
        method = 'GET'
        , url = '/api/v1/bulk_metadata/job/?id=23739'
        , json = job_api_response
    )

    # --- TEST THE FUNCTION --- #
    create_documents_result = MOCK_USER.create_documents(
        [
            DocumentPostItem(
                title = "My KPI 1"
                , description = "This is the description for KPI 1"
                , template_id = 12
                , folder_ids = [ 6 ]
                , document_hub_id = 2
                , custom_fields = [
                    CustomFieldValueItem(
                        field_id = 1323
                        , value = [
                            CustomFieldDictValueItem(
                                otype = "glossary_term"
                                , oid = 159
                            )
                        ]
                    )
                ]
            )
            , DocumentPostItem(
                title = "My KPI 2"
                , description = "This is the description for KPI 2"
                , template_id = 12
                , folder_ids = [ 6 ]
                , document_hub_id = 2
                , custom_fields = [
                    CustomFieldValueItem(
                        field_id = 1323
                        , value = [
                            CustomFieldDictValueItem(
                                otype = "glossary_term"
                                , oid = 160
                            )
                        ]
                    )
                ]
            )
        ]
    )

    function_expected_result = [
        # MOCK_USER.JobDetails(
        #     status='successful'
        #     , msg='Job finished in 0.242215 seconds at 2024-06-20 13:23:02.698215+00:00'
        #     , result={
        #         'created_term_count': 2
        #         , 'created_terms': [
        #             {'id': 1325, 'title': 'My KPI 1'}
        #             , {'id': 1326, 'title': 'My KPI 2'}
        #         ]
        #     }
        # )
        JobDetailsDocumentPost(
            status='successful'
            , msg='Job finished in 0.242215 seconds at 2024-06-20 13:23:02.698215+00:00'
            , result=JobDetailsDocumentPostResult(
                created_term_count=2
                , created_terms=[
                    JobDetailsDocumentPostResultDetails(id=1325, title='My KPI 1')
                    , JobDetailsDocumentPostResultDetails(id=1326, title='My KPI 2')
                ]
            )
        )
    ]
    assert function_expected_result == create_documents_result

def test_update_documents(requests_mock):

    # --- PREPARE THE TEST SETUP --- #

    # What does the response look like for the update document request?
    document_api_response = {
        'task': {
            'id': 23739
            , 'type': 'DOCUMENTS_BULK_CREATE'
            , 'state': 'QUEUED'
            , 'status': 'NA'
            , 'ts_started': '2023-12-08T10:08:35.974963Z'
            , 'links': []
        }    
    }

    # Override the policy API call
    requests_mock.register_uri(
        method='PUT'
        , url='/integration/v2/document/'
        , json=document_api_response
        , status_code=202
    )

    # What does the response look like for the Job?
    job_api_response = {
        'msg': 'Job finished in 0.075303 seconds at 2024-06-21 13:16:42.261763+00:00'
        , 'result': {
            'updated_term_count': 2
            , 'updated_terms': [
                {'id': 1334}
                , {'id': 1335}
            ]
        }
        , 'status': 'successful'
    }


    # Override the job API call
    # Note: The id in the job URL corresponds to the task id in document_response defined above
    requests_mock.register_uri(
        method = 'GET'
        , url = '/api/v1/bulk_metadata/job/?id=23739'
        , json=job_api_response
    )

    # --- TEST THE FUNCTION --- #
    update_documents_result = MOCK_USER.update_documents(
        [
            DocumentPutItem(
                id = 1334
                , title = "My KPI 1"
                , description = "This is the description for KPI 1"
                , template_id = 12
                , folder_ids = [ 6 ]
                , document_hub_id = 2
                , custom_fields = [
                    CustomFieldValueItem(
                        field_id = 1323
                        , value = [
                            CustomFieldDictValueItem(
                                otype = "glossary_term"
                                , oid = 159
                            )
                        ]
                    )
                ]
            )
            , DocumentPutItem(
                id = 1335
                , title = "My KPI 2"
                , description = "This is the description for KPI 2"
                , template_id = 12
                , folder_ids = [ 6 ]
                , document_hub_id = 2
                , custom_fields = [
                    CustomFieldValueItem(
                        field_id = 1323
                        , value = [
                            CustomFieldDictValueItem(
                                otype = "glossary_term"
                                , oid = 160
                            )
                        ]
                    )
                ]
            )
        ]
    )

    function_expected_result = [
        JobDetailsDocumentPut(
            status='successful'
            , msg='Job finished in 0.075303 seconds at 2024-06-21 13:16:42.261763+00:00'
            , result=JobDetailsDocumentPutResult(
                updated_term_count=2
                , updated_terms=[
                    JobDetailsDocumentPutResultDetails(id=1334)
                    , JobDetailsDocumentPutResultDetails(id=1335)
                ]
            )
        )
    ]

    assert function_expected_result == update_documents_result

def test_delete_documents(requests_mock):

    # --- PREPARE THE TEST SETUP --- #

    # What does the response look like for the delete document request?
    document_api_response = {
            "deleted_document_count": 2,
            "deleted_document_ids": [
                1, 2
            ]
        }

    # Override the policy API call
    requests_mock.register_uri(
        method = 'DELETE'
        , url = '/integration/v2/document/'
        , json = document_api_response
        , status_code = 204
    )


    # --- TEST THE FUNCTION --- #
    delete_document_result = MOCK_USER.delete_documents(
        [
            Document(
                id = 1
            )
            , Document(
                id = 2
            )
        ]
    )

    function_expected_result = JobDetailsDocumentDelete(
            deleted_document_count = 2
            , deleted_document_ids = [
                1, 2
            ]
        )
    assert function_expected_result == delete_document_result