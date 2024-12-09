import unittest
from allie_sdk.methods.job import *


class TestGroupModels(unittest.TestCase):

    def test_job_model_for_document_delete(self):

        # Expected input
        input = {
            'status': 'successful'
            , 'msg': 'Job finished in 0.242215 seconds at 2024-06-20 13:23:02.698215+00:00'
            , 'result': {
                "deleted_document_count": 2,
                "deleted_document_ids": [
                    11, 12
                ]
            }
        }

        # Transformation
        input_transformed = JobDetailsDocumentDelete(**input)

        # Expected Output
        output = JobDetailsDocumentDelete(
            status='successful'
            , msg='Job finished in 0.242215 seconds at 2024-06-20 13:23:02.698215+00:00'
            , result= JobDetailsDocumentDeleteResult(
                deleted_document_count = 2
                , deleted_document_ids = [
                    11, 12
                ]
            )
        )

        self.assertEqual(input_transformed, output)

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
        input_transformed = JobDetailsDocumentPost(**input)

        # Expected Output
        output = JobDetailsDocumentPost(
                status='successful'
                , msg='Job finished in 0.242215 seconds at 2024-06-20 13:23:02.698215+00:00'
                , result = JobDetailsDocumentPostResult(
                    created_term_count = 2
                    , created_terms = [
                        JobDetailsDocumentPostResultDetails(id = 1325, title = 'My KPI 1')
                        , JobDetailsDocumentPostResultDetails(id = 1326, title = 'My KPI 2')
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
        input_transformed = JobDetailsDocumentPut(**input)

        # Expected Output
        output = JobDetailsDocumentPut(
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
        input_transformed = JobDetailsDocumentPost(**input)

        # Expected Output
        output = JobDetailsDocumentPost(
                status='successful'
                , msg='Job finished in 0.242215 seconds at 2024-06-20 13:23:02.698215+00:00'
                , result = JobDetailsDocumentPostResult(
                    created_term_count = 2
                    , created_terms = [
                        JobDetailsDocumentPostResultDetails(id = 1325, title = 'My Term 1')
                        , JobDetailsDocumentPostResultDetails(id = 1326, title = 'My Term 2')
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
        input_transformed = JobDetailsDocumentPut(**input)

        # Expected Output
        output = JobDetailsDocumentPut(
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


        # Transformation
        input_transformed = JobDetailsCustomFieldPost(**input)

        # Expected Output
        output = JobDetailsCustomFieldPost(
            status='successful'
            , msg='Job finished in 0.011206 seconds at 2024-06-27 10:38:42.197271+00:00'
            , result = [
                JobDetailsCustomFieldPostResult(
                    msg='Starting bulk creation of Custom Fields...'
                    , data = {}
                )
                , JobDetailsCustomFieldPostResult(
                    msg='Finished bulk creation of Custom Fields'
                    , data = JobDetailsCustomFieldPostResultData(
                        field_ids = [10314]
                    )
                )
            ]
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

    def test_job_model_for_rdbms_schema_post(self):
        # Expected input
        input = {
            "status": "successful",
            "msg": "Job finished in 1.94582 seconds at 2023-11-30 16:09:48.515164+00:00",
            "result": [
                {
                    "response": "Upserted 2 column objects.",
                    "mapping": [
                        {"id": 1049, "key": "9.sales"},
                        {"id": 1048, "key": "9.orders"}
                    ],
                    "errors": []
                }
            ]
        }

        # Transformation
        input_transformed = JobDetailsRdbms(**input)

        # Expected Output
        output = JobDetailsRdbms(
            status='successful'
            , msg='Job finished in 1.94582 seconds at 2023-11-30 16:09:48.515164+00:00'
            , result = [
                JobDetailsRdbmsResult(
                    response = "Upserted 2 column objects."
                    , mapping = [
                        JobDetailsRdbmsResultMapping(id = 1049, key = "9.sales")
                        , JobDetailsRdbmsResultMapping(id = 1048, key = "9.orders")
                    ]
                    , errors = []
                )
            ]
        )

        self.assertEqual(input_transformed, output)
    def test_job_model_for_rdbms_table_post(self):
        # Expected input
        input = {
            "status": "successful",
            "msg": "Job finished in 1.94582 seconds at 2023-11-30 16:09:48.515164+00:00",
            "result": [
                {
                    "response": "Upserted 2 table objects.",
                    "mapping": [
                        {"id": 1049, "key": "9.sales.returns"},
                        {"id": 1048, "key": "9.sales.sales_commissions"}
                    ],
                    "errors": []
                }
            ]
        }

        # Transformation
        input_transformed = JobDetailsRdbms(**input)

        # Expected Output
        output = JobDetailsRdbms(
            status='successful'
            , msg='Job finished in 1.94582 seconds at 2023-11-30 16:09:48.515164+00:00'
            , result = [
                JobDetailsRdbmsResult(
                    response = "Upserted 2 table objects."
                    , mapping = [
                        JobDetailsRdbmsResultMapping(id = 1049, key = "9.sales.returns")
                        , JobDetailsRdbmsResultMapping(id = 1048, key = "9.sales.sales_commissions")
                    ]
                    , errors = []
                )
            ]
        )

        self.assertEqual(input_transformed, output)
    
    def test_job_model_for_rdbms_column_post(self):
        # Expected input
        input = {
            "status": "successful",
            "msg": "Job finished in 1.94582 seconds at 2023-11-30 16:09:48.515164+00:00",
            "result": [
                {
                    "response": "Upserted 2 column objects.",
                    "mapping": [
                        {"id": 1049, "key": "9.sales.returns.id"},
                        {"id": 1048, "key": "9.sales.sales_commissions.id"}
                    ],
                    "errors": []
                }
            ]
        }

        # Transformation
        input_transformed = JobDetailsRdbms(**input)

        # Expected Output
        output = JobDetailsRdbms(
            status='successful'
            , msg='Job finished in 1.94582 seconds at 2023-11-30 16:09:48.515164+00:00'
            , result = [
                JobDetailsRdbmsResult(
                    response = "Upserted 2 column objects."
                    , mapping = [
                        JobDetailsRdbmsResultMapping(id = 1049, key = "9.sales.returns.id")
                        , JobDetailsRdbmsResultMapping(id = 1048, key = "9.sales.sales_commissions.id")
                    ]
                    , errors = []
                )
            ]
        )

        self.assertEqual(input_transformed, output)

    def test_job_model_for_virtual_datasource_post(self):
        # Expected input
        input = {
            'status': 'successful'
            , 'msg': 'Job finished in 1.0 seconds at 2024-07-02 13:45:23.994057+00:00'
            , 'result': '{"number_received": 5, "updated_objects": 0, "error_objects": ["Failed to import the uploaded file at line 4. Data may be malformed."], "error": "1 errors were ignored"}'
        }

        # Transformation
        input_transformed = JobDetailsVirtualDatasourcePost(**input)

        # Expected Output
        output = JobDetailsVirtualDatasourcePost(
            status='successful'
            , msg='Job finished in 1.0 seconds at 2024-07-02 13:45:23.994057+00:00'
            , result= JobDetailsVirtualDatasourcePostResult(
                number_received = 5
                , updated_objects = 0
                , error_objects = ["Failed to import the uploaded file at line 4. Data may be malformed."]
                , error = "1 errors were ignored"
            )
        )

        self.assertEqual(input_transformed, output)

    def test_job_model_for_data_quality_fields_post(self):

        # Expected input
        input = {
            'status': 'successful'
            , 'msg': 'Job finished in 0.008073 seconds at 2024-07-03 15:30:23.473166+00:00'
            , 'result': {
                'fields': {
                    'created': {
                        'count': 0
                        , 'sample': []
                    }
                    , 'updated': {
                        'count': 1
                        , 'sample': [
                            {'field_key': 'sdk-test-1'}
                        ]
                    }
                }
                , 'values': {'created': {'count': 0, 'sample': []}, 'updated': {'count': 0, 'sample': []}}
                , 'created_object_attribution': {'success_count': 0, 'failure_count': 0, 'success_sample': [], 'failure_sample': []}
                , 'flag_counts': {'GOOD': 0, 'WARNING': 0, 'ALERT': 0}
                , 'total_duration': 0.010898920998442918
            }
        }

        # Transformation
        input_transformed = JobDetailsDataQuality(**input)

        # Expected Output
        output = JobDetailsDataQuality(
            status='successful'
            , msg='Job finished in 0.008073 seconds at 2024-07-03 15:30:23.473166+00:00'
            , result=JobDetailsDataQualityResult(
                fields=JobDetailsDataQualityResultAction(
                    created=JobDetailsDataQualityResultActionStats(
                        count=0
                        , sample=[]
                    )
                    , updated=JobDetailsDataQualityResultActionStats(
                        count=1
                        , sample=[
                            {'field_key': 'sdk-test-1'}
                        ]
                    )
                )
                , values=JobDetailsDataQualityResultAction(
                    created=JobDetailsDataQualityResultActionStats(
                        count=0
                        , sample=[]
                    )
                    , updated=JobDetailsDataQualityResultActionStats(
                        count=0
                        , sample=[]
                    )
                )
                , created_object_attribution=JobDetailsDataQualityResultCreatedObjectAttribution(
                    success_count=0
                    , failure_count=0
                    , success_sample=[]
                    , failure_sample=[]
                )
                , flag_counts={'GOOD': 0, 'WARNING': 0, 'ALERT': 0}
                , total_duration=0.010898920998442918
            )
        )

        self.assertEqual(input_transformed, output)

    def test_job_model_for_data_quality_values_post(self):

        # Expected input
        input = {
            'status': 'successful'
            , 'msg': 'Job finished in 0.067679 seconds at 2024-07-03 16:35:17.600805+00:00'
            , 'result': {
                'fields': {'created': {'count': 0, 'sample': []}, 'updated': {'count': 0, 'sample': []}}
                , 'values': {'created': {'count': 0, 'sample': []}, 'updated': {'count': 1, 'sample': [{'field_key': 'sdk-test-1', 'object_key': '131.schema_new.table_2'}]}}
                , 'created_object_attribution': {'success_count': 0, 'failure_count': 0, 'success_sample': [], 'failure_sample': []}
                , 'flag_counts': {'GOOD': 0, 'WARNING': 1, 'ALERT': 0}
                , 'total_duration': 0.07003468499897281
            }
        }

        # Transformation
        input_transformed = JobDetailsDataQuality(**input)

        # Expected Output
        output = JobDetailsDataQuality(
            status='successful'
            , msg='Job finished in 0.067679 seconds at 2024-07-03 16:35:17.600805+00:00'
            , result = JobDetailsDataQualityResult(
                fields = JobDetailsDataQualityResultAction(
                    created = JobDetailsDataQualityResultActionStats(
                        count = 0
                        , sample = []
                    )
                    , updated = JobDetailsDataQualityResultActionStats(
                        count = 0
                        , sample = []
                    )
                )
                , values = JobDetailsDataQualityResultAction(
                    created = JobDetailsDataQualityResultActionStats(
                        count = 0
                        , sample = []
                    )
                    , updated = JobDetailsDataQualityResultActionStats(
                        count = 1
                        , sample = [{'field_key': 'sdk-test-1', 'object_key': '131.schema_new.table_2'}]
                    )
                )
                , created_object_attribution = JobDetailsDataQualityResultCreatedObjectAttribution(
                    success_count = 0
                    , failure_count = 0
                    , success_sample = []
                    , failure_sample = []
                )
                , flag_counts = {'GOOD': 0, 'WARNING': 1, 'ALERT': 0}
                , total_duration = 0.07003468499897281
            )
        )

        self.assertEqual(input_transformed, output)

    def test_job_model_for_document_hub_folder_post(self):

        # Expected input
        input = {
            "status": "successful",
            "msg": "Job finished in 0.40343 seconds at 2024-08-16 16:19:11.482905+00:00",
            "result": {
                "created_folder_count": 2,
                "created_folders": [
                    {
                        "id": 10,
                        "title": "my test folder"
                    },
                    {
                        "id": 11,
                        "title": "my test folder 2"
                    }
                ]
            }
        }

        # Transformation
        input_transformed = JobDetailsDocumentHubFolderPost(**input)

        # Expected Output
        output = JobDetailsDocumentHubFolderPost(
            status='successful'
            , msg='Job finished in 0.40343 seconds at 2024-08-16 16:19:11.482905+00:00'
            , result = JobDetailsDocumentHubFolderPostResult(
                created_folder_count = 2
                , created_folders = [
                    JobDetailsDocumentHubFolderPostResultCreatedFolder(
                        id = 10
                        , title = "my test folder"
                    )
                    , JobDetailsDocumentHubFolderPostResultCreatedFolder(
                        id = 11
                        , title = "my test folder 2"
                    )
                ]
            )
        )

        self.assertEqual(input_transformed, output)

    def test_job_model_for_document_hub_folder_put(self):

        # Expected input
        input = {
            "status": "successful",
            "msg": "Job finished in 0.40343 seconds at 2024-08-16 16:19:11.482905+00:00",
            "result": {
                "updated_folder_count": 2,
                "updated_folders": [
                    {
                        "id": 10,
                        "title": "my test folder"
                    },
                    {
                        "id": 11,
                        "title": "my test folder 2"
                    }
                ]
            }
        }

        # Transformation
        input_transformed = JobDetailsDocumentHubFolderPut(**input)

        # Expected Output
        output = JobDetailsDocumentHubFolderPut(
            status='successful'
            , msg='Job finished in 0.40343 seconds at 2024-08-16 16:19:11.482905+00:00'
            , result = JobDetailsDocumentHubFolderPutResult(
                updated_folder_count = 2
                , updated_folders = [
                    JobDetailsDocumentHubFolderPutResultUpdatedFolder(
                        id = 10
                        , title = "my test folder"
                    )
                    , JobDetailsDocumentHubFolderPutResultUpdatedFolder(
                        id = 11
                        , title = "my test folder 2"
                    )
                ]
            )
        )

        self.assertEqual(input_transformed, output)

    def test_job_model_for_document_hub_folder_delete(self):

        # Expected input
        input = {
            'status': 'successful'
            , 'msg': 'Job finished in 0.40343 seconds at 2024-08-16 16:19:11.482905+00:00'
            , 'result': {
                "deleted_folder_count": 2,
                "deleted_folder_ids": [
                    11, 12
                ]
            }
        }

        # Transformation
        input_transformed = JobDetailsDocumentHubFolderDelete(**input)

        # Expected Output
        output = JobDetailsDocumentHubFolderDelete(
            status='successful'
            , msg='Job finished in 0.40343 seconds at 2024-08-16 16:19:11.482905+00:00'
            , result= JobDetailsDocumentHubFolderDeleteResult(
                deleted_folder_count = 2
                , deleted_folder_ids = [
                    11, 12
                ]
            )
        )

        self.assertEqual(input_transformed, output)