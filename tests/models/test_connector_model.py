"""Test the Alation REST API Connector Models."""

import unittest
from allie_sdk.methods.connector import *


class TestUserModels(unittest.TestCase):

    def test_v2_connector_model(self):

        connector_response = {
            "id": 15,
            "name": "Test Connector 1",
            "uses_agent": False,
            "connector_version": "1.0.3",
            "connector_category": "RDBMS"
        }
        connector = Connector.from_api_response(connector_response)

        connector_model = Connector(
            id=15,
            name="Test Connector 1",
            uses_agent=False,
            connector_version="1.0.3",
            connector_category="RDBMS"
        )

        self.assertEqual(connector, connector_model)

if __name__ == '__main__':
    unittest.main()
