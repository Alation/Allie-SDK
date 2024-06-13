"""Test the Alation REST API Otype Models."""

import unittest
from allie_sdk.methods.otype import *


class TestUserModels(unittest.TestCase):

    def test_v1_otype_model(self):

        otype_response = {
            "name": "SDK Test Otype",
        }
        otype = Otype.from_api_response(otype_response)

        otype_model = Otype(
            name="SDK Test Otype"
        )

        self.assertEqual(otype, otype_model)

if __name__ == '__main__':
    unittest.main()
