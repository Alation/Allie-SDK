"""Test the Alation REST API Relational Integration Methods."""

import requests_mock
import unittest
from allie_sdk.methods.rdbms import *

MOCK_RDBMS = AlationRDBMS(
    access_token='test', session=requests.session(), host='https://test.com'
)


class TestRDBMS(unittest.TestCase):

    @requests_mock.Mocker()
    def test_success_get_schemas(self, m):

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
        m.register_uri('GET', '/integration/v2/schema/?id=5', json=success_response)
        schemas = MOCK_RDBMS.get_schemas(mock_params)

        self.assertEqual(success_schemas, schemas)

    @requests_mock.Mocker()
    def test_failed_get_schemas(self, m):

        failed_response = {
            "detail": "Invalid query parameters: [ids]",
            "code": "400006"
        }
        m.register_uri('GET', '/integration/v2/schema/', json=failed_response, status_code=400)
        schemas = MOCK_RDBMS.get_schemas()

        self.assertIsNone(schemas)

    @requests_mock.Mocker()
    def test_success_post_schemas(self, m):

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
        m.register_uri('POST', '/integration/v2/schema/?ds_id=1', json=async_response)
        m.register_uri('GET', '/api/v1/bulk_metadata/job/?id=1', json=job_response)
        async_result = MOCK_RDBMS.post_schemas(1, mock_schema_list)

        self.assertTrue(async_result)

    @requests_mock.Mocker()
    def test_failed_post_schemas(self, m):

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
        m.register_uri('POST', '/integration/v2/schema/?ds_id=1',
                       json=failed_response, status_code=400)
        async_response = MOCK_RDBMS.post_schemas(1, mock_schema_list)

        self.assertFalse(async_response)

    @requests_mock.Mocker()
    def test_success_get_tables(self, m):

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
        m.register_uri('GET', '/integration/v2/table/?id=93', json=success_response)
        tables = MOCK_RDBMS.get_tables(mock_params)

        self.assertEqual(success_tables, tables)

    @requests_mock.Mocker()
    def test_failed_get_tables(self, m):

        failed_response = {
            "detail": "Invalid query parameters: [ids]",
            "code": "400006"
        }
        m.register_uri('GET', '/integration/v2/table/', json=failed_response, status_code=400)
        tables = MOCK_RDBMS.get_tables()

        self.assertIsNone(tables)

    @requests_mock.Mocker()
    def test_success_post_tables(self, m):

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

        m.register_uri('POST', '/integration/v2/table/?ds_id=1', json=async_response)
        m.register_uri('GET', '/api/v1/bulk_metadata/job/?id=1', json=job_response)
        async_result = MOCK_RDBMS.post_tables(1, mock_table_list)

        self.assertTrue(async_result)

    @requests_mock.Mocker()
    def test_failed_post_tables(self, m):

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
        m.register_uri('POST', '/integration/v2/table/?ds_id=1',
                       json=failed_response, status_code=400)
        async_response = MOCK_RDBMS.post_tables(1, mock_table_list)

        self.assertFalse(async_response)

    @requests_mock.Mocker()
    def test_success_get_columns(self, m):

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
        m.register_uri('GET', '/integration/v2/column/?id=1613', json=success_response)
        columns = MOCK_RDBMS.get_columns(mock_params)

        self.assertEqual(success_columns, columns)

    @requests_mock.Mocker()
    def test_failed_get_columns(self, m):

        failed_response = {
            "detail": "Invalid query parameters: [ids]",
            "code": "400006"
        }
        m.register_uri('GET', '/integration/v2/column/', json=failed_response, status_code=400)
        columns = MOCK_RDBMS.get_columns()

        self.assertIsNone(columns)

    @requests_mock.Mocker()
    def test_success_post_columns(self, m):

        mock_column = ColumnItem()
        mock_column.key = '1.schema.test'
        mock_column.title = 'Test Title'
        mock_column.description = 'Test Description'
        mock_column.column_type = 'VARCHAR'
        mock_column_list = [mock_column]

        async_response = {
            "job_id": 1
        }
        job_response = {
            "status": "successful",
            "msg": "Job finished in 6.076855 seconds at 2023-11-30 16:21:37.152796+00:00",
            "result": [
                {
                    "response": "Upserted 2 attribute objects.",
                    "mapping": [
                        {"id": 17634, "key": "9.sales.orders.id"},
                        {"id": 17646, "key": "9.sales.orders.discount"},
                    ],
                    "errors": []
                }
            ]
        }

        m.register_uri('POST', '/integration/v2/column/?ds_id=1', json=async_response)
        m.register_uri('GET', '/api/v1/bulk_metadata/job/?id=1', json=job_response)
        async_result = MOCK_RDBMS.post_columns(1, mock_column_list)

        self.assertTrue(async_result)

    @requests_mock.Mocker()
    def test_failed_post_columns(self, m):

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
        m.register_uri('POST', '/integration/v2/column/?ds_id=1',
                       json=failed_response, status_code=400)
        async_response = MOCK_RDBMS.post_columns(1, mock_column_list)

        self.assertFalse(async_response)


if __name__ == '__main__':
    unittest.main()
