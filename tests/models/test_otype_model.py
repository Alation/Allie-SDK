import pytest
"""Test the Alation REST API Otype Models."""

from allie_sdk.methods.otype import *


class TestUserModels:

    def test_v1_otype_model(self):

        otype_response = {
            "name": "SDK Test Otype",
        }
        otype = Otype.from_api_response(otype_response)

        otype_model = Otype(
            name="SDK Test Otype"
        )

        assert otype == otype_model

