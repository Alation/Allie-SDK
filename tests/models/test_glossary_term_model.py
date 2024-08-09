"""Test the Alation REST API Glossary Term Models"""

import unittest
from allie_sdk.core.custom_exceptions import InvalidPostBody, UnsupportedPostBody
from allie_sdk.models.custom_field_model import *
from allie_sdk.models.glossary_term_model import GlossaryTerm, GlossaryTermItem


class TestGlossaryTermModels(unittest.TestCase):

    def test_basic_glossary_term(self):

        glossary_term_response = {
            "id": 1,
            "title": "Test Term",
            "description": "This is a great description",
            "ts_created": "2022-08-31T23:40:57.642481Z",
            "ts_updated": "2022-08-31T23:40:57.642496Z",
            "ts_deleted": None,
            "deleted": False,
            "template_id": 45,
            "glossary_ids": [3],
            "custom_fields": [
                {"value": "Approved", "field_id": 5, "field_name": "Status"},
                {"value": "No", "field_id": 10040, "field_name": "Contains PII"},
                {"value": [{"otype": "groupprofile", "oid": 7}], "field_id": 8, "field_name": "Steward"}
            ]
        }
        term = GlossaryTerm.from_api_response(glossary_term_response)

        mock_term = GlossaryTerm(
            id=1,
            title="Test Term",
            description="This is a great description",
            template_id=45,
            glossary_ids=[3],
            deleted=False,
            ts_created="2022-08-31T23:40:57.642481Z",
            ts_updated="2022-08-31T23:40:57.642496Z",
            custom_fields=[
                {"value": "Approved", "field_id": 5, "field_name": "Status"},
                {"value": "No", "field_id": 10040, "field_name": "Contains PII"},
                {"value": [{"otype": "groupprofile", "oid": 7}], "field_id": 8, "field_name": "Steward"}
            ]
        )

        self.assertEqual(term, mock_term)

    def test_deleted_glossary_term(self):

        glossary_term_response = {
            "id": 1,
            "title": "Test Term",
            "description": "This is a great description",
            "ts_created": "2022-08-31T23:40:57.642481Z",
            "ts_updated": "2022-08-31T23:40:57.642496Z",
            "ts_deleted": "2022-10-31T23:40:57.642496Z",
            "deleted": True,
            "template_id": 45,
            "glossary_ids": [3],
        }
        term = GlossaryTerm.from_api_response(glossary_term_response)

        term_model = GlossaryTerm(
            id=1,
            title="Test Term",
            description="This is a great description",
            template_id=45,
            glossary_ids=[3],
            deleted = True,
            ts_created="2022-08-31T23:40:57.642481Z",
            ts_updated="2022-08-31T23:40:57.642496Z",
            ts_deleted="2022-10-31T23:40:57.642496Z"
        )

        self.assertEqual(term, term_model)

    def test_glossary_term_custom_field_parsing(self):

        mock_response = {
            "custom_fields": [
                {"value": "Approved", "field_id": 5},
                {"value": "No", "field_id": 10040},
                {"value": [{"otype": "groupprofile", "oid": 7}], "field_id": 8}
            ]
        }
        mock_term = GlossaryTerm.from_api_response(mock_response)
        expected_parsed_fields = [
            CustomFieldValue(
                field_id=5, value = CustomFieldStringValue(value="Approved")
            ),
            CustomFieldValue(
                field_id=10040, value = CustomFieldStringValue(value="No")
            ),
            CustomFieldValue(
                field_id=8, value=[CustomFieldDictValue(otype="groupprofile", oid=7)]
            )
        ]

        self.assertEqual(mock_term.custom_fields, expected_parsed_fields)

    def test_glossary_term_put_payload(self):

        mock_item = GlossaryTermItem(
            id=1,
            title="Test Term",
            description="Testing the Term",
            template_id=1,
            glossary_ids=[1],
            custom_fields=[CustomFieldValueItem(field_id=1, value=CustomFieldStringValueItem(value="Yes"))]
        )
        expected_payload = {
            "id": 1,
            "title": "Test Term",
            "description": "Testing the Term",
            "template_id": 1,
            "glossary_ids": [1],
            "custom_fields": [{"field_id": 1, "value": "Yes"}]
        }

        self.assertEqual(mock_item.generate_api_put_payload(), expected_payload)

    def test_glossary_term_post_payload(self):

        mock_item = GlossaryTermItem(
            title = "Test Term",
            description="Testing the Term",
            template_id=1,
            glossary_ids=[1],
            custom_fields=[CustomFieldValueItem(field_id=1, value=CustomFieldStringValueItem(value="Yes"))]
        )
        expected_payload = {
            "title": "Test Term",
            "description": "Testing the Term",
            "template_id": 1,
            "glossary_ids": [1],
            "custom_fields": [{"field_id": 1, "value": "Yes"}]
        }

        self.assertEqual(mock_item.generate_api_post_payload(), expected_payload)

    def test_glossary_term_put_exception_missing_id(self):

        mock_item = GlossaryTerm(
            title="Test Term",
            description="Testing the Term",
            template_id=1,
            glossary_ids=[1]
        )

        self.assertRaises(InvalidPostBody, lambda: mock_item.generate_api_put_payload())

    def test_glossary_term_post_exception_missing_title(self):

        mock_item = GlossaryTermItem(
            description="Testing the Term",
            template_id=1,
            glossary_ids=[1]
        )

        self.assertRaises(InvalidPostBody, lambda: mock_item.generate_api_post_payload())

    def test_glossary_term_post_custom_fields_exception(self):

        mock_item = GlossaryTermItem(
            title = "Test Term",
            description="Testing the Term",
            template_id=1,
            glossary_ids=[1],
            custom_fields=[CustomFieldStringValueItem(value="Yes")]
        )

        self.assertRaises(UnsupportedPostBody, lambda: mock_item.generate_api_post_payload())


if __name__ == '__main__':
    unittest.main()
