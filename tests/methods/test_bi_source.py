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
                , name_configuration=NameConfiguration(
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
                , name_configuration=NameConfiguration(
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