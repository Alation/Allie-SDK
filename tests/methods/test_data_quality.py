"""Test the Alation REST API Data Quality Methods"""

import requests_mock
from allie_sdk.methods.data_quality import *

MOCK_DQ = AlationDataQuality(
    access_token='test', session=requests.session(), host='https://test.com'
)



def test_success_get_data_quality_fields(requests_mock):

    mock_params = DataQualityFieldParams()
    mock_params.key.add('1.DQ.Test')
    success_response = [
        {
            "key": "1.DQ.Test",
            "name": "Possibly Deleted",
            "description": "Test DQ Field",
            "type": "VARCHAR",
            "ts_created": "2023-07-07T23:30:20.654601Z"
        }
    ]
    success_dq_fields = [DataQualityField.from_api_response(item) for item in success_response]
    requests_mock.register_uri('GET', '/integration/v1/data_quality/fields/?key=1.DQ.Test',
                   json=success_response)
    dq_fields = MOCK_DQ.get_data_quality_fields(mock_params)

    assert success_dq_fields == dq_fields

def test_failed_get_data_quality_fields(requests_mock):

    failed_response = {
        "detail": "Authentication credentials were not provided.",
        "code": "403000"
    }
    requests_mock.register_uri('GET', '/integration/v1/data_quality/fields/', json=failed_response,
                   status_code=403)
    dq_fields = MOCK_DQ.get_data_quality_fields()

    assert dq_fields is None

def test_success_post_data_quality_field(requests_mock):

    # --- PREPARE THE TEST SETUP --- #

    # What does the response look like for the DQ POST request?
    async_response = {
        "job_id": 1,
        "href": "/api/v1/bulk_metadata/job/?id=813"
    }

    # What does the response look like for the job endpoint?
    job_response = {
        "status": "successful",
        "msg": "Job finished in 0.013078 seconds at 2024-07-12 14:01:16.415484+00:00",
        "result": {
            "fields": {
                "created": {"count": 1, "sample": [{'field_key': 'sdk-test-1'}]},
                "updated": {"count": 0, "sample": []}
            },
            "values": {
                "created": { "count": 0,"sample": []},
                "updated": {"count": 0, "sample": []}
            },
            "created_object_attribution": {
                "success_count": 0, "failure_count": 0,
                "success_sample": [], "failure_sample": []
            },
            "flag_counts": {"GOOD": 0, "WARNING": 0, "ALERT": 0},
            "total_duration": 0.015614960000675637
        }
    }

    # Override the result of the API calls
    requests_mock.register_uri('POST', '/integration/v1/data_quality/', json=async_response)
    requests_mock.register_uri('GET', '/api/v1/bulk_metadata/job/?id=1', json=job_response)

    # --- TEST THE FUNCTION --- #
    async_result = MOCK_DQ.post_data_quality_fields(
        [
            DataQualityFieldItem(
                field_key='sdk-test-1',
                name='Testing the SDK',
                type='STRING',
                description='Example test code'
            )
        ]
    )

    function_expected_result = [
        JobDetailsDataQuality(
            status='successful'
            , msg='Job finished in 0.013078 seconds at 2024-07-12 14:01:16.415484+00:00'
            , result=JobDetailsDataQualityResult(
                fields=JobDetailsDataQualityResultAction(
                    created=JobDetailsDataQualityResultActionStats(count=1, sample=[{'field_key': 'sdk-test-1'}])
                    , updated=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , deleted=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , not_found=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                )
                , values=JobDetailsDataQualityResultAction(
                    created=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , updated=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , deleted=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , not_found=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                )
                , created_object_attribution=JobDetailsDataQualityResultCreatedObjectAttribution(
                    success_count=0
                    , failure_count=0
                    , success_sample=[]
                    , failure_sample=[]
                )
                , flag_counts={'GOOD': 0, 'WARNING': 0, 'ALERT': 0}
                , total_duration=0.015614960000675637
            )
        )
    ]

    assert async_result == function_expected_result

