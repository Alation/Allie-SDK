"""Test the Alation REST API BI Source Methods."""

import requests_mock
import unittest
from allie_sdk.methods.bi_source import *


class TestBISource(unittest.TestCase):

    def setUp(self):
        self.mock_user = AlationBISource(
            access_token='test',
            session=requests.session(),
            host='https://test.com'
        )

    @requests_mock.Mocker()
    def test_get_bi_servers(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the bi server request?
        api_response = [
            {
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
        ]

        success_response = [
            BIServer(
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
        ]


        # Override the document API call
        requests_mock.register_uri(
            method='GET',
            url='/integration/v2/bi/server/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        bi_servers = self.mock_user.get_bi_servers()

        self.assertEqual(success_response, bi_servers)

    @requests_mock.Mocker()
    def test_get_bi_servers_empty_result(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the bi server request?
        api_response = []

        success_response = []

        # Override the document API call
        requests_mock.register_uri(
            method='GET',
            url='/integration/v2/bi/server/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        bi_servers = self.mock_user.get_bi_servers()

        self.assertEqual(success_response, bi_servers)

    @requests_mock.Mocker()
    def test_get_a_bi_server(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the document request?
        api_response = [
            {
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
        ]

        success_response = [
            BIServer(
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
        ]

        # Override the document API call
        requests_mock.register_uri(
            method='GET',
            url='/integration/v2/bi/server/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        bi_servers = self.mock_user.get_bi_servers(
            BIServerParams(
                oids=[1]
            )
        )

        self.assertEqual(success_response, bi_servers)

    @requests_mock.Mocker()
    def test_create_bi_server(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the bi server request?
        api_response = {'Count': 1, 'Errors': [None], 'Server IDs': [11], 'Status': 'Success: Created 1 servers.'}

        success_response = JobDetailsBIServerPost(
                status='successful'
                , msg=''
                , result=JobDetailsBIServerPostResult(
                    Status = 'Success: Created 1 servers.'
                    , Count = 1
                    , ServerIDs = [11]
                    , Errors = [None]
                )
            )

        # Override the document API call
        requests_mock.register_uri(
            method='POST',
            url='/integration/v2/bi/server/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        bi_servers = self.mock_user.create_bi_servers(
            [
                BIServerItem(
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
            ]
        )

        self.assertEqual(success_response, bi_servers)

    @requests_mock.Mocker()
    def test_create_bi_server_fail(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the bi server request?
        api_response = {
                'detail': 'Unable to create BI servers'
                , 'errors': ['Problem creating/updating virtual bi configuration parameters']
                , 'code': '400002'
            }

        success_response = JobDetailsBIServerPost(
            status='failed'
            , msg=None
            , result={
                'detail': 'Unable to create BI servers'
                , 'errors': ['Problem creating/updating virtual bi configuration parameters']
                , 'code': '400002'
            }
        )


        # Override the document API call
        requests_mock.register_uri(
            method='POST',
            url='/integration/v2/bi/server/',
            json=api_response,
            status_code=400
        )

        # --- TEST THE FUNCTION --- #
        bi_servers = self.mock_user.create_bi_servers(
            [
                BIServerItem(
                    uri="" # <= missing URI should cause an error
                    , title="BI Server Test"
                    , description="BI Server Test"
                    , name_configuration=BIServerNameConfiguration(
                        bi_report="BI Report"
                        , bi_datasource="BI Data Source"
                        , bi_folder="BI Folder"
                        , bi_connection="BI Connection"
                    )
                )
            ]
        )

        self.assertEqual(success_response, bi_servers)

    @requests_mock.Mocker()
    def test_update_bi_server(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the bi server request?
        api_response = {'Status': 'Success: Updated server-id 21'}

        success_response = JobDetails(
            status='successful'
            , msg=''
            , result={'Status': 'Success: Updated server-id 21'}
        )

        # Override the document API call
        requests_mock.register_uri(
            method='PATCH',
            url='/integration/v2/bi/server/21/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        bi_servers = self.mock_user.update_bi_server(
            bi_server_id=21
            , bi_server = BIServerItem(
                uri=""  # <= missing URI should cause an error
                , title="BI Server Test"
                , description="BI Server Test UPDATED"
                , name_configuration=BIServerNameConfiguration(
                    bi_report="BI Report"
                    , bi_datasource="BI Data Source"
                    , bi_folder="BI Folder"
                    , bi_connection="BI Connection"
                )
            )
        )

        self.assertEqual(success_response, bi_servers)

    @requests_mock.Mocker()
    def test_get_bi_folders(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        # What does the response look like for the folder request?
        api_response = [
            {
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
            }, {
                'id': 17
                , 'external_id': '2a41d8b2-038d-49f2-8afc-24520bab929f'
                , 'name': 'Acme Bank Workspace'
                , 'created_at': None
                , 'last_updated': None
                , 'source_url': 'groups/2a41d8b2-038d-49f2-8afc-24520bab929f'
                , 'bi_object_type': 'New Workspace'
                , 'owner': None
                , 'description_at_source': None
                , 'num_reports': 2
                , 'num_report_accesses': 0
                , 'popularity': None
                , 'parent_folder': 'parent_workspace_folder'
                , 'subfolders': []
                , 'connections': []
                , 'reports': ['663b9e9a-d6dc-4554-a0d3-9379a6586897', '90274a21-e533-4506-b23a-2f5e6b75e15c']
                , 'datasources': ['919cf9a1-cd06-422a-b239-b82948e0dde1']
            }]

        success_response = [
            BIFolder(
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
                , datasources = []
            )
            , BIFolder(
                id=17
                , name='Acme Bank Workspace'
                , external_id='2a41d8b2-038d-49f2-8afc-24520bab929f'
                , source_url='groups/2a41d8b2-038d-49f2-8afc-24520bab929f'
                , bi_object_type='New Workspace'
                , description_at_source=None
                , owner=None
                , created_at=None
                , last_updated=None
                , num_reports=2
                , num_report_accesses=0
                , parent_folder='parent_workspace_folder'
                , popularity=None
                , subfolders=[]
                , connections=[]
                , reports=['663b9e9a-d6dc-4554-a0d3-9379a6586897', '90274a21-e533-4506-b23a-2f5e6b75e15c']
                , datasources=['919cf9a1-cd06-422a-b239-b82948e0dde1']
            )
        ]


        # Override the document API call
        bi_server_id = 21

        requests_mock.register_uri(
            method='GET',
            url=f'/integration/v2/bi/server/{bi_server_id}/folder/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        bi_servers = self.mock_user.get_bi_folders(
            bi_server_id=bi_server_id
        )

        self.assertEqual(success_response, bi_servers)

    @requests_mock.Mocker()
    def test_get_a_bi_folder(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        bi_folder_id = 16

        # What does the response look like for the folder request?
        api_response = [
            {
                'id': bi_folder_id
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
        ]

        success_response = [
            BIFolder(
                id = bi_folder_id
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
                , datasources = []
            )
        ]

        # Override the document API call
        bi_server_id = 21

        requests_mock.register_uri(
            method='GET',
            url=f'/integration/v2/bi/server/{bi_server_id}/folder/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        bi_servers = self.mock_user.get_bi_folders(
            bi_server_id = bi_server_id
            , query_params = BIFolderParams(
                oids = [ bi_folder_id ]
            )
        )

        self.assertEqual(success_response, bi_servers)

    @requests_mock.Mocker()
    def test_create_bi_folders(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        bi_server_id = 21
        job_id = 27809

        # What does the response look like for the create document request?
        bi_folders_api_response = {
            "job_id": job_id
        }

        # Override the document API call
        requests_mock.register_uri(
            method='POST',
            url=f'/integration/v2/bi/server/{bi_server_id}/folder/',
            json=bi_folders_api_response,
            status_code=202
        )

        # What does the response look like for the Job?
        job_api_response = {
                'msg': 'Job finished in 0.092239 seconds at 2025-04-17 10:00:55.383912+00:00'
                , 'result': ['1 BIFolder object(s) received, 1 new object(s) created', 'BI_V2_API_SYNCING took 0.09s']
                , 'status': 'successful'
            }

        # What should the correct response look like?
        success_response = [
            JobDetails(
                status='successful'
                , msg='Job finished in 0.092239 seconds at 2025-04-17 10:00:55.383912+00:00'
                , result=['1 BIFolder object(s) received, 1 new object(s) created', 'BI_V2_API_SYNCING took 0.09s']
            )
        ]

        # Override the job API call
        # Note: The id in the job URL corresponds to the task id in document_api_response defined above
        requests_mock.register_uri(
            method='GET',
            url=f'/api/v1/bulk_metadata/job/?id={job_id}',
            json=job_api_response
        )

        # --- TEST THE FUNCTION --- #
        bi_servers = self.mock_user.create_or_update_bi_folders_using_external_id(
            bi_server_id = bi_server_id
            , bi_folders = [
                BIFolderItem(
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
            ]
        )

        self.assertEqual(success_response, bi_servers)

    @requests_mock.Mocker()
    def test_update_bi_folder_using_internal_id(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        BI_SERVER_ID = 1
        BI_FOLDER_ID = 123

        # What does the response look like for the request?
        api_response = dict(
            id=BI_FOLDER_ID
            , name = "Product Data Domains"  # required
            , external_id = "product_data_domains"  # required
            , source_url = "/a/b/c"  # required
            , bi_object_type = "Project"
            , description_at_source = "And here goes the description ..."
            , owner = "Peter Summer"
            , created_at = "2025-04-10T00:00:00.000000-08:00"
            , last_updated = "2025-04-10T00:00:00.000000-08:00"
            , num_reports = 2
            , num_report_accesses = 343
            , parent_folder = ""
        )

        expected_result = BIFolder(
            id=BI_FOLDER_ID
            , name = "Product Data Domains"  # required
            , external_id = "product_data_domains"  # required
            , source_url = "/a/b/c"  # required
            , bi_object_type = "Project"
            , description_at_source = "And here goes the description ..."
            , owner = "Peter Summer"
            , created_at = "2025-04-10T00:00:00.000000-08:00"
            , last_updated = "2025-04-10T00:00:00.000000-08:00"
            , num_reports = 2
            , num_report_accesses = 343
            , parent_folder = ""
        )

        # Override the document API call
        requests_mock.register_uri(
            method='PATCH',
            url=f'/integration/v2/bi/server/{BI_SERVER_ID}/folder/{BI_FOLDER_ID}/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        actual_result = self.mock_user.update_bi_folder_using_internal_id(
            bi_server_id=BI_SERVER_ID
            , bi_folder_id=BI_FOLDER_ID
            , bi_folder=BIFolderItem(
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
        )

        self.assertEqual(expected_result, actual_result)

    @requests_mock.Mocker()
    def test_delete_bi_folders(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        BI_SERVER_ID = 1

        # What does the response look like for the request?
        api_response = ""

        expected_result = JobDetails(
            status="successful"
            , msg=""
            , result=""
        )

        # Override the document API call
        requests_mock.register_uri(
            method='DELETE'
            , url=f'/integration/v2/bi/server/{BI_SERVER_ID}/folder/'
            , json=api_response
            , status_code=204
        )

        # --- TEST THE FUNCTION --- #
        actual_result = self.mock_user.delete_bi_folders(
            bi_server_id=BI_SERVER_ID
        )

        self.assertEqual(expected_result, actual_result)

    # ------------------------------
    # --------- BI REPORTS ---------
    # ------------------------------

    @requests_mock.Mocker()
    def test_get_bi_reports(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        BI_SERVER_ID = 1

        # What does the response look like for the request?
        api_response = [
            dict(
                name = "abc"
                , external_id = "123"
                , source_url = "/a/b/c"
                , bi_object_type = "report" # freetext
                , report_type = "SIMPLE"
                , description_at_source = "And here goes the description ... CREATED"
                , owner = "Peter Summer"
                , parent_folder = "p_888"
            )
        ]

        expected_result = [
            BIReport(
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
        ]

        # Override the document API call
        requests_mock.register_uri(
            method='GET',
            url=f'/integration/v2/bi/server/{BI_SERVER_ID}/report/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        actual_result = self.mock_user.get_bi_reports(
            bi_server_id=BI_SERVER_ID
        )

        self.assertEqual(expected_result, actual_result)

    @requests_mock.Mocker()
    def test_get_bi_reports_with_query_params(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        BI_SERVER_ID = 1

        # What does the response look like for the request?
        api_response = [
            dict(
                name="abc"
                , external_id="123"
                , source_url="/a/b/c"
                , bi_object_type="report"  # freetext
                , report_type="SIMPLE"
                , description_at_source="And here goes the description ... CREATED"
                , owner="Peter Summer"
                , parent_folder="p_888"
            )
        ]

        expected_result = [
            BIReport(
                name="abc"
                , external_id="123"
                , source_url="/a/b/c"
                , bi_object_type="report"  # freetext
                , report_type="SIMPLE"
                , description_at_source="And here goes the description ... CREATED"
                , owner="Peter Summer"
                , parent_folder="p_888"
                , sub_reports=None
                , report_columns=None
            )
        ]

        # Override the document API call
        requests_mock.register_uri(
            method='GET',
            url=f'/integration/v2/bi/server/{BI_SERVER_ID}/report/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        actual_result = self.mock_user.get_bi_reports(
            bi_server_id=BI_SERVER_ID
            , query_params = BIReportParams(
                keyField = "external_id"
                , oids = "123"
            )
        )

        self.assertEqual(expected_result, actual_result)

    @requests_mock.Mocker()
    def test_create_or_update_bi_reports_using_external_id(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        BI_SERVER_ID = 1
        JOB_ID = 27809

        # What does the response look like for the create document request?
        api_response = {
            "job_id": JOB_ID
        }

        # Override the function API call
        requests_mock.register_uri(
            method='POST',
            url=f'/integration/v2/bi/server/{BI_SERVER_ID}/report/',
            json=api_response,
            status_code=202
        )

        # What does the response look like for the Job?
        job_api_response = {
            'msg': 'Job finished in 0.057239 seconds at 2025-09-30 07:03:24.836810+00:00'
            , 'result': ['1 BIReport object(s) received, 1 existing object(s) updated', 'BI_V2_API_SYNCING took 0.06s']
            , 'status': 'successful'
        }

        # Override the job API call
        # Note: The id in the job URL corresponds to the task id in api_response defined above
        requests_mock.register_uri(
            method='GET',
            url=f'/api/v1/bulk_metadata/job/?id={JOB_ID}',
            json=job_api_response
        )

        # --- TEST THE FUNCTION --- #
        actual_result = self.mock_user.create_or_update_bi_reports_using_external_id(
            bi_server_id = BI_SERVER_ID
            , bi_reports =[
                BIReportItem(
                    name="xyz"
                    , external_id="report_xyz"
                    , source_url="/a/b/c"
                    , bi_object_type="report"
                    , report_type="SIMPLE"
                    , description_at_source="And here goes the description ... CREATED"
                    , owner="Peter Summer"
                    , parent_folder="parent_xyz"
                )
            ]
        )

        function_expected_result = [
            JobDetails(
                status='successful'
                , msg='Job finished in 0.057239 seconds at 2025-09-30 07:03:24.836810+00:00'
                , result=['1 BIReport object(s) received, 1 existing object(s) updated', 'BI_V2_API_SYNCING took 0.06s']
            )
        ]

        self.assertEqual(function_expected_result, actual_result)

    @requests_mock.Mocker()
    def test_update_bi_report_using_internal_id(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        BI_SERVER_ID = 1
        BI_REPORT_ID = 123

        # What does the response look like for the request?
        api_response = dict(
            id = BI_REPORT_ID
            , name="abc"
            , external_id="ext_123"
            , source_url="/a/b/c"
            , bi_object_type="report"  # freetext
            , report_type="SIMPLE"
            , description_at_source="And here goes the description ... UPDATED"
            , owner="Peter Summer"
            , parent_folder="p_888"
        )

        expected_result = BIReport(
            id = BI_REPORT_ID
            , name="abc"
            , external_id="ext_123"
            , source_url="/a/b/c"
            , bi_object_type="report"  # freetext
            , report_type="SIMPLE"
            , description_at_source="And here goes the description ... UPDATED"
            , owner="Peter Summer"
            , parent_folder="p_888"
            , sub_reports=None
            , report_columns=None
        )

        # Override the document API call
        requests_mock.register_uri(
            method='PATCH',
            url=f'/integration/v2/bi/server/{BI_SERVER_ID}/report/{BI_REPORT_ID}/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        actual_result = self.mock_user.update_bi_report_using_internal_id(
            bi_server_id = BI_SERVER_ID
            , bi_report_id = BI_REPORT_ID
            , bi_report = BIReportItem(
                name="abc"
                , external_id="ext_123"
                , source_url="/a/b/c"
                , bi_object_type="report"  # freetext
                , report_type="SIMPLE"
                , description_at_source="And here goes the description ... UPDATED"
                , owner="Peter Summer"
                , parent_folder="p_888"
            )
        )

        self.assertEqual(expected_result, actual_result)

    @requests_mock.Mocker()
    def test_delete_a_bi_report(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        BI_SERVER_ID = 1
        BI_REPORT_ID = 123

        # What does the response look like for the request?
        api_response = ""

        expected_result = JobDetails(
            status = "successful"
            , msg = ""
            , result = ""
        )

        # Override the document API call
        requests_mock.register_uri(
            method='DELETE'
            , url=f'/integration/v2/bi/server/{BI_SERVER_ID}/report/{BI_REPORT_ID}/'
            , json=api_response
            , status_code=204
        )

        # --- TEST THE FUNCTION --- #
        actual_result = self.mock_user.delete_a_bi_report(
            bi_server_id=BI_SERVER_ID
            , bi_report_id=BI_REPORT_ID
        )

        self.assertEqual(expected_result, actual_result)

    @requests_mock.Mocker()
    def test_delete_bi_reports(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        BI_SERVER_ID = 1
        BI_REPORT_ID = 123

        # What does the response look like for the request?
        api_response = ""

        expected_result = JobDetails(
            status="successful"
            , msg=""
            , result=""
        )

        # Override the document API call
        requests_mock.register_uri(
            method='DELETE'
            , url=f'/integration/v2/bi/server/{BI_SERVER_ID}/report/'
            , json=api_response
            , status_code=204
        )

        # --- TEST THE FUNCTION --- #
        actual_result = self.mock_user.delete_bi_reports(
            bi_server_id=BI_SERVER_ID
        )

        self.assertEqual(expected_result, actual_result)

    # ------------------------------
    # ----- BI REPORT COLUMNS ------
    # ------------------------------

    @requests_mock.Mocker()
    def test_get_bi_report_columns(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        BI_SERVER_ID = 1

        # What does the response look like for the request?
        api_response = [
            {
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
        ]

        expected_result = [BIReportColumn.from_api_response(item) for item in api_response]

        # Override the document API call
        requests_mock.register_uri(
            method='GET',
            url=f'/integration/v2/bi/server/{BI_SERVER_ID}/report/column/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        actual_result = self.mock_user.get_bi_report_columns(
            bi_server_id=BI_SERVER_ID
        )

        self.assertEqual(expected_result, actual_result)

    @requests_mock.Mocker()
    def test_get_bi_report_columns_with_query_params(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        BI_SERVER_ID = 1

        # What does the response look like for the request?
        api_response = [
            {
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
        ]

        expected_result = [BIReportColumn.from_api_response(item) for item in api_response]

        # Override the document API call
        requests_mock.register_uri(
            method='GET',
            url=f'/integration/v2/bi/server/{BI_SERVER_ID}/report/column/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        actual_result = self.mock_user.get_bi_report_columns(
            bi_server_id=BI_SERVER_ID
            , query_params = BIReportColumnParams(
                keyField = "external_id"
                , oids = "ext_id_1"
            )
        )

        self.assertEqual(expected_result, actual_result)

    @requests_mock.Mocker()
    def test_create_or_update_bi_report_columns_using_external_id(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        BI_SERVER_ID = 1
        JOB_ID = 27809

        # What does the response look like for the create document request?
        api_response = {
            "job_id": JOB_ID
        }

        # Override the function API call
        requests_mock.register_uri(
            method='POST',
            url=f'/integration/v2/bi/server/{BI_SERVER_ID}/report/column/',
            json=api_response,
            status_code=202
        )

        # What does the response look like for the Job?
        job_api_response = {
            'msg': 'Job finished in 0.05236 seconds at 2025-09-30 07:24:27.631871+00:00'
            , 'result': ['1 BIReportColumn object(s) received, 1 existing object(s) updated', 'BI_V2_API_SYNCING took 0.05s']
            , 'status': 'successful'
        }

        # Override the job API call
        # Note: The id in the job URL corresponds to the task id in api_response defined above
        requests_mock.register_uri(
            method='GET',
            url=f'/api/v1/bulk_metadata/job/?id={JOB_ID}',
            json=job_api_response
        )

        # --- TEST THE FUNCTION --- #
        actual_result = self.mock_user.create_or_update_bi_report_columns_using_external_id(
            bi_server_id=BI_SERVER_ID
            , bi_report_columns=[
                BIReportColumnItem(
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
            ]
        )

        function_expected_result = [
            JobDetails(
                status='successful'
                , msg='Job finished in 0.05236 seconds at 2025-09-30 07:24:27.631871+00:00'
                , result=['1 BIReportColumn object(s) received, 1 existing object(s) updated', 'BI_V2_API_SYNCING took 0.05s']
            )
        ]

        self.assertEqual(function_expected_result, actual_result)

    @requests_mock.Mocker()
    def test_update_bi_report_column_using_internal_id(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        BI_SERVER_ID = 1
        BI_REPORT_COLUMN_ID = 123

        # What does the response look like for the request?
        api_response = dict(
            id=BI_REPORT_COLUMN_ID
            , name = 'abc - UPDATED'
            , external_id = 'report_col_ext_id_1'
            , created_at = None
            , last_updated = None
            , source_url = 'http://bi.server/sales'
            , bi_object_type = 'column'
            , description_at_source = 'Sales data - UPDATED'
            , data_type = 'number'
            , role = 'dimension'
            , expression = 'SUM(sales)'
            , values = ['100', '200', '300']
            , report = "ext_123"
        )

        expected_result = BIReportColumn(
            id=BI_REPORT_COLUMN_ID
            , name = 'abc - UPDATED'
            , external_id = 'report_col_ext_id_1'
            , created_at = None
            , last_updated = None
            , source_url = 'http://bi.server/sales'
            , bi_object_type = 'column'
            , description_at_source = 'Sales data - UPDATED'
            , data_type = 'number'
            , role = 'dimension'
            , expression = 'SUM(sales)'
            , values = ['100', '200', '300']
            , report = "ext_123"
        )

        # Override the document API call
        requests_mock.register_uri(
            method='PATCH',
            url=f'/integration/v2/bi/server/{BI_SERVER_ID}/report/column/{BI_REPORT_COLUMN_ID}/',
            json=api_response,
            status_code=200
        )

        # --- TEST THE FUNCTION --- #
        actual_result = self.mock_user.update_bi_report_column_using_internal_id(
            bi_server_id=BI_SERVER_ID
            , bi_report_column_id=BI_REPORT_COLUMN_ID
            , bi_report_column=BIReportColumnItem(
                name='abc - UPDATED'
                , external_id='report_col_ext_id_1'
                , created_at=None
                , last_updated=None
                , source_url='http://bi.server/sales'
                , bi_object_type='column'
                , description_at_source='Sales data - UPDATED'
                , data_type='number'
                , role='dimension'
                , expression='SUM(sales)'
                , values=['100', '200', '300']
                , report= "ext_123"
            )
        )

        self.assertEqual(expected_result, actual_result)

    @requests_mock.Mocker()
    def test_delete_bi_report_columns(self, requests_mock):
        # --- PREPARE THE TEST SETUP --- #

        BI_SERVER_ID = 1

        # What does the response look like for the request?
        api_response = ""

        expected_result = JobDetails(
            status="successful"
            , msg=""
            , result=""
        )

        # Override the document API call
        requests_mock.register_uri(
            method='DELETE'
            , url=f'/integration/v2/bi/server/{BI_SERVER_ID}/report/column/'
            , json=api_response
            , status_code=204
        )

        # --- TEST THE FUNCTION --- #
        actual_result = self.mock_user.delete_bi_report_columns(
            bi_server_id=BI_SERVER_ID
        )

        self.assertEqual(expected_result, actual_result)