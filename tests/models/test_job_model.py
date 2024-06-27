import unittest
from allie_sdk.methods.job import *


class TestGroupModels(unittest.TestCase):
    # check if we can map the job result output for a document creation to our data class
    def test_job_model_for_document_post(self):

        # Expected input
        input = {
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

        # Transformation
        input_transformed = JobDetails(**input)

        # Expected Output
        output = JobDetails(
                status='successful'
                , msg='Job finished in 0.242215 seconds at 2024-06-20 13:23:02.698215+00:00'
                , result = JobDetailsResult(
                    created_term_count = 2
                    , created_terms = [
                        JobDetailsResultDetails(id = 1325, title = 'My KPI 1')
                        , JobDetailsResultDetails(id = 1326, title = 'My KPI 2')
                    ]
                )
            )

        self.assertEqual(input_transformed, output)

    def test_job_model_for_document_put(self):
        # Expected input
        input =  {
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

        # Transformation
        input_transformed = JobDetails(**input)

        # Expected Output
        output = JobDetails(
            status='successful'
            , msg='Job finished in 0.075303 seconds at 2024-06-21 13:16:42.261763+00:00'
            , result=JobDetailsResult(
                updated_term_count=2
                , updated_terms=[
                    JobDetailsResultDetails(id=1334)
                    , JobDetailsResultDetails(id=1335)
                ]
            )
        )

        self.assertEqual(input_transformed, output)

    # the job resonse for terms is exactly the same as for documents
    def test_job_model_for_term_post(self):

        # Expected input
        input = {
            'status': 'successful'
            , 'msg': 'Job finished in 0.242215 seconds at 2024-06-20 13:23:02.698215+00:00'
            , 'result': {
                'created_term_count': 2
                , 'created_terms': [
                    {'id': 1325, 'title': 'My Term 1'}
                    , {'id': 1326, 'title': 'My Term 2'}
                ]
            }
        }

        # Transformation
        input_transformed = JobDetails(**input)

        # Expected Output
        output = JobDetails(
                status='successful'
                , msg='Job finished in 0.242215 seconds at 2024-06-20 13:23:02.698215+00:00'
                , result = JobDetailsResult(
                    created_term_count = 2
                    , created_terms = [
                        JobDetailsResultDetails(id = 1325, title = 'My Term 1')
                        , JobDetailsResultDetails(id = 1326, title = 'My Term 2')
                    ]
                )
            )

        self.assertEqual(input_transformed, output)

    def test_job_model_for_term_put(self):
        # Expected input
        input =  {
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

        # Transformation
        input_transformed = JobDetails(**input)

        # Expected Output
        output = JobDetails(
            status='successful'
            , msg='Job finished in 0.075303 seconds at 2024-06-21 13:16:42.261763+00:00'
            , result=JobDetailsResult(
                updated_term_count=2
                , updated_terms=[
                    JobDetailsResultDetails(id=1334)
                    , JobDetailsResultDetails(id=1335)
                ]
            )
        )

        self.assertEqual(input_transformed, output)
    def test_job_model_for_business_policy_post(self):
        # Expected input
        input = {
            "status": 'successful'
            , "msg": 'Job finished in 0.187183 seconds at 2024-06-24 14:25:00.890058+00:00'
            , "result": [
                'Successfully processed 2 items (index range: [0, 1])'
                , 'All total 1 batches with a limit of 250 items attempted. [Succeeded: 2, Failed: 0, Total: 2]'
            ]
        }

        # Transformation
        input_transformed = JobDetails(**input)

        # Expected Output
        output = JobDetails(
            status='successful'
            , msg='Job finished in 0.187183 seconds at 2024-06-24 14:25:00.890058+00:00'
            , result=[
                'Successfully processed 2 items (index range: [0, 1])'
                , 'All total 1 batches with a limit of 250 items attempted. [Succeeded: 2, Failed: 0, Total: 2]'
            ]
        )

        self.assertEqual(input_transformed, output)

    def test_job_model_for_business_policy_put(self):
        # Expected input
        input = {
            'status': 'successful'
            , 'msg': 'Job finished in 0.235195 seconds at 2024-06-24 14:46:05.806027+00:00'
            , 'result': [
                'Successfully processed 1 items (index range: [0, 0])'
                , 'All total 1 batches with a limit of 250 items attempted. [Succeeded: 1, Failed: 0, Total: 1]'
            ]
        }

        # Transformation
        input_transformed = JobDetails(**input)

        # Expected Output
        output = JobDetails(
            status='successful'
            , msg='Job finished in 0.235195 seconds at 2024-06-24 14:46:05.806027+00:00'
            , result=[
                'Successfully processed 1 items (index range: [0, 0])'
                , 'All total 1 batches with a limit of 250 items attempted. [Succeeded: 1, Failed: 0, Total: 1]'
            ]
        )

        self.assertEqual(input_transformed, output)

    # CUSTOM FIELDS

    # Custom Field POST

    """
    For custom field post no status is returned.
    On the plus side, it returns the field IDs once finished successfully.
    
    '{"msg": "Starting bulk creation of Custom Fields...", "data": {}}'
    '{"msg": "Finished bulk creation of Custom Fields", "data": {"field_ids": [10314]}}'
    """

    def test_job_model_for_custom_field_post(self):
        # Expected input
        input = {
            "status": "successful"
            , "msg": "Job finished in 0.011206 seconds at 2024-06-27 10:38:42.197271+00:00"
            , "result": [
                {
                    "msg": "Starting bulk creation of Custom Fields..."
                    , "data": {}
                }
                , {
                    "msg": "Finished bulk creation of Custom Fields"
                    , "data": {
                        "field_ids": [10314]
                    }
                }
            ]

        }

        JobDetails(status='successful', msg='Job finished in 0.011206 seconds at 2024-06-27 10:38:42.197271+00:00',
                   result=['{"msg": "Starting bulk creation of Custom Fields...", "data": {}}',
                           '{"msg": "Finished bulk creation of Custom Fields", "data": {"field_ids": [10317]}}'],
                   data=JobDetailsCustomFieldData(field_ids=[]))

        # Transformation
        input_transformed = JobDetails(**input)

        # Expected Output
        output = JobDetails(
            msg='Finished bulk creation of Custom Fields'
            , data = JobDetailsCustomFieldData(
                field_ids = [10314]
            )
        )

        self.assertEqual(input_transformed, output)

    # Custom Field Value PUT

    """
    "When updating custom field values, this API runs two background jobs. The API response returns the ID of the first job. Use that ID to query the Jobs API. The response from the Jobs API returns the ID of the second job.
    If either job fails, you must retry the API request." (Source: Official API Doc) 
    DS: This applies to ACS instances only it seems
    """

    def test_job_model_for_custom_field_value_put(self):
        # Expected input
        input = {
            "status": "successful",
            "msg": "Job finished in 0.147134 seconds at 2024-06-27 10:01:45.113414+00:00",
            "result": [
                "Start bulk upsert public annotation field values...",
                "Finished bulk upsert public annotation field values. Updated objects: 0, created objects: 1"
            ]
        }

        # Transformation
        input_transformed = JobDetails(**input)

        # Expected Output
        output = JobDetails(
            status='successful'
            , msg='Job finished in 0.147134 seconds at 2024-06-27 10:01:45.113414+00:00'
            , result=[
                'Start bulk upsert public annotation field values...'
                , 'Finished bulk upsert public annotation field values. Updated objects: 0, created objects: 1'
                ]
            )

        self.assertEqual(input_transformed, output)