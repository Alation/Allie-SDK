"""Test the Alation REST API Custom Field Methods."""

import requests_mock
import pytest
from allie_sdk.methods.custom_field import *

MOCK_CUSTOM_FIELD = AlationCustomField(
    access_token='test'
    , session=requests.session()
    , host='https://test.com'
)



def test_success_get_custom_fields(requests_mock):

    mock_params = CustomFieldParams()
    mock_params.field_type.add('MULTI_PICKER')
    success_response = [
        {
            "allow_multiple": False,
            "allowed_otypes": None,
            "backref_name": None,
            "backref_tooltip_text": None,
            "builtin_name": "title",
            "field_type": "MULTI_PICKER",
            "id": 1,
            "name_plural": "",
            "name_singular": "Title",
            "options": None,
            "tooltip_text": None
        }
    ]
    mock_fields = [CustomField.from_api_response(item) for item in success_response]
    requests_mock.register_uri('GET', '/integration/v2/custom_field/', json=success_response)
    custom_fields = MOCK_CUSTOM_FIELD.get_custom_fields(query_params=mock_params)

    assert mock_fields == custom_fields


def test_failed_get_custom_fields(requests_mock):

    failed_response = {
        "detail": "Authentication credentials were not provided.",
        "code": "403000"
    }
    requests_mock.register_uri('GET', '/integration/v2/custom_field/', json=failed_response, status_code=403)
    custom_fields = MOCK_CUSTOM_FIELD.get_custom_fields()

    assert custom_fields == None


def test_success_get_custom_field_values(requests_mock):

    mock_params = CustomFieldValueParams()
    mock_params.field_id.add(10006)
    success_response = [
        {
            "field_id": 10006,
            "oid": 12,
            "otype": "table",
            "ts_updated": "2023-07-17T23:59:31.113261Z",
            "value": [{"otype": "groupprofile", "oid": 8}]
        }
    ]
    mock_values = [CustomFieldValue.from_api_response(item) for item in success_response]
    requests_mock.register_uri('GET', '/integration/v2/custom_field_value/', json=success_response)
    field_values = MOCK_CUSTOM_FIELD.get_custom_field_values(query_params=mock_params)

    assert mock_values == field_values

def test_failed_get_custom_field_values(requests_mock):

    failed_response = {
        "detail": "Invalid query parameters: [test]",
        "code": "400006"
    }
    requests_mock.register_uri('GET', '/integration/v2/custom_field_value/', json=failed_response, status_code=400)
    field_values = MOCK_CUSTOM_FIELD.get_custom_field_values()

    assert field_values == None

def test_success_get_a_builtin_custom_field(requests_mock):

    success_response = {
        "allow_multiple": True,
        "allowed_otypes": ["groupprofile", "user"],
        "backref_name": "Steward",
        "backref_tooltip_text": None,
        "builtin_name": "steward",
        "field_type": "OBJECT_SET",
        "id": 8,
        "name_plural": "Stewards",
        "name_singular": "Steward",
        "options": None,
        "tooltip_text": "This is a required field!"
    }
    mock_field = CustomField.from_api_response(success_response)
    requests_mock.register_uri('GET', '/integration/v2/custom_field/builtin/steward/', json=success_response)
    custom_field = MOCK_CUSTOM_FIELD.get_a_builtin_custom_field('steward')

    assert mock_field == custom_field

def test_failed_get_a_builtin_custom_field(requests_mock):

    failed_response = {
        "detail": "Not found.",
        "code": "404000"
    }
    requests_mock.register_uri('GET', '/integration/v2/custom_field/builtin/stewards/', json=failed_response, status_code=404)
    custom_field = MOCK_CUSTOM_FIELD.get_a_builtin_custom_field('stewards')

    assert custom_field == None

def test_success_get_a_custom_field(requests_mock):

    success_response = {
        "allow_multiple": False,
        "allowed_otypes": None,
        "backref_name": None,
        "backref_tooltip_text": None,
        "builtin_name": None,
        "field_type": "RICH_TEXT",
        "id": 10012,
        "name_plural": "",
        "name_singular": "Statement of Policy",
        "options": None,
        "tooltip_text": "This is the specific details of a policy"
    }
    mock_field = CustomField.from_api_response(success_response)
    requests_mock.register_uri('GET', '/integration/v2/custom_field/10012/', json=success_response)
    custom_field = MOCK_CUSTOM_FIELD.get_a_custom_field(10012)

    assert mock_field == custom_field

def test_failed_get_a_custom_filed(requests_mock):

    failed_response = {
        "detail": "Not found.",
        "code": "404000"
    }
    requests_mock.register_uri('GET', '/integration/v2/custom_field/10012/', json=failed_response, status_code=404)
    custom_field = MOCK_CUSTOM_FIELD.get_a_custom_field(10012)

    assert custom_field == None

