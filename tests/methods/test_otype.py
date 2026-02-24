import pytest
"""Test the Alation REST API Otype Methods."""

import requests_mock

from requests import HTTPError

from allie_sdk.methods.otype import *

MOCK_OTYPE = AlationOtype(
    access_token='test', session=requests.session(), host='https://test.com'
)

class TestOtype:

    
    def test_success_get_otypes(self, requests_mock):

        success_response = [
            {
                "name": "Test Otype 1"
            },
            {
                "name": "Test Otype 2",
            }
        ]
        success_otypes = [Otype.from_api_response(otype) for otype in success_response]
        requests_mock.register_uri('GET', '/integration/v1/otype/', json=success_response)
        otypes = MOCK_OTYPE.get_otypes()

        assert success_otypes == otypes

    
    def test_failed_get_otypes(self, requests_mock):

        failed_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }
        requests_mock.register_uri('GET', '/integration/v1/otype/', json=failed_response, status_code=403)

        with pytest.raises(HTTPError) as context:
            MOCK_OTYPE.get_otypes()

        assert (context.value.response.status_code == 403)

