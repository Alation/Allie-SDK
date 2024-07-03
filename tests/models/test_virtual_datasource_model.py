"""Test the Alation REST API Virtual Data Source Models."""

import unittest
from allie_sdk.models.virtual_datasource_model import *


class TestVirtualDataSourceModels(unittest.TestCase):

    def test_virtual_data_source_model_schema(self):

        schema_response = {
            "key": "99.SchemaName",
            "description": "Test Schema model",
            "title": "Test Schema model",
        }
        schema = VirtualDataSourceSchema.from_api_response(schema_response)

        schema_model = VirtualDataSourceSchema(
            key="99.SchemaName", description="Test Schema model",
            title="Test Schema model"
        )
        self.assertEqual(schema, schema_model)


    def test_virtual_data_source_model_table(self):

        table_response = {
            "key": "99.SchemaName.TableName",
            "description": "Test Table model",
            "title": "Test Table model",
            "data_location": "//hdfs/path",
            "db_owner": "Admin",
            "definition_sql": "create table TableName (col1, int, col2, varchar(30))",
            "constraint_text": "UNIQUE(col1)",
            "ts_created": "2024-06-14T18:26:54.663432Z",
            "ts_last_altered": "2024-06-14T18:26:54.663432Z",
            "partitioning_attributes": ["column1", "column2"],
            "bucket_attributes": ["column1", "column2"],
            "sort_attributes": ["column1", "column2"],
            "synonyms": [{"schema_name": "schema_a","table_name": "table_a"},
                         {"schema_name": "schema_b","table_name": "table_b"}],
            "skews_info": {"column1": ["column1_value1", "column1_value2"],
                           "column2": ["column2_value1", "column2_value2"]},
            "table_comment": "This Table is created by ETL"
        }
        table = VirtualDataSourceTable.from_api_response(table_response)

        table_model = VirtualDataSourceTable(
            key="99.SchemaName.TableName",
            description="Test Table model",
            title="Test Table model",
            data_location="//hdfs/path",
            db_owner="Admin",
            definition_sql="create table TableName (col1, int, col2, varchar(30))",
            constraint_text="UNIQUE(col1)",
            ts_created="2024-06-14T18:26:54.663432Z",
            ts_last_altered="2024-06-14T18:26:54.663432Z",
            partitioning_attributes=["column1", "column2"],
            bucket_attributes=["column1", "column2"],
            sort_attributes=["column1", "column2"],
            synonyms=[{"schema_name": "schema_a","table_name": "table_a"},
                      {"schema_name": "schema_b","table_name": "table_b"}],
            skews_info={"column1": ["column1_value1", "column1_value2"],
                        "column2": ["column2_value1", "column2_value2"]},
            table_comment="This Table is created by ETL"
        )

        self.assertEqual(table, table_model)

    def test_virtual_data_source_model_view(self):
        view_response = {
            "key": "99.SchemaName.ViewName",
            "description": "Test View model",
            "title": "Test View model",
            "db_owner": "Admin",
            "view_sql": "create table ViewName as select * from TableName",
            "view_sql_expanded": "More details on the view here",
            "ts_created": "2024-06-14T18:26:54.663432Z",
            "ts_last_altered": "2024-06-14T18:26:54.663432Z",
            "partitioning_attributes": ["column1", "column2"],
            "bucket_attributes": ["column1", "column2"],
            "sort_attributes": ["column1", "column2"],
            "synonyms": [{"schema_name": "schema_a","table_name": "table_a"},
                         {"schema_name": "schema_b","table_name": "table_b"}],
            "skews_info": {"column1": ["column1_value1", "column1_value2"],
                           "column2": ["column2_value1", "column2_value2"]},
            "table_comment": "This Table is created by ETL"
        }

        view = VirtualDataSourceView.from_api_response(view_response)

        view_model = VirtualDataSourceView(key="99.SchemaName.ViewName", description="Test View model",
                                           title="Test View model", db_owner="Admin",
                                           view_sql="create table ViewName as select * from TableName",
                                           view_sql_expanded="More details on the view here",
                                           ts_created="2024-06-14T18:26:54.663432Z",
                                           ts_last_altered="2024-06-14T18:26:54.663432Z",
                                           partitioning_attributes=["column1", "column2"],
                                           bucket_attributes=["column1", "column2"],
                                           sort_attributes=["column1", "column2"],
                                           synonyms=[{"schema_name": "schema_a","table_name": "table_a"},
                                                     {"schema_name": "schema_b","table_name": "table_b"}],
                                           skews_info={"column1": ["column1_value1", "column1_value2"],
                                                       "column2": ["column2_value1", "column2_value2"]},
                                           table_comment="This Table is created by ETL"
                                           )

        self.assertEqual(view, view_model)

    def test_virtual_data_source_model_column(self):
        column_response = {
            "key": "99.SchemaName.TableName.ColumnName",
            "description": "Test Column model",
            "title": "Test Column model",
            "column_type": "varchar(20)",
            "position": 1,
            "column_comment": "ColumnName for table TableName",
            "nullable": "false",
        }
        column = VirtualDataSourceColumn.from_api_response(column_response)

        column_model = VirtualDataSourceColumn(key="99.SchemaName.TableName.ColumnName",
                                               description="Test Column model",
                                               title="Test Column model", column_type="varchar(20)", position=1,
                                               column_comment="ColumnName for table TableName", nullable="false")

        self.assertEqual(column, column_model)

    def test_virtual_data_source_model_index_primary(self):
        index_response = {
            "key": "99.SchemaName.TableName.index",
            "description": "Test Index model",
            "title": "Test Index model",
            "index_type": "PRIMARY",
            "column_names": ["ColumnName"],
            "data_structure": "BTREE",
            "index_type_detail": "MULTI_COLUMN_STATISTICS",
            "is_ascending": True,
            "filter_condition": "([filteredIndexCol]>(0))",
            "is_foreign_key": False,
            "foreign_key_table_name": "",
            "foreign_key_column_names": []
        }

        index = VirtualDataSourceIndex.from_api_response(index_response)

        index_model = VirtualDataSourceIndex(key="99.SchemaName.TableName.index", description="Test Index model",
                                             title="Test Index model", index_type="PRIMARY", column_names=["ColumnName"],
                                             data_structure="BTREE", index_type_detail="MULTI_COLUMN_STATISTICS",
                                             is_ascending=True,
                                             filter_condition="([filteredIndexCol]>(0))", is_foreign_key=False,
                                             foreign_key_table_name="",
                                             foreign_key_column_names=[]
        )

        self.assertEqual(index, index_model)

    def test_virtual_data_source_model_index_secondary(self):
        index_response = {
            "key": "99.SchemaName.TableName.index",
            "description": "Test Index model",
            "title": "Test Index model",
            "index_type": "SECONDARY",
            "column_names": ["ColumnName"],
            "data_structure": "BTREE",
            "index_type_detail": "MULTI_COLUMN_STATISTICS",
            "is_ascending": True,
            "filter_condition": "([filteredIndexCol]>(0))",
            "is_foreign_key": True,
            "foreign_key_table_name": "7.schema_a.table_a",
            "foreign_key_column_names": ["column1"]
        }

        index = VirtualDataSourceIndex.from_api_response(index_response)

        index_model = VirtualDataSourceIndex(key="99.SchemaName.TableName.index", description="Test Index model",
                                             title="Test Index model", index_type="SECONDARY", column_names=["ColumnName"],
                                             data_structure="BTREE", index_type_detail="MULTI_COLUMN_STATISTICS",
                                             is_ascending=True,
                                             filter_condition="([filteredIndexCol]>(0))", is_foreign_key=True,
                                             foreign_key_table_name="7.schema_a.table_a",
                                             foreign_key_column_names=["column1"]
        )

        self.assertEqual(index, index_model)


if __name__ == '__main__':
    unittest.main()
