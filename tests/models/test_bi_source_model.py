import unittest
from allie_sdk.methods.bi_source import *


class TestBiSourceModels(unittest.TestCase):

    def test_bi_object_base_params_model(self):
        # Expected input
        input = BIObjectBaseParams(
            keyField="external_id"
            , oids="123, 234"
        )

        # Transformation
        input_transformed = input.generate_params_dict()

        # Expected Output
        output = {
            'keyField': 'external_id'
            , 'oids': '123, 234'
        }

        self.assertEqual(input_transformed, output)

    def test_bi_server_model(self):
        # Expected input
        input = {
            'id': 1
            , 'type': 'CONNECTOR'
            , 'uri': ''
            , 'title': 'Tableau SE'
            , 'description': ''
            , 'name_configuration': {
                'bi_folder': 'Folders'
                , 'bi_report': 'Reports'
                , 'bi_datasource': 'DataSources'
            }
            , 'private': False
        }

        # Transformation
        input_transformed = BIServer(**input)

        # Expected Output
        output = BIServer(
            id=1
            , type='CONNECTOR'
            , uri=''
            , title='Tableau SE'
            , description=''
            , name_configuration=BIServerNameConfiguration(
                bi_report='Reports'
                , bi_datasource='DataSources'
                , bi_folder='Folders'
                , bi_connection=None
            )
            , private=False
        )

        self.assertEqual(input_transformed, output)

    def test_bi_server_item_model(self):
        # Expected input
        input = BIServerItem(
            uri="http://localhost:5000/bi_servers"
            , title="BI Server Test"
            , description="BI Server Test"
            , name_configuration=BIServerNameConfiguration(
                bi_report="BI Report"
                , bi_datasource="BI Data Source"
                , bi_folder="BI Folder"
                , bi_connection="BI Connection"
            )
        )

        # Transformation
        input_transformed = input.generate_api_payload(
            method = "post"
        )

        # Expected Output
        output = {
            'description': 'BI Server Test'
            , 'name_configuration': {
                'bi_connection': 'BI Connection'
                , 'bi_datasource': 'BI Data Source'
                , 'bi_folder': 'BI Folder'
                , 'bi_report': 'BI Report'
            }
            , 'title': 'BI Server Test'
            , 'uri': 'http://localhost:5000/bi_servers'
        }

        self.assertEqual(input_transformed, output)

    def test_bi_folder_model(self):
        # Expected input
        input = {
            'id': 16
            , 'external_id': 'parent_workspace_folder'
            , 'name': 'Workspaces'
            , 'created_at': None
            , 'last_updated': None
            , 'source_url': None
            , 'bi_object_type': 'PowerBI Workspaces'
            , 'owner': None
            , 'description_at_source': None
            , 'num_reports': 0
            , 'num_report_accesses': 0
            , 'popularity': 0.0
            , 'parent_folder': None
            , 'subfolders': ['2a41d8b2-038d-49f2-8afc-24520bab929f']
            , 'connections': []
            , 'reports': []
            , 'datasources': []
        }

        # Transformation
        input_transformed = BIFolder(**input)

        # Expected Output
        output = BIFolder(
            id=16
            , name='Workspaces'
            , external_id='parent_workspace_folder'
            , source_url=None
            , bi_object_type='PowerBI Workspaces'
            , description_at_source=None
            , owner=None
            , created_at=None
            , last_updated=None
            , num_reports=0
            , num_report_accesses=0
            , parent_folder=None
            , popularity=0.0
            , subfolders=['2a41d8b2-038d-49f2-8afc-24520bab929f']
            , connections=[]
            , reports=[]
            , datasources=[]
        )

        self.assertEqual(input_transformed, output)

    def test_bi_folder_item_model(self):
        # Expected input
        input = BIFolderItem(
            name="Product Data Domains"  # required
            , external_id="product_data_domains"  # required
            , source_url="/a/b/c"  # required
            , bi_object_type="Project"
            , description_at_source="And here goes the description ..."
            , owner="Peter Summer"
            , created_at="2025-04-10T00:00:00.000000-08:00"
            , last_updated="2025-04-10T00:00:00.000000-08:00"
            , num_reports=2
            , num_report_accesses=343
            , parent_folder=""
        )

        # Transformation
        input_transformed = input.generate_api_payload()

        # Expected Output
        output = {
            'name': 'Product Data Domains'
            , 'external_id': 'product_data_domains'
            , 'source_url': '/a/b/c'
            , 'bi_object_type': 'Project'
            , 'description_at_source': 'And here goes the description ...'
            , 'owner': 'Peter Summer', 'created_at': '2025-04-10T00:00:00.000000-08:00'
            , 'last_updated': '2025-04-10T00:00:00.000000-08:00'
            , 'num_reports': 2
            , 'num_report_accesses': 343
            , 'parent_folder': ''
        }

        self.assertEqual(input_transformed, output)

    def test_bi_report_model(self):
        # Expected input
        input = dict(
            name = "abc"
            , external_id = "123"
            , source_url = "/a/b/c"
            , bi_object_type = "report" # freetext
            , report_type = "SIMPLE"
            , description_at_source = "And here goes the description ... CREATED"
            , owner = "Peter Summer"
            , parent_folder = "p_888"
        )

        # Transformation
        input_transformed = BIReport(**input)

        # Expected Output
        output = BIReport(
                name = "abc"
                , external_id = "123"
                , source_url = "/a/b/c"
                , bi_object_type = "report" # freetext
                , report_type = "SIMPLE"
                , description_at_source = "And here goes the description ... CREATED"
                , owner = "Peter Summer"
                , parent_folder = "p_888"
                , sub_reports = None
                , report_columns = None
            )

        self.assertEqual(input_transformed, output)

    def test_bi_report_item_model(self):
        # Expected input
        input = BIReportItem(
            name="xyz"
            , external_id="report_xyz"
            , source_url="/a/b/c"
            , bi_object_type="report"
            , report_type="SIMPLE"
            , description_at_source="And here goes the description ... CREATED"
            , owner="Peter Summer"
            , parent_folder="parent_xyz"
        )

        # Transformation
        input_transformed = input.generate_api_payload()

        # Expected Output
        output = {
            'bi_object_type': 'report'
            , 'description_at_source': 'And here goes the description ... CREATED'
            , 'external_id': 'report_xyz'
            , 'name': 'xyz'
            , 'owner': 'Peter Summer'
            , 'parent_folder': 'parent_xyz'
            , 'report_type': 'SIMPLE'
            , 'source_url': '/a/b/c'
        }

        self.assertEqual(input_transformed, output)

    def test_bi_report_column_model(self):
        # Expected input
        input = {
            "id": 1,
            "name": "sales_column",
            "external_id": "ext_id_1",
            "source_url": "http://bi.server/sales",
            "bi_object_type": "column",
            "description_at_source": "Sales data",
            "data_type": "number",
            "role": "dimension",
            "expression": "SUM(sales)",
            "values": ["100", "200", "300"],
            "report": "report_1",
            "parent_datasource_columns": ["ds_col_1"],
            "parent_report_columns": ["rpt_col_1"],
            "derived_report_columns": ["derived_col_1"]
        }

        # Transformation
        input_transformed = BIReportColumn(**input)

        # Expected Output
        output = BIReportColumn(
            id=1
            , name='sales_column'
            , external_id='ext_id_1'
            , created_at=None
            , last_updated=None
            , source_url='http://bi.server/sales'
            , bi_object_type='column'
            , description_at_source='Sales data'
            , data_type='number'
            , role='dimension'
            , expression='SUM(sales)'
            , values=['100', '200', '300']
            , report='report_1'
            , parent_datasource_columns=['ds_col_1']
            , parent_report_columns=['rpt_col_1']
            , derived_report_columns=['derived_col_1']
        )

        self.assertEqual(input_transformed, output)

    def test_bi_report_column_item_model(self):
        # Expected input
        input = BIReportColumnItem(
            name="xyz"
            , external_id='report_col_ext_id_1'
            , created_at=None
            , last_updated=None
            , source_url='http://bi.server/sales'
            , bi_object_type='column'
            , description_at_source='Sales data'
            , data_type='number'
            , role='dimension'
            , expression='SUM(sales)'
            , values=['100', '200', '300']
            , report="rep_1"
        )

        # Transformation
        input_transformed = input.generate_api_payload()

        # Expected Output
        output = {
            'name': 'xyz'
            , 'external_id': 'report_col_ext_id_1'
            , 'source_url': 'http://bi.server/sales'
            , 'bi_object_type': 'column'
            , 'description_at_source': 'Sales data'
            , 'data_type': 'number'
            , 'role': 'dimension'
            , 'expression': 'SUM(sales)'
            , 'values': ['100', '200', '300']
            , 'report': 'rep_1'
        }

        self.assertEqual(input_transformed, output)