def test_success_post_custom_fields(requests_mock):

    mock_field_1 = CustomFieldItem()
    mock_field_1.field_type = 'RICH_TEXT'
    mock_field_1.name_singular = 'Testing'

    mock_field_2 = CustomFieldItem()
    mock_field_2.field_type = 'DATE'
    mock_field_2.name_singular = 'Date Test'

    mock_fields_list = [mock_field_1, mock_field_2]

    async_response = {
        "job_id": 1
    }
    job_response = {
        "status": "successful",
        "msg": "Job finished in 0.082468 seconds at 2023-11-28 04:02:35.654663+00:00",
        "result": [
            "{\"msg\": \"Starting bulk creation of Custom Fields...\", \"data\": {}}",
            "{\"msg\": \"Finished bulk creation of Custom Fields\", \"data\": {\"field_ids\": [10020, 10021]}}"
        ]
    }

    requests_mock.register_uri('POST', '/integration/v2/custom_field/', json=async_response)
    requests_mock.register_uri('GET', '/api/v1/bulk_metadata/job/?id=1', json=job_response)

    async_result = MOCK_CUSTOM_FIELD.post_custom_fields(mock_fields_list)

    input_transformed = [JobDetailsCustomFieldPost(**job_response)]

    assert input_transformed == async_result

def test_failed_post_custom_fields(requests_mock):

    """
    Test that a InvalidPostBody is raised when the value of a field doesn't match
    the list of expected values.
    """

    with pytest.raises(InvalidPostBody) as excinfo:

        # input (payload)
        mock_field_1 = CustomFieldItem()
        mock_field_1.field_type = 'RICH_TEXTS' # <= Note: Extra S at the end of RICH_TEXT to cause an error
        mock_field_1.name_singular = 'Testing'
        mock_fields_list = [mock_field_1]

        # response from the custom fields API endpoint
        # NOTE: This error message is coming from the DATA MODEL!
        custom_field_api_response = [
            {
                "field_type": [
                    "The field type 'RICH_TEXTS' is not supported."
                ]
            }
        ]

        # expected_response = [
        #     JobDetailsCustomFieldPost(
        #         status = "failed"
        #         , msg = ""
        #         , result = custom_field_api_response
        #     )
        # ]

        # override response of custom field API endpoint
        requests_mock.register_uri(
            'POST'
            , '/integration/v2/custom_field/'
            , json = custom_field_api_response
            , status_code = 400
        )

        actual_response = MOCK_CUSTOM_FIELD.post_custom_fields(mock_fields_list)

    assert str(excinfo.value) == "The field type 'RICH_TEXTS' is not supported"

def test_success_post_custom_field_values(requests_mock):

    mock_value_1 = CustomFieldValueItem()
    mock_value_1.field_id = 1
    mock_value_1.otype = 'Table'
    mock_value_1.oid = 1
    mock_value_1.value = []
    mock_value_1.value.append(CustomFieldStringValueItem(value='Test'))

    mock_value_2 = CustomFieldValueItem()
    mock_value_2.field_id = 2
    mock_value_2.otype = 'Table'
    mock_value_2.oid = 1
    mock_value_2.value = []
    mock_value_2.value.append(CustomFieldDictValueItem(otype='user', oid=1))

    mock_values_list = [mock_value_1, mock_value_2]

    async_response = {
        "job_id": 1
    }
    job_response = {
        "status": "successful",
        "msg": "Job finished in 1.162451 seconds at 2023-11-28 04:27:11.427967+00:00",
        "result": [
            "Start bulk upsert public annotation field values...",
            "Finished bulk upsert public annotation field values. Updated objects: 1, created objects: 0"
        ]
    }

    requests_mock.register_uri('PUT', '/integration/v2/custom_field_value/async/', json=async_response)
    requests_mock.register_uri('GET', '/api/v1/bulk_metadata/job/?id=1', json=job_response)

    async_result = MOCK_CUSTOM_FIELD.put_custom_field_values(mock_values_list)

    input_transformed = [JobDetails(**job_response)]

    assert input_transformed == async_result

def test_failed_post_custom_field_value(requests_mock):

    # Input data (payload)
    mock_value_1 = CustomFieldValueItem()
    mock_value_1.field_id = 1
    mock_value_1.otype = 'Table'
    mock_value_1.oid = 1
    mock_value_1.value = []
    mock_value_1.value.append(CustomFieldStringValueItem(value='Test'))
    mock_values_list = [mock_value_1]

    custom_field_value_api_failed_response =  {
        "title": "Invalid Payload",
        "detail": "Please check the API documentation for more details on the spec.",
        "errors": [
            {
                "otype": [
                    "Invalid otype"
                ]
            }
        ],
        "code": "400000"
    }

    expected_response = [
        JobDetails(
            status = "failed"
            , msg = "Invalid Payload"
            , result = {
                "title": "Invalid Payload",
                "detail": "Please check the API documentation for more details on the spec.",
                "errors": [
                    {
                        "otype": [
                            "Invalid otype"
                        ]
                    }
                ],
                "code": "400000"
            }
        )
    ]

    # override the custom field value api response
    requests_mock.register_uri(
        'PUT'
        , '/integration/v2/custom_field_value/async/'
        , json=custom_field_value_api_failed_response
        , status_code=400
    )

    # call the function that we want to test
    actual_response = MOCK_CUSTOM_FIELD.put_custom_field_values(mock_values_list)

    # check if the actual result matches the expected result
    assert expected_response == actual_response

