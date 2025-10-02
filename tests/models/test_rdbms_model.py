"""Test the Alation REST API Relational Integration Models"""

import unittest
from allie_sdk.models.rdbms_model import *
from allie_sdk.models.custom_field_model import *


class TestRDBMSModels(unittest.TestCase):

    def test_schema(self):

        schema_response = {
            "id": 6,
            "name": "test_name",
            "title": "Test title",
            "description": "This is a test description",
            "ds_id": 7,
            "key": "7.test_name",
            "url": "/schema/6/",
            "custom_fields": [{
                "value": [
                    {"otype": "user", "oid": 2},
                    {"otype": "user", "oid": 20},
                    {"otype": "user", "oid": 19}
                ],
                "field_id": 8,
                "field_name": "Steward"}],
            "db_comment": None
        }
        schema = Schema.from_api_response(schema_response)

        mock_schema = Schema(
            id=6,
            name="test_name",
            title="Test title",
            description="This is a test description",
            ds_id=7,
            key="7.test_name",
            url="/schema/6/",
            custom_fields= [{
                "value": [
                    {"otype": "user", "oid": 2},
                    {"otype": "user", "oid": 20},
                    {"otype": "user", "oid": 19}
                ],
                "field_id": 8,
                "field_name": "Steward"}]
        )

        self.assertEqual(schema, mock_schema)

    def test_schema_item_payload(self):

        mock_schema = SchemaItem(
            key='1.schema_test.public',
            title='This is a test',
            description='Very Nice!',
            db_comment="A schema for testing",
            custom_fields=[
                CustomFieldValueItem(field_id=1, value=CustomFieldStringValueItem(value="Testing")),
                CustomFieldValueItem(field_id=2, value=[CustomFieldDictValueItem(otype='Table', oid=5)])
            ]
        )
        expected_payload = {
            'key': '1.schema_test.public', 'title': 'This is a test', 'description': 'Very Nice!',
            'db_comment': 'A schema for testing',
            'custom_fields': [
                {'field_id':1, 'value': 'Testing'},
                {'field_id': 2, 'value': [{'otype': 'table', 'oid': 5}]}
            ]
        }

        self.assertEqual(mock_schema.generate_api_post_payload(), expected_payload)

    def test_schema_payload_exception_missing_key(self):

        mock_schema = SchemaItem(
            title='This is a test',
            description='Very Nice!',
            db_comment="A schema for testing",
            custom_fields=[
                CustomFieldValueItem(field_id=1, value=[CustomFieldStringValueItem(value="Testing")]),
                CustomFieldValueItem(field_id=2, value=[CustomFieldDictValueItem(otype='Table', oid=5)])
            ]
        )

        self.assertRaises(InvalidPostBody, lambda: mock_schema.generate_api_post_payload())

    def test_table(self):

        table_response = {
            "id": 93,
            "name": "test_title",
            "title": "Test Table Title",
            "description": "Test Table Description",
            "ds_id": 6,
            "key": "6.TEST_SCHEMA.PUBLIC.MOCK_TABLE",
            "url": "/table/93/",
            "custom_fields": [{
                "value": [
                    {"otype": "user", "oid": 21},
                    {"otype": "user", "oid": 11},
                    {"otype": "user", "oid": 2},
                    {"otype": "user", "oid": 25}
                ],
                "field_id": 8,
                "field_name": "Steward"}],
            "table_type": "TABLE",
            "schema_id": 5,
            "schema_name": "TEST_SCHEMA.PUBLIC",
            "base_table_key": None,
            "sql": None,
            "partition_columns": [],
            "partition_definition": None,
            "table_comment": "Schema for Integration Testing"
        }
        table = Table.from_api_response(table_response)

        mock_table = Table(
            id=93,
            name="test_title",
            title="Test Table Title",
            description="Test Table Description",
            ds_id=6,
            key="6.TEST_SCHEMA.PUBLIC.MOCK_TABLE",
            url="/table/93/",
            custom_fields= [{
                "value": [
                    {"otype": "user", "oid": 21},
                    {"otype": "user", "oid": 11},
                    {"otype": "user", "oid": 2},
                    {"otype": "user", "oid": 25}
                ],
                "field_id": 8,
                "field_name": "Steward"}],
            table_type="TABLE",
            schema_id=5,
            schema_name="TEST_SCHEMA.PUBLIC",
            table_comment="Schema for Integration Testing"
        )

        self.assertEqual(table, mock_table)

    def test_table_item_payload(self):

        mock_table = TableItem(
            key='1.schema_test.public.table',
            title='This is a test',
            description='Very Nice!',
            table_comment='This is a test table',
            table_type="SYNONYM",
            base_table_key='1.test.base',
            owner='Alation_PS',
            sql="select * from test.test",
            custom_fields=[
                CustomFieldValueItem(field_id=1, value=CustomFieldStringValueItem(value="Testing")),
                CustomFieldValueItem(field_id=2, value=[CustomFieldDictValueItem(otype='Table', oid=5)])
            ]
        )
        expected_payload = {
            "key": "1.schema_test.public.table", "title": 'This is a test',
            "description": "Very Nice!", "table_comment": "This is a test table",
            "table_type": "SYNONYM", "base_table_key": "1.test.base", "owner": "Alation_PS",
            "sql": "select * from test.test",
            'custom_fields': [
                {'field_id': 1, 'value': 'Testing'},
                {'field_id': 2, 'value': [{'otype': 'table', 'oid': 5}]}
            ]
        }

        self.assertEqual(mock_table.generate_api_post_payload(), expected_payload)

    def test_table_payload_exception_missing_key(self):

        mock_table = TableItem(
            title='This is a test',
            description='Very Nice!',
            table_comment='This is a test table',
            table_type="SYNONYM",
            base_table_key='1.test.base',
            owner='Alation_PS',
            sql="select * from test.test",
            custom_fields=[
                CustomFieldValueItem(field_id=1, value=[CustomFieldStringValueItem(value="Testing")]),
                CustomFieldValueItem(field_id=2, value=[CustomFieldDictValueItem(otype='Table', oid=5)])
            ]
        )

        self.assertRaises(InvalidPostBody, lambda: mock_table.generate_api_post_payload())

    def test_table_patch_item_payload(self):

        mock_table = TablePatchItem(
            id=123,
            title='Updated Title',
            description='Updated Description',
            table_comment='Updated comment',
            table_type='VIEW',
            table_type_name='View',
            owner='Alation_PS',
            sql='select 1',
            base_table_key='1.test.base',
            partition_definition='P1',
            partition_columns=['col_a', 'col_b'],
            custom_fields=[
                CustomFieldValueItem(field_id=1, value=CustomFieldStringValueItem(value='Testing')),
                CustomFieldValueItem(field_id=2, value=[CustomFieldDictValueItem(otype='Table', oid=5)])
            ]
        )

        expected_payload = {
            'id': 123,
            'title': 'Updated Title',
            'description': 'Updated Description',
            'table_comment': 'Updated comment',
            'table_type': 'VIEW',
            'table_type_name': 'View',
            'owner': 'Alation_PS',
            'sql': 'select 1',
            'base_table_key': '1.test.base',
            'partition_definition': 'P1',
            'partition_columns': ['col_a', 'col_b'],
            'custom_fields': [
                {'field_id': 1, 'value': 'Testing'},
                {'field_id': 2, 'value': [{'otype': 'table', 'oid': 5}]}
            ]
        }

        self.assertEqual(mock_table.generate_api_patch_payload(), expected_payload)

    def test_table_patch_item_exception_missing_id(self):

        mock_table = TablePatchItem(
            title='Updated Title'
        )

        self.assertRaises(InvalidPostBody, lambda: mock_table.generate_api_patch_payload())

    def test_column(self):

        column_response = {
            "id": 1613,
            "name": "CUSTOMER_NAME",
            "title": "Customer Name",
            "description": "<p>This is the customer name</p>",
            "ds_id": 6,
            "key": "6.SUPERSTORE.PUBLIC.SUPERSTORE_REPORTING.CUSTOMER_NAME",
            "url": "/attribute/1613/",
            "custom_fields": [
                {"value": [{"otype": "user", "oid": 18}], "field_id": 8, "field_name": "Steward"},
                {"value": "PII", "field_id": 10087, "field_name": "PII (Personally Identifiable Information)"},
                {"value": "PCI", "field_id": 10089, "field_name": "PCI (Personal Credit Information)"},
                {"value": "No", "field_id": 10039, "field_name": "CDE (Critical Data Element)"},
                {"value": "No", "field_id": 10088, "field_name": "PHI (Protected Health Information)"}
            ],
            "column_type": "VARCHAR(100)",
            "column_comment": "This is a comment",
            "index": {"isPrimaryKey": False, "isForeignKey": False,
                      "referencedColumnId": None, "isOtherIndex": False,},
            "nullable": True,
            "schema_id": 5,
            "table_id": 91,
            "table_name": "superstore.public.superstore_reporting",
            "position": 7
        }
        column = Column.from_api_response(column_response)

        mock_column = Column(
            id=1613,
            name="CUSTOMER_NAME",
            title="Customer Name",
            description="<p>This is the customer name</p>",
            ds_id=6,
            key="6.SUPERSTORE.PUBLIC.SUPERSTORE_REPORTING.CUSTOMER_NAME",
            url="/attribute/1613/",
            custom_fields=[
                {"value": [{"otype": "user", "oid": 18}], "field_id": 8, "field_name": "Steward"},
                {"value": "PII", "field_id": 10087, "field_name": "PII (Personally Identifiable Information)"},
                {"value": "PCI", "field_id": 10089, "field_name": "PCI (Personal Credit Information)"},
                {"value": "No", "field_id": 10039, "field_name": "CDE (Critical Data Element)"},
                {"value": "No", "field_id": 10088, "field_name": "PHI (Protected Health Information)"}
            ],
            column_type="VARCHAR(100)",
            index={"isPrimaryKey": False, "isForeignKey": False,
                   "referencedColumnId": None, "isOtherIndex": False},
            nullable=True,
            schema_id=5,
            table_id=91,
            column_comment="This is a comment",
            table_name="superstore.public.superstore_reporting",
            position=7
        )

        self.assertEqual(column, mock_column)

    def test_column_index_parsing(self):

        mock_column = Column(
            index = {"isPrimaryKey": False, "isForeignKey": True,
                     "referencedColumnId": "1.Test.Table", "isOtherIndex": False},
        )
        expected_index = ColumnIndex(
            isPrimaryKey=False,
            isForeignKey=True,
            isOtherIndex=False,
            referencedColumnId="1.Test.Table"
        )

        self.assertEqual(mock_column.index, expected_index)

    def test_column_item_payload(self):

        mock_column = ColumnItem(
            title="Customer Name",
            description="<p>This is the customer name</p>",
            key="6.SUPERSTORE.PUBLIC.SUPERSTORE_REPORTING.CUSTOMER_NAME",
            custom_fields=[
                CustomFieldValueItem(field_id=1, value=CustomFieldStringValueItem(value="Testing")),
                CustomFieldValueItem(field_id=2, value=[CustomFieldDictValueItem(otype='Table', oid=5)])
            ],
            column_type="VARCHAR(100)",
            index=ColumnIndex(
                isPrimaryKey=False,
                isForeignKey=True,
                isOtherIndex=False,
                referencedColumnId="1.Test.Table"
            ),
            nullable=False,
            position=7
        )
        expected_payload = {
            "key": "6.SUPERSTORE.PUBLIC.SUPERSTORE_REPORTING.CUSTOMER_NAME", "title": "Customer Name",
            "description": "<p>This is the customer name</p>", "column_type": "VARCHAR(100)",
            "nullable": False, "position": 7,
            "index": {"isPrimaryKey": False, "isForeignKey": True, "isOtherIndex": False,
                      "referencedColumnId": "1.Test.Table"},
            "custom_fields":  [
                {'field_id': 1, 'value': 'Testing'},
                {'field_id': 2, 'value': [{'otype': 'table', 'oid': 5}]}
            ]
        }

        self.assertEqual(mock_column.generate_api_post_payload(), expected_payload)

    def test_column_item_exception_missing_key(self):

        mock_column = ColumnItem(
            title="Customer Name",
            description="<p>This is the customer name</p>",
            custom_fields=[
                CustomFieldValueItem(field_id=1, value=CustomFieldStringValueItem(value="Testing")),
                CustomFieldValueItem(field_id=2, value=[CustomFieldDictValueItem(otype='Table', oid=5)])
            ],
            column_type="VARCHAR(100)",
            index=ColumnIndex(
                isPrimaryKey=False,
                isForeignKey=True,
                isOtherIndex=False,
                referencedColumnId="1.Test.Table"
            ),
            nullable=False,
            position=7
        )

        self.assertRaises(InvalidPostBody, lambda: mock_column.generate_api_post_payload())

    def test_column_item_exception_missing_column_type(self):

        mock_column = ColumnItem(
            title="Customer Name",
            description="<p>This is the customer name</p>",
            key="6.SUPERSTORE.PUBLIC.SUPERSTORE_REPORTING.CUSTOMER_NAME",
            custom_fields=[
                CustomFieldValue(field_id=1, value=CustomFieldStringValueItem(value="Testing")),
                CustomFieldValue(field_id=2, value=[CustomFieldDictValueItem(otype='Table', oid=5)])
            ],
            index=ColumnIndex(
                isPrimaryKey=False,
                isForeignKey=True,
                isOtherIndex=False,
                referencedColumnId="1.Test.Table"
            ),
            nullable=False,
            position=7
        )

        self.assertRaises(InvalidPostBody, lambda: mock_column.generate_api_post_payload())

    def test_column_patch_item_payload(self):
        mock_column = ColumnPatchItem(
            id=1,
            title="Customer Name",
            description="<p>This is the customer name</p>",
            custom_fields=[
                CustomFieldValueItem(field_id=1, value=CustomFieldStringValueItem(value="Testing")),
                CustomFieldValueItem(field_id=2, value=[CustomFieldDictValueItem(otype='Table', oid=5)])
            ],
            column_comment="This is a comment",
            nullable=False,
            position=7,
            index=ColumnIndex(
                isPrimaryKey=False,
                isForeignKey=True,
                isOtherIndex=False,
                referencedColumnId="1.Test.Table"
            )
        )
        expected_payload = {
            "id": 1,
            "title": "Customer Name",
            "description": "<p>This is the customer name</p>",
            "column_comment": "This is a comment",
            "nullable": False,
            "position": 7,
            "index": {
                "isPrimaryKey": False
                , "isForeignKey": True
                , "isOtherIndex": False
                , "referencedColumnId": "1.Test.Table"
            },
            "custom_fields": [
                {'field_id': 1, 'value': 'Testing'},
                {'field_id': 2, 'value': [{'otype': 'table', 'oid': 5}]}
            ]
        }

        self.assertEqual(mock_column.generate_api_patch_payload(), expected_payload)

    def test_column_patch_item_exception_missing_id(self):
        mock_column = ColumnPatchItem(
            title="Customer Name",
            description="<p>This is the customer name</p>"
        )

        self.assertRaises(InvalidPostBody, lambda: mock_column.generate_api_patch_payload())

    def test_base_rdbms_custom_field_parsing(self):

        mock_base = BaseRDBMS(
            custom_fields=[
                {"value": [{"otype": "user", "oid": 18}], "field_id": 8, "field_name": "Steward"},
                {"value": "PII", "field_id": 10087, "field_name": "PII (Personally Identifiable Information)"},
            ]
        )
        expected_custom_fields = [
            CustomFieldValue(
                field_id=8,
                field_name="Steward",
                value=[CustomFieldDictValue(otype='user', oid=18)]
            ),
            CustomFieldValue(
                field_id=10087,
                field_name="PII (Personally Identifiable Information)",
                value= CustomFieldStringValue(value="PII")
            )
        ]

        self.assertEqual(mock_base.custom_fields, expected_custom_fields)


if __name__ == '__main__':
    unittest.main()
