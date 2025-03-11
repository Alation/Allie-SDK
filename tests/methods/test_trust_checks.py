"""Test the Alation REST API Trust Check Flag Methods"""

import requests_mock
import unittest
from allie_sdk.methods.trust_check import *

MOCK_TRUST_CHECK = AlationTrustChecks(
    access_token='test', session=requests.session(), host='https://test.com'
)


class TestTrustChecks(unittest.TestCase):

    @requests_mock.Mocker()
    def test_success_get_trust_checks(self, m):

        mock_params = TrustCheckFlagParams()
        mock_params.otype = 'table'
        success_response = [
            {
                "id": 4302,
                "flag_type": "ENDORSEMENT",
                "flag_reason": "",
                "ts_created": "2023-03-13T17:51:10.631861Z",
                "ts_updated": "2023-09-11T22:38:17.130821Z",
                "subject": {
                    "otype": "data",
                    "id": 6,
                    "url": "/data/6/"
                },
                "user": {
                    "id": 1,
                    "url": "/user/1/",
                    "display_name": "Alation PS User"
                }
            }
        ]
        success_flags = [TrustCheckFlag.from_api_response(item) for item in success_response]
        m.register_uri('GET', '/integration/flag/', json=success_response)
        flags = MOCK_TRUST_CHECK.get_trust_checks(mock_params)

        self.assertEqual(success_flags, flags)

    @requests_mock.Mocker()
    def test_failed_get_trust_checks(self, m):

        failed_response = {
            "detail": "Authentication credentials were not provided.",
            "code": "403000"
        }
        m.register_uri('GET', '/integration/flag/', json=failed_response, status_code=403)
        
        # The method should now raise an HTTPError for non-200 status codes
        with self.assertRaises(requests.exceptions.HTTPError):
            MOCK_TRUST_CHECK.get_trust_checks()

    @requests_mock.Mocker()
    def test_success_post_trust_check(self, m):

        mock_item = TrustCheckFlagItem()
        mock_item.flag_type = 'ENDORSEMENT'
        mock_item.subject.otype = 'table'
        mock_item.subject.id = 1

        success_response = {
            "id": 481,
            "flag_type": "ENDORSEMENT",
            "flag_reason": "",
            "ts_created": "2023-12-03T16:26:57.043823Z",
            "subject": {
                "otype": "table",
                "id": 12,
                "url": "/table/12/"
            },
            "user": {
                "id": 1,
                "url": "/user/1/",
                "display_name": "Alation PS User"
            }
        }
        # success_flag = TrustCheckFlag.from_api_response(success_response)
        m.register_uri('POST', '/integration/flag/', json=success_response)
        flag = MOCK_TRUST_CHECK.post_trust_check(mock_item)

        expected_response = JobDetails(
            status='successful'
            , msg=''
            , result=TrustCheckFlag(
                id=481
                , flag_type='ENDORSEMENT'
                , flag_reason=''
                , ts_created="2023-12-03T16:26:57.043823Z"
                , ts_updated=None
                , subject=TrustCheckFlagSubject(id=12, otype='table', url='/table/12/')
                , user=User(
                    display_name='Alation PS User'
                    , email=None
                    , id=1
                    , profile_id=None
                    , url='/user/1/'
                    , last_login=None
                    , ts_created=None
                    , first_name=None
                    , last_name=None
                    , role=None
                    , title=None
                    , username=None
                )
            )
        )

        self.assertEqual(expected_response, flag)

    @requests_mock.Mocker()
    def test_failed_post_trust_check(self, m):

        mock_item = TrustCheckFlagItem()
        mock_item.flag_type = 'ENDORSEMENT'
        mock_item.subject.otype = 'table'
        mock_item.subject.id = 1

        failed_response = {
            "subject": [
                "Invalid otype"
            ]
        }
        m.register_uri('POST', '/integration/flag/', json=failed_response, status_code=400)
        flag = MOCK_TRUST_CHECK.post_trust_check(mock_item)

        expected_result = JobDetails(
            status='failed'
            , msg=None
            , result={'subject': ['Invalid otype']}
        )

        self.assertEqual(expected_result, flag)

    @requests_mock.Mocker()
    def test_success_put_trust_check(self, m):

        mock_item = TrustCheckFlag()
        mock_item.flag_type = 'WARNING'
        mock_item.id = 1
        mock_item.flag_reason = 'This is a test'

        success_response = {
            "id": 1,
            "flag_type": "WARNING",
            "flag_reason": "<p>This is a test/p>",
            "ts_created": "2023-12-03T16:38:21.165765Z",
            "subject": {
                "otype": "table",
                "id": 12,
                "url": "/table/12/"
            },
            "user": {
                "id": 1,
                "url": "/user/1/",
                "display_name": "Alation PS User"
            }
        }

        m.register_uri('PUT', '/integration/flag/1/', json=success_response)
        flag = MOCK_TRUST_CHECK.put_trust_check(mock_item)

        expected_response = JobDetails(
            status='successful'
            , msg=''
            , result=TrustCheckFlag(
                id=1
                , flag_type='WARNING'
                , flag_reason='<p>This is a test/p>'
                , ts_created="2023-12-03T16:38:21.165765Z"
                , ts_updated=None
                , subject=TrustCheckFlagSubject(
                    id=12
                    , otype='table'
                    , url='/table/12/'
                )
                , user=User(
                    display_name='Alation PS User'
                    , email=None
                    , id=1
                    , profile_id=None
                    , url='/user/1/'
                    , last_login=None
                    , ts_created=None
                    , first_name=None
                    , last_name=None
                    , role=None
                    , title=None
                    , username=None
                )
            )
        )

        self.assertEqual(expected_response, flag)

    @requests_mock.Mocker()
    def test_failed_put_trust_check(self, m):

        mock_item = TrustCheckFlag()
        mock_item.flag_type = 'WARNING'
        mock_item.id = 1
        mock_item.flag_reason = 'This is a test'

        failed_response = {
            "detail": "Not found."
        }
        m.register_uri('PUT', '/integration/flag/1/', json=failed_response, status_code=404)
        flag = MOCK_TRUST_CHECK.put_trust_check(mock_item)

        expected_response = JobDetails(
            status='failed'
            , msg=None
            , result={'detail': 'Not found.'}
        )

        self.assertEqual(expected_response, flag)

    @requests_mock.Mocker()
    def test_success_delete_trust_check(self, m):

        mock_item = TrustCheckFlag()
        mock_item.id = 1
        m.register_uri('DELETE', '/integration/flag/1/',  status_code=204)
        delete_result = MOCK_TRUST_CHECK.delete_trust_check(mock_item)

        expected_response = JobDetails(
            status='successful'
            , msg=''
            , result=''
        )

        self.assertEqual(expected_response, delete_result)

    @requests_mock.Mocker()
    def test_failed_delete_trust_check(self, m):

        mock_item = TrustCheckFlag()
        mock_item.id = 1

        failed_response = {
            "detail": "Not found."
        }
        m.register_uri('DELETE', '/integration/flag/1/', json=failed_response, status_code=404)
        flag = MOCK_TRUST_CHECK.delete_trust_check(mock_item)

        expected_response = JobDetails(
            status='failed'
            , msg=None
            , result={'detail': 'Not found.'}
        )

        self.assertEqual(expected_response, flag)


if __name__ == '__main__':
    unittest.main()
