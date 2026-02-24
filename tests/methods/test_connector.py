"""Test the Alation REST API Connector Methods."""
import pytest
from requests import HTTPError
from allie_sdk.methods.connector import *

MOCK_CONNECTOR = AlationConnector(
    access_token='test', session=requests.session(), host='https://test.com'
)

class TestConnector:
    def test_success_get_connectors_v2(self, requests_mock):

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
        requests_mock.register_uri('GET', '/integration/v2/connectors/', json=success_response)
        connectors = MOCK_CONNECTOR.get_connectors()

        assert success_connectors == connectors

    def test_failed_get_connectors_v2(self, requests_mock):

        MOCK_CONNECTOR.use_v2_endpoint = True
        failed_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }
        requests_mock.register_uri('GET', '/integration/v2/connectors/', json=failed_response, status_code=403)

        with pytest.raises(HTTPError) as context:
            MOCK_CONNECTOR.get_connectors()

        status_code = context.value.response.status_code

        assert status_code == 403

