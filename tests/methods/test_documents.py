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
                "value": "sample text"
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

    # Override the policy API call
    requests_mock.register_uri(
        method='POST'
        , url='/integration/v2/document/'
        , json=document_api_response
        , status_code=202
    )

    # What does the response look like for the Job?
    job_api_response = {
        'status': 'successful'
        , 'msg': 'Job finished in 2.171085 seconds at 2023-12-08 17:20:53.735123+00:00'
        , 'result': [
            'Successfully processed 2 items (index range: [0, 1])'
            , 'All total 1 batches with a limit of 250 items attempted. [Succeeded: 2, Failed: 0, Total: 2]'
        ]
    }
    
    """
    OPEN/CONCERN: Here we don't get any details about the created documents back.
    With terms in example the job response includes details about the created terms within
    the result section.
    With documents there's no point really testing this bit of code since we don't really
    have something proper to validate against.
    """

    # Override the job API call
    # Note: The id in the job URL correspondes to the task id in policy_api_response defined above
    requests_mock.register_uri(
        method = 'GET'
        , url = '/api/v1/bulk_metadata/job/?id=23739'
        , json=job_api_response
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

    """
    OPEN/CONCERN: Here we don't get any details about the created documents back.
    With terms in example the job response includes details about the created terms within
    the result section.
    With documents there's no point really testing this bit of code since we don't really
    have something proper to validate against.
    """

    # OPEN: See concern mentioned further up
    function_expected_result = True
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
        'status': 'successful'
        , 'msg': 'Job finished in 2.171085 seconds at 2023-12-08 17:20:53.735123+00:00'
        , 'result': [
            'Successfully processed 2 items (index range: [0, 1])'
            , 'All total 1 batches with a limit of 250 items attempted. [Succeeded: 2, Failed: 0, Total: 2]'
        ]
    }
    
    """
    OPEN/CONCERN: Here we don't get any details about the created documents back.
    With terms in example the job response includes details about the created terms within
    the result section.
    With documents there's no point really testing this bit of code since we don't really
    have something proper to validate against.
    """

    # Override the job API call
    # Note: The id in the job URL correspondes to the task id in policy_api_response defined above
    requests_mock.register_uri(
        method = 'GET'
        , url = '/api/v1/bulk_metadata/job/?id=23739'
        , json=job_api_response
    )

    # --- TEST THE FUNCTION --- #
    create_documents_result = MOCK_USER.update_documents(
        [
            DocumentPutItem(
                id = 221
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
                id = 222
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

    """
    OPEN/CONCERN: Here we don't get any details about the created documents back.
    With terms in example the job response includes details about the created terms within
    the result section.
    With documents there's no point really testing this bit of code since we don't really
    have something proper to validate against.
    """

    # OPEN: See concern mentioned further up
    function_expected_result = True
    assert function_expected_result == create_documents_result

def test_delete_documents(requests_mock):

    # --- PREPARE THE TEST SETUP --- #

    # What does the response look like for the delete document request?
    document_api_response = ''

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

    # OPEN: See concern mentioned further up
    function_expected_result = True
    assert function_expected_result == delete_document_result