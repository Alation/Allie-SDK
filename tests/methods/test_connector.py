"""Test the Alation REST API Connector Methods."""

import requests_mock
import unittest

from requests import HTTPError

from allie_sdk.methods.connector import *

MOCK_CONNECTOR = AlationConnector(
    access_token='test', session=requests.session(), host='https://test.com'
)

class TestConnector(unittest.TestCase):

    @requests_mock.Mocker()
    def test_success_get_connectors_v2(self, m):

        MOCK_CONNECTOR.use_v2_endpoint = True
        success_response = [
            {
                "id": 15,
                "name": "Test Connector 1",
                "uses_agent": False,
                "connector_version": "1.0.3",
                "connector_category": "RDBMS"
            },
            {
                "id": 27,
                "name": "Test Connector 2",
                "uses_agent": False,
                "connector_version": "1.0.0",
                "connector_category": "BI"
            }
        ]
        success_connectors = [Connector.from_api_response(connector) for connector in success_response]
        m.register_uri('GET', '/integration/v2/connectors/', json=success_response)
        connectors = MOCK_CONNECTOR.get_connectors()

        self.assertEqual(success_connectors, connectors)

    @requests_mock.Mocker()
    def test_failed_get_connectors_v2(self, m):

        MOCK_CONNECTOR.use_v2_endpoint = True
        failed_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }
        m.register_uri('GET', '/integration/v2/connectors/', json=failed_response, status_code=403)

        with self.assertRaises(HTTPError) as context:
            connectors = MOCK_CONNECTOR.get_connectors()

        self.assertEqual(context.exception.response.status_code, 403)

if __name__ == '__main__':
    unittest.main()
