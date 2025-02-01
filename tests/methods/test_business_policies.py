"""Test the Alation REST API Business Policy Methods."""

import requests_mock
import unittest
from requests import HTTPError
from allie_sdk.methods.business_policy import *


class TestBusinessPolicy(unittest.TestCase):

    def setUp(self):
        self.mock_user = AlationBusinessPolicy(
            access_token='test',
            session=requests.session(),
            host='https://test.com'
        )

    @requests_mock.Mocker()
    def test_get_business_policies(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the Get Policy request?
        policy_api_response = [
            {
                "id": 1,
                "description": "This ...",
                "title": "Compliance with GDPR",
                "otype": "business_policy",
                "ts_created": "2023-01-05T13:27:34.347166Z",
                "url": "/policy/1/",
                "stewards": [
                    {
                        "otype": "user",
                        "otype_display_name": "User",
                        "id": 6,
                        "name": "Diethard Steiner",
                        "title": "",
                        "url": "/user/6/",
                        "deleted": False,
                        "snippet": "",
                        "photo_url": "/static/img/user.png",
                        "email": "diethard.steiner@outlook.com"
                    }
                ]
            },
            {
                "id": 2,
                "description": "",
                "title": "",
                "otype": "business_policy",
                "ts_created": "2023-01-05T13:29:07.345800Z",
                "url": "/policy/2/",
                "stewards": []
            }
        ]

        success_business_policies = [BusinessPolicy.from_api_response(item) for item in policy_api_response]

        # Override the policy API call
        requests_mock.register_uri(
            method='GET',
            url='/integration/v1/business_policies/',
            json=policy_api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        business_policies = self.mock_user.get_business_policies()

        self.assertEqual(success_business_policies, business_policies)
        
    @requests_mock.Mocker()
    def test_empty_get_business_policies(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #
        empty_response = []

        # Override the policy API call
        requests_mock.register_uri(
            method='GET',
            url='/integration/v1/business_policies/',
            json=empty_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        business_policies = self.mock_user.get_business_policies()

        self.assertEqual([], business_policies)
        
    @requests_mock.Mocker()
    def test_failed_get_business_policies(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #
        error_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }

        # Override the policy API call with error response
        requests_mock.register_uri(
            method='GET',
            url='/integration/v1/business_policies/',
            json=error_response,
            status_code=403
        )

        # --- TEST THE FUNCTION --- #
        with self.assertRaises(HTTPError) as context:
            self.mock_user.get_business_policies()
            
        self.assertEqual(context.exception.response.status_code, 403)

    @requests_mock.Mocker()
    def test_create_business_policies(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the Policy Creation request?
        policy_api_response = {
            'task': {
                'id': 23739,
                'type': 'BUSINESS_POLICY_BULK_CREATE',
                'state': 'QUEUED',
                'status': 'NA',
                'ts_started': '2023-12-08T10:08:35.974963Z',
                'links': []
            }
        }

        # Override the policy API call
        requests_mock.register_uri(
            method='POST',
            url='/integration/v1/business_policies/',
            json=policy_api_response,
            status_code=202
        )

        # What does the response look like for the Job?
        job_api_response = {
            'status': 'successful',
            'msg': 'Job finished in 2.171085 seconds at 2023-12-08 17:20:53.735123+00:00',
            'result': [
                'Successfully processed 2 items (index range: [0, 1])',
                'All total 1 batches with a limit of 250 items attempted. [Succeeded: 2, Failed: 0, Total: 2]'
            ]
        }

        """
        OPEN/CONCERN: Here we don't get any details about the created policies back.
        With terms in example the job response includes details about the created terms within
        the result section.
        With policies there's no point really testing this bit of code since we don't really
        have something proper to validate against.
        """

        # Override the job API call
        # Note: The id in the job URL corresponds to the task id in policy_api_response defined above
        requests_mock.register_uri(
            method='GET',
            url='/api/v1/bulk_metadata/job/?id=23739',
            json=job_api_response
        )

        # --- TEST THE FUNCTION --- #
        bulk_create_business_policies_result = self.mock_user.create_business_policies(
            [
                BusinessPolicyPostItem(
                    title="BP3",
                    template_id=158,
                    policy_group_ids=[1],
                    fields=[
                        CustomFieldValueItem(
                            field_id=8,
                            value=[
                                CustomFieldDictValueItem(
                                    otype="user",
                                    oid=1
                                )
                            ]
                        )
                    ]
                ),
                BusinessPolicyPostItem(
                    title="BP4",
                    template_id=158,
                    policy_group_ids=[1],
                    fields=[
                        CustomFieldValueItem(
                            field_id=8,
                            value=[
                                CustomFieldDictValueItem(
                                    otype="user",
                                    oid=1
                                )
                            ]
                        )
                    ]
                )
            ]
        )

        function_expected_result = [
            JobDetails(
                status='successful',
                msg='Job finished in 2.171085 seconds at 2023-12-08 17:20:53.735123+00:00',
                result=[
                    'Successfully processed 2 items (index range: [0, 1])',
                    'All total 1 batches with a limit of 250 items attempted. [Succeeded: 2, Failed: 0, Total: 2]'
                ]
            )
        ]

        self.assertEqual(function_expected_result, bulk_create_business_policies_result)
        
    @requests_mock.Mocker()
    def test_failed_create_business_policies(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #
        error_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }

        # Override the policy API call with error response
        requests_mock.register_uri(
            method='POST',
            url='/integration/v1/business_policies/',
            json=error_response,
            status_code=403
        )

        # --- TEST THE FUNCTION --- #
        with self.assertRaises(HTTPError) as context:
            self.mock_user.create_business_policies(
                [
                    BusinessPolicyPostItem(
                        title="BP3",
                        template_id=158,
                        policy_group_ids=[1],
                        fields=[
                            CustomFieldValueItem(
                                field_id=8,
                                value=[
                                    CustomFieldDictValueItem(
                                        otype="user",
                                        oid=1
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
            
        self.assertEqual(context.exception.response.status_code, 403)

    @requests_mock.Mocker()
    def test_update_business_policies(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the Policy Update request?
        policy_api_response = {
            'task': {
                'id': 24984,
                'type': 'BUSINESS_POLICY_BULK_UPDATE',
                'state': 'QUEUED',
                'status': 'NA',
                'ts_started': '2023-12-28T17:29:18.693001Z',
                'links': []
            }
        }

        # Override the policy API call
        requests_mock.register_uri(
            method='PUT',
            url='/integration/v1/business_policies/',
            json=policy_api_response,
            status_code=202
        )

        # What does the response look like for the Job?
        job_api_response = {
            'status': 'successful',
            'msg': 'Job finished in 1.129593 seconds at 2023-12-28 17:29:20.084519+00:00',
            'result': [
                'Successfully processed 2 items (index range: [0, 1])',
                'All total 1 batches with a limit of 250 items attempted. [Succeeded: 2, Failed: 0, Total: 2]'
            ]
        }

        """
        OPEN/CONCERN: Here we don't get any details about the created policies back.
        With terms in example the job response includes details about the created terms within
        the result section.
        With policies there's no point really testing this bit of code since we don't really
        have something proper to validate against.
        """

        # Override the job API call
        # Note: The id in the job URL correspondes to the task id in policy_api_response defined above
        requests_mock.register_uri('GET', '/api/v1/bulk_metadata/job/?id=24984', json=job_api_response)

        # --- TEST THE FUNCTION --- #
        bulk_update_business_policies_result = self.mock_user.update_business_policies(
            business_policies=[
                BusinessPolicyPutItem(
                    id=26,
                    title="UPDATED description",
                    template_id=158,
                    policy_group_ids=BusinessPolicyGroupIds(
                        add=[1]
                    ),
                    fields=[
                        CustomFieldValueItem(
                            field_id=8,
                            value=[
                                CustomFieldDictValueItem(
                                    otype="user",
                                    oid=2
                                )
                            ]
                        )
                    ]
                )
            ]
        )

        function_expected_result = [
            JobDetails(
                status='successful',
                msg='Job finished in 1.129593 seconds at 2023-12-28 17:29:20.084519+00:00',
                result=[
                    'Successfully processed 2 items (index range: [0, 1])',
                    'All total 1 batches with a limit of 250 items attempted. [Succeeded: 2, Failed: 0, Total: 2]'
                ]
            )
        ]
        self.assertEqual(function_expected_result, bulk_update_business_policies_result)

    @requests_mock.Mocker()
    def test_delete_business_policies(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the Policy Delete request?
        policy_api_response = ''

        # Override the policy API call
        requests_mock.register_uri(
            method='DELETE',
            url='/integration/v1/business_policies/',
            json=policy_api_response,
            status_code=204
        )

        # --- TEST THE FUNCTION --- #
        delete_business_policy_result = self.mock_user.delete_business_policies(
            [
                BusinessPolicy(
                    id=1
                ),
                BusinessPolicy(
                    id=2
                )
            ]
        )

        # OPEN: See concern mentioned further up
        function_expected_result = JobDetails(
            status='successful',
            msg='',
            result=''
        )
        self.assertEqual(function_expected_result, delete_business_policy_result)