import unittest
from allie_sdk.methods.job import *


class TestGroupModels(unittest.TestCase):
    # check if we can map the job result output for a document creation to our data class
    def test_job_model_for_post_documents(self):

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
                        JobDetailsResultCreatedObjects(id = 1325, title = 'My KPI 1')
                        , JobDetailsResultCreatedObjects(id = 1326, title = 'My KPI 2')
                    ]
                )
            )

        self.assertEqual(input_transformed, output)