def test_failed_post_data_quality_fields(requests_mock):

    failed_response = {
        "Entry": 1,
        "Message": "field_key is required"
    }

    requests_mock.register_uri(
        'POST'
        , '/integration/v1/data_quality/'
        , json = failed_response
        , status_code = 400
    )

    async_result = MOCK_DQ.post_data_quality_fields(
        [
            DataQualityFieldItem(
                field_key='sdk-test-1',
                name='Testing the SDK',
                type='STRING',
                description='Example test code'
            )
        ]
    )

    expected_response = [
        JobDetailsDataQuality(
            status = 'failed'
            , msg = None
            , result = {'Entry': 1, 'Message': 'field_key is required'}
        )
    ]

    assert expected_response == async_result

def test_success_delete_data_quality_fields(requests_mock):


    # --- PREPARE THE TEST SETUP --- #

    # What does the response look like for the DQ DELETE request?
    async_response = {
        "job_id": 1,
        "href": "/api/v1/bulk_metadata/job/?id=814"
    }

    # What does the response look like for the job endpoint?
    job_response = {
        "status": "successful",
        "msg": "Job finished in 0.10362 seconds at 2023-11-30 17:08:47.859401+00:00",
        "result": {
            "fields": {
                "deleted": {"count": 1, "sample": [{"field_key": "human_name_string_2"}]},
                "not_found": {"count": 1, "sample": [{"field_key": "human_name_string"}]}},
            "values": {
                "deleted": {"count": 0, "sample": []},
                "not_found": {"count": 0, "sample": []}
            },
            "total_duration": 0.10439563915133476
        }
    }

    # Override the result of the API calls
    requests_mock.register_uri('DELETE', '/integration/v1/data_quality/', json=async_response)
    requests_mock.register_uri('GET', '/api/v1/bulk_metadata/job/?id=1', json=job_response)

    # --- TEST THE FUNCTION --- #
    async_result = MOCK_DQ.delete_data_quality_fields(
        [
            DataQualityField(
                key='1.Test.DataQuality'
            )
        ]
    )

    function_expected_result = [
        JobDetailsDataQuality(
            status='successful'
            , msg='Job finished in 0.10362 seconds at 2023-11-30 17:08:47.859401+00:00'
            , result=JobDetailsDataQualityResult(
                fields=JobDetailsDataQualityResultAction(
                    created=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , updated=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , deleted=JobDetailsDataQualityResultActionStats(count=1, sample=[{"field_key": "human_name_string_2"}])
                    , not_found=JobDetailsDataQualityResultActionStats(count=1, sample=[{"field_key": "human_name_string"}])
                )
                , values=JobDetailsDataQualityResultAction(
                    created=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , updated=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , deleted=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , not_found=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                )
                , created_object_attribution=JobDetailsDataQualityResultCreatedObjectAttribution(
                    success_count=0
                    , failure_count=0
                    , success_sample=[]
                    , failure_sample=[]
                )
                , flag_counts={}
                , total_duration=0.10439563915133476
            )
        )
    ]

    assert async_result == function_expected_result
def test_failed_delete_data_quality_fields(requests_mock):

    dq_field = DataQualityField()
    dq_field.key = '1.Test.DataQuality'
    dq_field_list = [dq_field]

    failed_response = {
        "Entry": -1,
        "Message": "A \"values\" or \"fields\" property must be specified"
    }

    requests_mock.register_uri(
        'DELETE'
        , '/integration/v1/data_quality/'
        , json = failed_response
        , status_code = 400
    )
    async_result = MOCK_DQ.delete_data_quality_fields(dq_field_list)

    expected_result = [
        JobDetailsDataQuality(
            status='failed'
            , msg=None
            , result={'Entry': -1, 'Message': 'A "values" or "fields" property must be specified'}
        )
    ]

    assert expected_result == async_result

