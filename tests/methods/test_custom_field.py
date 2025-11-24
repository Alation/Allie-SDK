"""Test the Alation REST API Custom Field Methods."""
import pytest
from allie_sdk.methods.custom_field import *

class TestCustomField:

    def setup_method(self):
        self.mock_custom_field = AlationCustomField(
            access_token='test',
            session=requests.session(),
            host='https://test.com'
        )


    def test_success_get_custom_fields(self, requests_mock):
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
        custom_fields = self.mock_custom_field.get_custom_fields(query_params=mock_params)

        assert mock_fields == custom_fields


    def test_failed_get_custom_fields(self, requests_mock):
        failed_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }
        requests_mock.register_uri('GET', '/integration/v2/custom_field/', json=failed_response, status_code=403)
        
        # Now we expect an HTTPError to be raised
        with pytest.raises(requests.exceptions.HTTPError) as context:
            self.mock_custom_field.get_custom_fields()
        
        # Verify the error response contains expected information
        assert context.value.response.status_code == 403


    def test_success_get_custom_field_values(self, requests_mock):
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
        field_values = self.mock_custom_field.get_custom_field_values(query_params=mock_params)

        assert mock_values == field_values


    def test_failed_get_custom_field_values(self, requests_mock):
        failed_response = {
            "detail": "Invalid query parameters: [test]",
            "code": "400006"
        }
        requests_mock.register_uri('GET', '/integration/v2/custom_field_value/', json=failed_response, status_code=400)
        
        # Now we expect an HTTPError to be raised
        with pytest.raises(requests.exceptions.HTTPError) as context:
            self.mock_custom_field.get_custom_field_values()
        
        # Verify the error response contains expected information
        assert context.value.response.status_code == 400


    def test_success_get_a_builtin_custom_field(self, requests_mock):
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
        custom_field = self.mock_custom_field.get_a_builtin_custom_field('steward')

        assert mock_field == custom_field


    def test_failed_get_a_builtin_custom_field(self, requests_mock):
        failed_response = {
            "detail": "Not found.",
            "code": "404000"
        }
        requests_mock.register_uri('GET', '/integration/v2/custom_field/builtin/stewards/', json=failed_response, status_code=404)
        
        # Now we expect an HTTPError to be raised
        with pytest.raises(requests.exceptions.HTTPError) as context:
            self.mock_custom_field.get_a_builtin_custom_field('stewards')
        
        # Verify the error response contains expected information
        assert context.value.response.status_code == 404


    def test_success_get_a_custom_field(self, requests_mock):
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
        custom_field = self.mock_custom_field.get_a_custom_field(10012)

        assert mock_field == custom_field


    def test_failed_get_a_custom_field(self, requests_mock):
        failed_response = {
            "detail": "Not found.",
            "code": "404000"
        }
        requests_mock.register_uri('GET', '/integration/v2/custom_field/10012/', json=failed_response, status_code=404)
        
        # Now we expect an HTTPError to be raised
        with pytest.raises(requests.exceptions.HTTPError) as context:
            self.mock_custom_field.get_a_custom_field(10012)
        
        # Verify the error response contains expected information
        assert context.value.response.status_code == 404


    def test_success_post_custom_fields(self, requests_mock):
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

        async_result = self.mock_custom_field.post_custom_fields(mock_fields_list)

        input_transformed = [JobDetailsCustomFieldPost(**job_response)]

        assert input_transformed == async_result


    def test_failed_post_custom_fields(self, requests_mock):
        """
        Test that a InvalidPostBody is raised when the value of a field doesn't match
        the list of expected values.
        """
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

        # override response of custom field API endpoint
        requests_mock.register_uri(
            'POST',
            '/integration/v2/custom_field/',
            json=custom_field_api_response,
            status_code=400
        )

        with pytest.raises(InvalidPostBody) as excinfo:
            self.mock_custom_field.post_custom_fields(mock_fields_list)

        assert str(excinfo.value) == "The field type 'RICH_TEXTS' is not supported"


    def test_success_post_custom_field_values(self, requests_mock):
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

        async_result = self.mock_custom_field.put_custom_field_values(mock_values_list)

        input_transformed = [JobDetails(**job_response)]

        assert input_transformed == async_result



