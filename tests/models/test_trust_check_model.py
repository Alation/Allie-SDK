"""Test the Alation REST API Trust Check Models"""

import unittest
from allie_sdk.models.trust_check_model import *


class TestTrustCheckModels(unittest.TestCase):

    def test_trust_check_flag(self):

        flag_response = {
            "id": 2366,
            "flag_type": "ENDORSEMENT",
            "flag_reason": "",
            "ts_created": "2023-01-22T21:56:17.956051Z",
            "ts_updated": "2023-09-11T22:38:17.130821Z",
            "subject": {
                "otype": "attribute",
                "id": 1609,
                "url": "/attribute/1609/"
            },
            "user": {
                "id": 18,
                "url": "/user/18/",
                "display_name": "Test User"
            }
        }
        flag = TrustCheckFlag.from_api_response(flag_response)

        mock_flag = TrustCheckFlag(
            id=2366,
            flag_type="ENDORSEMENT",
            flag_reason="",
            ts_created="2023-01-22T21:56:17.956051Z",
            ts_updated="2023-09-11T22:38:17.130821Z",
            subject={"otype": "attribute", "id": 1609, "url": "/attribute/1609/"},
            user={"id": 18, "url": "/user/18/", "display_name": "Test User"}
        )

        self.assertEqual(flag, mock_flag)

    def test_trust_check_subject_parsing(self):

        flag_response = {
            "id": 2366,
            "flag_type": "ENDORSEMENT",
            "flag_reason": "",
            "ts_created": "2023-01-22T21:56:17.956051Z",
            "ts_updated": "2023-09-11T22:38:17.130821Z",
            "subject": {
                "otype": "attribute",
                "id": 1609,
                "url": "/attribute/1609/"
            },
            "user": {
                "id": 18,
                "url": "/user/18/",
                "display_name": "Test User"
            }
        }
        flag = TrustCheckFlag.from_api_response(flag_response)

        mock_flag_subject = TrustCheckFlagSubject(
            otype="attribute",
            id=1609,
            url="/attribute/1609/"
        )

        self.assertEqual(flag.subject, mock_flag_subject)

    def test_trust_check_user_parsing(self):

        flag_response = {
            "id": 2366,
            "flag_type": "ENDORSEMENT",
            "flag_reason": "",
            "ts_created": "2023-01-22T21:56:17.956051Z",
            "ts_updated": "2023-09-11T22:38:17.130821Z",
            "subject": {
                "otype": "attribute",
                "id": 1609,
                "url": "/attribute/1609/"
            },
            "user": {
                "id": 18,
                "url": "/user/18/",
                "display_name": "Test User"
            }
        }
        flag = TrustCheckFlag.from_api_response(flag_response)

        mock_flag_user = User(
            id=18,
            url="/user/18/",
            display_name="Test User"
        )

        self.assertEqual(flag.user, mock_flag_user)

    def test_trust_check_flag_put_payload(self):

        mock_flag = TrustCheckFlag(
            flag_type='Warning',
            flag_reason='Testing the Put Payload'
        )
        expected_payload = {'flag_reason': 'Testing the Put Payload'}

        self.assertEqual(mock_flag.generate_api_put_body(), expected_payload)

    def test_trust_check_flag_put_exception_invalid_flag_type(self):

        mock_flag = TrustCheckFlag(
            flag_type='Endorsement',
            flag_reason='Testing the Put Payload'
        )

        self.assertRaises(InvalidPostBody, lambda: mock_flag.generate_api_put_body())

    def test_trust_check_flag_item_payload(self):

        mock_flag = TrustCheckFlagItem(
            flag_type='WARNING',
            flag_reason='This is a test',
            subject=TrustCheckFlagSubject(
                id=1,
                otype='Table'
            )
        )
        expected_payload = {
            'flag_type': 'WARNING', 'flag_reason': 'This is a test',
            'subject': {'id': 1, 'otype': 'table'}
        }

        self.assertEqual(mock_flag.generate_api_post_payload(), expected_payload)

    def test_trust_check_flag_payload_endorsement_with_reason(self):

        mock_flag = TrustCheckFlagItem(
            flag_type='ENDORSEMENT',
            flag_reason='This is a test',
            subject=TrustCheckFlagSubject(
                id=1,
                otype='Table'
            )
        )
        expected_payload = {'flag_type': 'ENDORSEMENT', 'subject': {'id': 1, 'otype': 'table'}}

        self.assertEqual(mock_flag.generate_api_post_payload(), expected_payload)

    def test_trust_check_flag_item_exception_invalid_flag_type(self):

        mock_flag = TrustCheckFlagItem(
            flag_type='PASSING',
            flag_reason='This is a test',
            subject=TrustCheckFlagSubject(
                id=1,
                otype='Table'
            )
        )

        self.assertRaises(InvalidPostBody, lambda: mock_flag.generate_api_post_payload())

    def test_trust_check_flag_item_exception_missing_subject_otype(self):

        mock_flag = TrustCheckFlagItem(
            flag_type='WARNING',
            flag_reason='This is a test',
            subject=TrustCheckFlagSubject(
                id=1,
            )
        )

        self.assertRaises(InvalidPostBody, lambda: mock_flag.generate_api_post_payload())

    def test_trust_check_flag_item_exception_missing_subject_id(self):

        mock_flag = TrustCheckFlagItem(
            flag_type='WARNING',
            flag_reason='This is a test',
            subject=TrustCheckFlagSubject(
                otype='Table'
            )
        )

        self.assertRaises(InvalidPostBody, lambda: mock_flag.generate_api_post_payload())



if __name__ == '__main__':
    unittest.main()
