"""Test the Alation REST API Otype Methods."""

import requests_mock
import unittest

from requests import HTTPError

from allie_sdk.methods.otype import *

MOCK_OTYPE = AlationOtype(
    access_token='test', session=requests.session(), host='https://test.com'
)

class TestOtype(unittest.TestCase):

    @requests_mock.Mocker()
    def test_success_get_otypes(self, m):

        success_response = [
            {
                "name": "Test Otype 1"
            },
            {
                "name": "Test Otype 2",
            }
        ]
        success_otypes = [Otype.from_api_response(otype) for otype in success_response]
        m.register_uri('GET', '/integration/v1/otype/', json=success_response)
        otypes = MOCK_OTYPE.get_otypes()

        self.assertEqual(success_otypes, otypes)

    @requests_mock.Mocker()
    def test_failed_get_otypes(self, m):

        failed_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }
        m.register_uri('GET', '/integration/v1/otype/', json=failed_response, status_code=403)

        with self.assertRaises(HTTPError) as context:
            MOCK_OTYPE.get_otypes()

        self.assertEqual(context.exception.response.status_code, 403)

if __name__ == '__main__':
    unittest.main()