def test_success_get_data_quality_values(requests_mock):

    mock_params = DataQualityValueParams()
    mock_params.field_key.add("1.DQ.Test")
    success_response = [
        {
            "object_key": "1.superstore.public.superstore_reporting.product_name",
            "object_name": "product_name",
            "otype": "attribute",
            "oid": 84,
            "source_object_key": "1.superstore.public.superstore_reporting.product_name",
            "source_object_name": "product_name",
            "source_otype": "attribute",
            "source_oid": 84,
            "value_id": 174,
            "value_value": "Pass Rate: 81.5655%",
            "value_quality": "ALERT",
            "value_last_updated": "2023-08-31T19:12:26.093295Z",
            "value_external_url": None,
            "field_key": "1.DQ.Test",
            "field_name": "COL_GOLD",
            "field_description": None
        }
    ]
    success_dq_values = [DataQualityValue.from_api_response(item) for item in success_response]
    requests_mock.register_uri('GET', '/integration/v1/data_quality/values/',
                   json=success_response)
    dq_values = MOCK_DQ.get_data_quality_values(mock_params)

    assert success_dq_values == dq_values

def test_failed_get_data_quality_values(requests_mock):

    failed_response = {
        "detail": "Authentication credentials were not provided.",
        "code": "403000"
    }
    requests_mock.register_uri('GET', '/integration/v1/data_quality/values/', json=failed_response,
                   status_code=403)
    dq_values = MOCK_DQ.get_data_quality_values()

    assert dq_values is None

def test_success_post_data_quality_values(requests_mock):

    # --- PREPARE THE TEST SETUP --- #

    # What does the response look like for the DQ POST request?
    async_response = {
        "job_id": 1,
        "href": "/api/v1/bulk_metadata/job/?id=815"
    }

    # What does the response look like for the job endpoint?
    job_response = {
        "status": "successful",
        "msg": "Job finished in 0.102986 seconds at 2023-11-30 17:19:08.627064+00:00",
        "result": {
            "fields": {
                "created": {"count": 0, "sample": []},
                "updated": {"count": 0, "sample": []}
            },
            "values": {
                "created": {"count": 1, "sample": [{'field_key': '1.DQ.Test', 'object_key': '1.Test.Table'}]},
                "updated": {"count": 0, "sample": []}
            },
            "created_object_attribution": {
                "success_count": 0,
                "failure_count": 0,
                "success_sample": [],
                "failure_sample": []
            },
            "flag_counts": {
                "GOOD": 0,
                "WARNING": 0,
                "ALERT": 0
            },
            "total_duration": 0.10394948534667492
        }
    }

    # Override the result of the API calls
    requests_mock.register_uri('POST', '/integration/v1/data_quality/', json=async_response)
    requests_mock.register_uri('GET', '/api/v1/bulk_metadata/job/', json=job_response)

    # --- TEST THE FUNCTION --- #
    async_result = MOCK_DQ.post_data_quality_values(
        [
            DataQualityValueItem(
                field_key='1.DQ.Test'
                , object_key='1.Test.Table'
                , object_type='Table'
                , status='WARNING'
                , value='ETL job warning'
            )
        ]
    )

    function_expected_result = [
        JobDetailsDataQuality(
            status='successful'
            , msg='Job finished in 0.102986 seconds at 2023-11-30 17:19:08.627064+00:00'
            , result=JobDetailsDataQualityResult(
                fields=JobDetailsDataQualityResultAction(
                    created=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , updated=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , deleted=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , not_found=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                )
                , values=JobDetailsDataQualityResultAction(
                    created=JobDetailsDataQualityResultActionStats(count=1, sample=[
                            {'field_key': '1.DQ.Test', 'object_key': '1.Test.Table'}
                        ]
                    )
                    , updated=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , deleted=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , not_found=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                )
                , created_object_attribution=JobDetailsDataQualityResultCreatedObjectAttribution(
                    success_count=0
                    , failure_count=0
                    , success_sample=[]
                    , failure_sample=[]
                )
                , flag_counts={'GOOD': 0, 'WARNING': 0, 'ALERT': 0}
                , total_duration=0.10394948534667492
            )
        )
    ]

    assert async_result == function_expected_result

