"""Test the Alation REST API Relational Integration Methods."""

import requests_mock
import unittest
from allie_sdk.methods.rdbms import *

class TestRDBMS(unittest.TestCase):

    def setUp(self):
        self.mock_user = AlationRDBMS(
            access_token='test',
            session=requests.session(),
            host='https://test.com'
        )

    @requests_mock.Mocker()
    def test_success_get_schemas(self, requests_mock):

        mock_params = SchemaParams()
        mock_params.id.add(5)
        success_response = [
            {
                "id": 5,
                "name": "SUPERSTORE.PUBLIC",
                "title": "Superstore EDW",
                "description": "Test Description",
                "ds_id": 6,
                "key": "6.SUPERSTORE.PUBLIC",
                "url": "/schema/5/",
                "custom_fields": [
                    {
                        "value": [
                            {"otype": "user", "oid": 11},
                            {"otype": "user", "oid": 2},
                            {"otype": "user", "oid": 25},
                            {"otype": "user", "oid": 19},
                            {"otype": "user", "oid": 24}
                        ],
                        "field_id": 8,
                        "field_name": "Steward"
                    }
                ],
                "db_comment": None
            }
        ]
        success_schemas = [Schema.from_api_response(item) for item in success_response]
        requests_mock.register_uri('GET', '/integration/v2/schema/?id=5', json=success_response)
        schemas = self.mock_user.get_schemas(mock_params)

        self.assertEqual(success_schemas, schemas)

    @requests_mock.Mocker()
    def test_failed_get_schemas(self, requests_mock):

        failed_response = {
            "detail": "Invalid query parameters: [ids]",
            "code": "400006"
        }
        requests_mock.register_uri('GET', '/integration/v2/schema/', json=failed_response, status_code=400)
        
        # The method should now raise an HTTPError for non-200 status codes
        with self.assertRaises(requests.exceptions.HTTPError):
            self.mock_user.get_schemas()

    @requests_mock.Mocker()
    def test_success_post_schemas(self, requests_mock):

        mock_schema = SchemaItem()
        mock_schema.key = '1.schema.test'
        mock_schema.title = 'Test Title'
        mock_schema.description = 'Test Description'
        mock_schema_list = [mock_schema]

        async_response = {
            "job_id": 1
        }
        job_response = {
            "status": "successful",
            "msg": "Job finished in 0.335952 seconds at 2023-11-30 15:55:16.125679+00:00",
            "result": [
                {
                    "response": "Upserted 2 schema objects.",
                    "mapping": [
                        {"id": 17, "key": "9.sales"},
                        {"id": 18, "key": "9.human_resources"}
                    ],
                    "errors": []
                }
            ]
        }
        requests_mock.register_uri('POST', '/integration/v2/schema/?ds_id=1', json=async_response)
        requests_mock.register_uri('GET', '/api/v1/bulk_metadata/job/?id=1', json=job_response)
        async_result = self.mock_user.post_schemas(1, mock_schema_list)

        input_transformed = [JobDetailsRdbms(**job_response)]
        # self.assertTrue(async_result)
        self.assertEqual(input_transformed, async_result)

    @requests_mock.Mocker()
    def test_failed_post_schemas(self, requests_mock):
        mock_schema = SchemaItem()
        mock_schema.key = '1.schema.test'
        mock_schema.title = 'Test Title'
        mock_schema.description = 'Test Description'
        mock_schema_list = [mock_schema]

        failed_response = {
            "detail": "Incorrect input data. Please fix the errors and post the data.",
            "errors": [
                {
                    "key": [
                        "400068: API Key is a required input"
                    ]
                }
            ],
            "code": "400010"
        }
        requests_mock.register_uri('POST', '/integration/v2/schema/?ds_id=1',
                      json=failed_response, status_code=400)
        
        # Now we expect an HTTPError to be raised
        with self.assertRaises(requests.exceptions.HTTPError) as context:
            self.mock_user.post_schemas(ds_id=1, schemas=mock_schema_list)

        # Verify the error response contains expected information
        self.assertEqual(context.exception.response.status_code, 400)

    @requests_mock.Mocker()
    def test_success_patch_schemas(self, requests_mock):

        schemas = [
            SchemaPatchItem(
                id=1,
                title='Updated Schema Title',
                description='Updated description for schema',
                db_comment='New database comment'
            )
        ]

        async_response = {
            "job_id": 27808
        }

        requests_mock.register_uri(
            method='PATCH',
            url='/integration/v2/schema/?ds_id=1',
            json=async_response,
            status_code=202
        )

        job_api_response = {
            "status": "successful",
            "msg": "Job finished in 5.01234 seconds at 2023-11-30 16:15:20.000000+00:00",
            "result": [
                {
                    "response": "Updated 1 schema objects.",
                    "mapping": [
                        {"id": 1, "key": "1.ORDERS"}
                    ],
                    "errors": []
                }
            ]
        }

        requests_mock.register_uri(
            method='GET',
            url='/api/v1/bulk_metadata/job/?id=27808',
            json=job_api_response
        )

        async_result = self.mock_user.patch_schemas(
            ds_id=1,
            schemas=schemas
        )

        expected_result = [
            JobDetailsRdbms(
                status="successful",
                msg="Job finished in 5.01234 seconds at 2023-11-30 16:15:20.000000+00:00",
                result=[
                    JobDetailsRdbmsResult(
                        response="Updated 1 schema objects.",
                        mapping=[
                            JobDetailsRdbmsResultMapping(
                                id=1,
                                key="1.ORDERS"
                            )
                        ],
                        errors=[]
                    )
                ]
            )
        ]

        self.assertEqual(expected_result, async_result)

    @requests_mock.Mocker()
    def test_failed_patch_schemas(self, requests_mock):
        mock_schema = SchemaPatchItem(id=1)
        mock_schema_list = [mock_schema]

        failed_response = {
            "detail": "Incorrect input data. Please fix the errors and post the data.",
            "errors": [
                {
                    "id": [
                        "400068: id is a required input"
                    ]
                }
            ],
            "code": "400010"
        }

        requests_mock.register_uri('PATCH', '/integration/v2/schema/?ds_id=1',
                      json=failed_response, status_code=400)

        with self.assertRaises(requests.exceptions.HTTPError) as context:
            self.mock_user.patch_schemas(ds_id=1, schemas=mock_schema_list)

        self.assertEqual(context.exception.response.status_code, 400)

    @requests_mock.Mocker()
    def test_success_get_tables(self, requests_mock):

        mock_params = TableParams()
        mock_params.id.add(93)
        success_response = [
            {
                "id": 93,
                "name": "SALES_TARGETS",
                "title": "Sales Targets",
                "description": "Test Description",
                "ds_id": 6,
                "key": "6.SUPERSTORE.PUBLIC.SALES_TARGETS",
                "url": "/table/93/",
                "custom_fields": [
                    {
                        "value": [
                            {"otype": "user", "oid": 21},
                            {"otype": "user", "oid": 11},
                            {"otype": "user", "oid": 2},
                            {"otype": "user", "oid": 25}
                        ],
                        "field_id": 8,
                        "field_name": "Steward"
                    }
                ],
                "table_type": "TABLE",
                "schema_id": 5,
                "schema_name": "SUPERSTORE.PUBLIC",
                "base_table_key": None,
                "sql": None,
                "partition_columns": [],
                "partition_definition": None,
                "table_comment": "Superstore Sales Target Data"
            }
        ]
        success_tables = [Table.from_api_response(item) for item in success_response]
        requests_mock.register_uri('GET', '/integration/v2/table/?id=93', json=success_response)
        tables = self.mock_user.get_tables(mock_params)

        self.assertEqual(success_tables, tables)

    @requests_mock.Mocker()
    def test_failed_get_tables(self, requests_mock):

        failed_response = {
            "detail": "Invalid query parameters: [ids]",
            "code": "400006"
        }
        requests_mock.register_uri('GET', '/integration/v2/table/', json=failed_response, status_code=400)
        
        # The method should now raise an HTTPError for non-200 status codes
        with self.assertRaises(requests.exceptions.HTTPError):
            self.mock_user.get_tables()

    @requests_mock.Mocker()
    def test_success_post_tables(self, requests_mock):

        mock_table = TableItem()
        mock_table.key = '1.schema.test'
        mock_table.title = 'Test Title'
        mock_table.description = 'Test Description'
        mock_table_list = [mock_table]

        async_response = {
            "job_id": 1
        }

        job_response = {
            "status": "successful",
            "msg": "Job finished in 1.94582 seconds at 2023-11-30 16:09:48.515164+00:00",
            "result": [
                {
                    "response": "Upserted 8 table objects.",
                    "mapping": [
                        {"id": 1049, "key": "9.sales.returns"},
                        {"id": 1048, "key": "9.sales.sales_commissions"},
                        {"id": 1047, "key": "9.sales.orders"},
                        {"id": 1046, "key": "9.sales.sales_targets"},
                        {"id": 1053, "key": "9.human_resources.salaries"},
                        {"id": 1052, "key": "9.human_resources.titles"},
                        {"id": 1051, "key": "9.human_resources.employees"},
                        {"id": 1050, "key": "9.sales.executive_reporting"}
                    ],
                    "errors": []
                }
            ]
        }

        requests_mock.register_uri('POST', '/integration/v2/table/?ds_id=1', json=async_response)
        requests_mock.register_uri('GET', '/api/v1/bulk_metadata/job/?id=1', json=job_response)
        async_result = self.mock_user.post_tables(1, mock_table_list)

        input_transformed = [JobDetailsRdbms(**job_response)]
        # self.assertTrue(async_result)
        self.assertEqual(input_transformed, async_result)

    @requests_mock.Mocker()
    def test_failed_post_tables(self, requests_mock):
        mock_table = TableItem()
        mock_table.key = '1.schema.test'
        mock_table.title = 'Test Title'
        mock_table.description = 'Test Description'
        mock_table_list = [mock_table]

        failed_response = {
            "detail": "Incorrect input data. Please fix the errors and post the data.",
            "errors": [
                {
                    "key": [
                        "400068: API Key is a required input"
                    ]
                }
            ],
            "code": "400010"
        }
        requests_mock.register_uri('POST', '/integration/v2/table/?ds_id=1',
                      json=failed_response, status_code=400)
        
        # Now we expect an HTTPError to be raised
        with self.assertRaises(requests.exceptions.HTTPError) as context:
            self.mock_user.post_tables(ds_id=1, tables=mock_table_list)

        # Verify the error response contains expected information
        self.assertEqual(context.exception.response.status_code, 400)

    @requests_mock.Mocker()
    def test_success_patch_tables(self, requests_mock):

        tables = [
            TablePatchItem(
                id=1,
                title='Updated Table Title',
                description='Updated Table Description',
                table_comment='Updated comment'
            )
        ]

        async_response = {
            "job_id": 27810
        }

        requests_mock.register_uri(
            method='PATCH',
            url='/integration/v2/table/?ds_id=1',
            json=async_response,
            status_code=202
        )

        job_api_response = {
            "status": "successful",
            "msg": "Job finished in 5.000000 seconds at 2023-11-30 16:21:37.152796+00:00",
            "result": [
                {
                    "response": "Updated 1 table objects.",
                    "mapping": [
                        {"id": 1, "key": "1.schema.table"}
                    ],
                    "errors": []
                }
            ]
        }

        requests_mock.register_uri(
            method='GET',
            url='/api/v1/bulk_metadata/job/?id=27810',
            json=job_api_response
        )

        async_result = self.mock_user.patch_tables(
            ds_id=1,
            tables=tables
        )

        expected_result = [
            JobDetailsRdbms(
                status="successful",
                msg="Job finished in 5.000000 seconds at 2023-11-30 16:21:37.152796+00:00",
                result=[
                    JobDetailsRdbmsResult(
                        response="Updated 1 table objects.",
                        mapping=[
                            JobDetailsRdbmsResultMapping(
                                id=1,
                                key="1.schema.table"
                            )
                        ],
                        errors=[]
                    )
                ]
            )
        ]

        self.assertEqual(expected_result, async_result)

    @requests_mock.Mocker()
    def test_failed_patch_tables(self, requests_mock):
        mock_table = TablePatchItem(id=1)
        mock_table_list = [mock_table]

        failed_response = {
            "detail": "Incorrect input data. Please fix the errors and post the data.",
            "errors": [
                {
                    "id": [
                        "400068: id is a required input"
                    ]
                }
            ],
            "code": "400010",
        }

        requests_mock.register_uri('PATCH', '/integration/v2/table/?ds_id=1',
                      json=failed_response, status_code=400)

        with self.assertRaises(requests.exceptions.HTTPError) as context:
            self.mock_user.patch_tables(ds_id=1, tables=mock_table_list)

        self.assertEqual(context.exception.response.status_code, 400)

    @requests_mock.Mocker()
    def test_success_get_columns(self, requests_mock):

        mock_params = ColumnParams()
        mock_params.id.add(1613)
        success_response = [
            {
                "id": 1613,
                "name": "CUSTOMER_NAME",
                "title": "Customer Name",
                "description": "<p>This is the customer name</p>",
                "ds_id": 6,
                "key": "6.SUPERSTORE.PUBLIC.SUPERSTORE_REPORTING.CUSTOMER_NAME",
                "url": "/attribute/1613/",
                "custom_fields": [
                    {
                        "value": [{"otype": "user", "oid": 18}],
                        "field_id": 8,
                        "field_name": "Steward"
                    },
                    {
                        "value": "PII",
                        "field_id": 10087,
                        "field_name": "PII (Personally Identifiable Information)"
                    },
                    {
                        "value": "PCI",
                        "field_id": 10089,
                        "field_name": "PCI (Personal Credit Information)"
                    },
                    {
                        "value": "No",
                        "field_id": 10039,
                        "field_name": "CDE (Critical Data Element)"
                    },
                    {
                        "value": "No",
                        "field_id": 10088,
                        "field_name": "PHI (Protected Health Information)"
                    }
                ],
                "column_type": "VARCHAR(100)",
                "column_comment": None,
                "index": {"isPrimaryKey": False, "isForeignKey": False,
                          "referencedColumnId": None, "isOtherIndex": False},
                "nullable": True,
                "schema_id": 5,
                "table_id": 91,
                "table_name": "superstore.public.superstore_reporting",
                "position": 7
            }
        ]
        success_columns = [Column.from_api_response(item) for item in success_response]
        requests_mock.register_uri('GET', '/integration/v2/column/?id=1613', json=success_response)
        columns = self.mock_user.get_columns(mock_params)

        self.assertEqual(success_columns, columns)

    @requests_mock.Mocker()
    def test_failed_get_columns(self, requests_mock):

        failed_response = {
            "detail": "Invalid query parameters: [ids]",
            "code": "400006"
        }
        requests_mock.register_uri('GET', '/integration/v2/column/', json=failed_response, status_code=400)
        
        # The method should now raise an HTTPError for non-200 status codes
        with self.assertRaises(requests.exceptions.HTTPError):
            self.mock_user.get_columns()

    @requests_mock.Mocker()
    def test_success_post_columns(self, requests_mock):

        # --- PREPARE THE TEST SETUP --- #

        # payload for the main request
        columns = [
            ColumnItem(
                key=f"1.ORDERS.refunds.id"
                , column_type="INTEGER"
                , title="ID"
                , description="This is the id column of the refunds table ..."
                , index=ColumnIndex(
                    isPrimaryKey=True
                    , isForeignKey=False
                    , referencedColumnId=None
                    , isOtherIndex=False
                )
            )
        ]


        # What does the response look like for the main request?
        async_response = {
            "job_id": 27809
        }

        # Override the main API call
        requests_mock.register_uri(
            method='POST',
            url='/integration/v2/column/?ds_id=1',
            json=async_response,
            status_code=202
        )

        # What does the response look like for the Job?
        job_api_response = {
            "status": "successful",
            "msg": "Job finished in 6.076855 seconds at 2023-11-30 16:21:37.152796+00:00",
            "result": [
                {
                    "response": "Upserted 1 attribute objects.",
                    "mapping": [
                        {"id": 17634, "key": "1.ORDERS.refunds.id"}
                    ],
                    "errors": []
                }
            ]
        }

        # Override the job API call
        # Note: The id in the job URL corresponds to the task id in document_api_response defined above
        requests_mock.register_uri(
            method='GET'
            , url='/api/v1/bulk_metadata/job/?id=27809'
            , json=job_api_response
        )

        # --- TEST THE FUNCTION --- #
        async_result = self.mock_user.post_columns(
            ds_id = 1
            , columns = columns
        )

        expected_result = [
            JobDetailsRdbms(
                status = "successful"
                , msg = "Job finished in 6.076855 seconds at 2023-11-30 16:21:37.152796+00:00"
                , result = [
                    JobDetailsRdbmsResult(
                        response = "Upserted 1 attribute objects."
                        , mapping = [
                            JobDetailsRdbmsResultMapping(
                                id = 17634
                                , key = "1.ORDERS.refunds.id"
                            )
                        ]
                        , errors = []
                    )
                ]
            )
        ]
        # self.assertTrue(async_result)
        self.assertEqual(expected_result, async_result)

    @requests_mock.Mocker()
    def test_failed_post_columns(self, requests_mock):
        mock_column = ColumnItem()
        mock_column.key = '1.schema.test'
        mock_column.title = 'Test Title'
        mock_column.description = 'Test Description'
        mock_column.column_type = 'VARCHAR'
        mock_column_list = [mock_column]

        failed_response = {
            "detail": "Incorrect input data. Please fix the errors and post the data.",
            "errors": [
                {
                    "key": [
                        "400068: API Key is a required input"
                    ]
                }
            ],
            "code": "400010"
        }
        requests_mock.register_uri('POST', '/integration/v2/column/?ds_id=1',
                      json=failed_response, status_code=400)
        
        # Now we expect an HTTPError to be raised
        with self.assertRaises(requests.exceptions.HTTPError) as context:
            self.mock_user.post_columns(ds_id=1, columns=mock_column_list)
        
        # Verify the error response contains expected information
        self.assertEqual(context.exception.response.status_code, 400)

    @requests_mock.Mocker()
    def test_success_patch_column(self, requests_mock):

        # --- PREPARE THE TEST SETUP --- #

        # payload for the main request
        columns = [
            ColumnPatchItem(
                id=1
                , title='Updated Title'
                , description="This is the id column of the refunds table ..."
                , index=ColumnIndex(
                    isPrimaryKey=True
                    , isForeignKey=False
                    , referencedColumnId=None
                    , isOtherIndex=False
                )
            )
        ]

        # What does the response look like for the main request?
        async_response = {
            "job_id": 27809
        }

        # Override the main API call
        requests_mock.register_uri(
            method='PATCH',
            url='/integration/v2/column/?ds_id=1',
            json=async_response,
            status_code=202
        )

        # What does the response look like for the Job?
        job_api_response = {
            "status": "successful",
            "msg": "Job finished in 6.076855 seconds at 2023-11-30 16:21:37.152796+00:00",
            "result": [
                {
                    "response": "Updated 1 attribute objects.",
                    "mapping": [
                        {"id": 1, "key": "1.ORDERS.refunds.id"}
                    ],
                    "errors": []
                }
            ]
        }

        # Override the job API call
        # Note: The id in the job URL corresponds to the task id in document_api_response defined above
        requests_mock.register_uri(
            method='GET'
            , url='/api/v1/bulk_metadata/job/?id=27809'
            , json=job_api_response
        )

        # --- TEST THE FUNCTION --- #

        async_result = self.mock_user.patch_columns(
            ds_id=1
            , columns = columns
        )

        expected_result = [
            JobDetailsRdbms(
                status="successful"
                , msg="Job finished in 6.076855 seconds at 2023-11-30 16:21:37.152796+00:00"
                , result=[
                    JobDetailsRdbmsResult(
                        response="Updated 1 attribute objects."
                        , mapping=[
                            JobDetailsRdbmsResultMapping(
                                id=1
                                , key="1.ORDERS.refunds.id"
                            )
                        ]
                        , errors=[]
                    )
                ]
            )
        ]

        self.assertEqual(expected_result, async_result)

    @requests_mock.Mocker()
    def test_failed_patch_columns(self, requests_mock):
        mock_column = ColumnPatchItem(id=1)
        mock_column_list = [mock_column]

        failed_response = {
            "detail": "Incorrect input data. Please fix the errors and post the data.",
            "errors": [
                {
                    "id": [
                        "400068: id is a required input"
                    ]
                }
            ],
            "code": "400010",
        }

        requests_mock.register_uri('PATCH', '/integration/v2/column/?ds_id=1',
                      json=failed_response, status_code=400)

        with self.assertRaises(requests.exceptions.HTTPError) as context:
            self.mock_user.patch_columns(ds_id=1, columns=mock_column_list)

        self.assertEqual(context.exception.response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