def test_failed_post_data_quality_values(requests_mock):

    dq_value = DataQualityValueItem()
    dq_value.field_key = '1.DQ.Test'
    dq_value.object_key = '1.Test.Table'
    dq_value.object_type = 'Table'
    dq_value.status = 'WARNING'
    dq_value.value = 'ETL job warning'
    dq_value_list = [dq_value]

    failed_response = {
        "Entry": 1,
        "Message": "field_key is required"
    }
    requests_mock.register_uri(
        'POST'
        , '/integration/v1/data_quality/'
        , json=failed_response
        , status_code=400
    )
    async_result = MOCK_DQ.post_data_quality_values(dq_value_list)

    expected_result = [
        JobDetailsDataQuality(
            status='failed'
            , msg=None
            , result={'Entry': 1, 'Message': 'field_key is required'}
        )
    ]

    assert expected_result == async_result

def test_success_delete_data_quality_values(requests_mock):

    # --- PREPARE THE TEST SETUP --- #

    # What does the response look like for the DQ DELETE request?
    async_response = {
        "job_id": 1,
        "href": "/api/v1/bulk_metadata/job/?id=819"
    }

    # What does the response look like for the job endpoint?
    job_response = {
        "status": "successful",
        "msg": "Job finished in 0.086684 seconds at 2023-11-30 17:30:34.582365+00:00",
        "result": {
            "fields": {
                "deleted": {
                    "count": 0,
                    "sample": []
                },
                "not_found": {
                    "count": 0,
                    "sample": []
                }
            },
            "values": {
                "deleted": {
                    "count": 1,
                    "sample": [{"field_key": "1.DQ.Test", "object_key": "1.Test.Table"}]
                },
                "not_found": {
                    "count": 0,
                    "sample": []
                }
            },
            "total_duration": 0.0881261546164751
        }
    }

    # Override the result of the API calls
    requests_mock.register_uri('DELETE', '/integration/v1/data_quality/', json=async_response)
    requests_mock.register_uri('GET', '/api/v1/bulk_metadata/job/?id=1', json=job_response)

    # --- TEST THE FUNCTION --- #
    async_result = MOCK_DQ.delete_data_quality_values(
        [
            DataQualityValue(
                field_key='1.DQ.Test'
                , object_key='1.Test.Table'
            )
        ]
    )

    function_expected_result = [
        JobDetailsDataQuality(
            status='successful'
            , msg='Job finished in 0.086684 seconds at 2023-11-30 17:30:34.582365+00:00'
            , result=JobDetailsDataQualityResult(
                fields=JobDetailsDataQualityResultAction(
                    created=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , updated=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , deleted=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , not_found=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                )
                , values=JobDetailsDataQualityResultAction(
                    created=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , updated=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                    , deleted=JobDetailsDataQualityResultActionStats(count=1, sample=[
                            {"field_key": "1.DQ.Test", "object_key": "1.Test.Table"}
                        ]
                    )
                    , not_found=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                )
                , created_object_attribution=JobDetailsDataQualityResultCreatedObjectAttribution(
                    success_count=0
                    , failure_count=0
                    , success_sample=[]
                    , failure_sample=[]
                )
                , flag_counts={}
                , total_duration=0.0881261546164751
            )
        )
    ]

    assert async_result == function_expected_result

def test_failed_async_delete_process(requests_mock):

    dq_value = DataQualityValue()
    dq_value.field_key = '1.DQ.Test'
    dq_value.object_key = '1.Test.Table'
    dq_value_list = [dq_value]

    failed_response = {
        "Entry": 1,
        "Message": "field_key is required"
    }
    requests_mock.register_uri(
        'DELETE'
        , '/integration/v1/data_quality/'
        , json=failed_response
        , status_code=400
    )


    async_result = MOCK_DQ.delete_data_quality_values(dq_value_list)

    expected_result = [
        JobDetailsDataQuality(
            status='failed'
            , msg=None
            , result={'Entry': 1, 'Message': 'field_key is required'}
        )
    ]

    assert expected_result == async_result
