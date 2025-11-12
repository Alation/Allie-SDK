"""Test the Alation REST API Custom Field and Values Models"""

import unittest
from allie_sdk.methods.custom_field import *


class TestCustomFieldModels(unittest.TestCase):

    def test_custom_field_model(self):

        mock_field_response = {
            "allow_multiple": False,
            "allowed_otypes": ["groupprofile", "user"],
            "field_type": "OBJECT_SET",
            "id": 9,
            "name_plural": "People working on",
            "name_singular": "Person working on"
        }
        mock_field = CustomField.from_api_response(mock_field_response)
        expected_field = CustomField(
            id=9,
            name_plural="People working on",
            name_singular="Person working on",
            field_type="OBJECT_SET",
            allow_multiple=False,
            allowed_otypes=["groupprofile", "user"]
        )

        self.assertEqual(mock_field, expected_field)

    def test_custom_field_item_picker_payload(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Picker'
        mock_item.name_singular = 'Testing'
        mock_item.options = ['test1', 'test2']
        mock_item.tooltip_text = 'Test Custom Picker Field'

        expected_payload = {
            'field_type': 'PICKER'
            , 'name_singular': 'Testing'
            , 'options': ['test1', 'test2']
            , 'tooltip_text': 'Test Custom Picker Field'
        }

        self.assertEqual(mock_item.generate_api_post_payload(), expected_payload)

    def test_custom_field_item_picker_exception_title(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Picker'
        mock_item.options = ['test1', 'test2']

        self.assertRaises(InvalidPostBody, lambda: mock_item.generate_api_post_payload())

    def test_custom_field_item_picker_exception_options(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Picker'
        mock_item.name_singular = 'Testing'

        self.assertRaises(InvalidPostBody, lambda: mock_item.generate_api_post_payload())

    def test_custom_field_item_multipicker_payload(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Multi_Picker'
        mock_item.name_singular = 'Testing'
        mock_item.name_plural = 'Tests'
        mock_item.options = ['test1', 'test2']
        expected_payload = {
            'field_type': 'MULTI_PICKER'
            , 'name_singular': 'Testing'
            , 'name_plural': 'Tests'
            , 'options': ['test1', 'test2']
        }

        self.assertEqual(mock_item.generate_api_post_payload(), expected_payload)

    def test_custom_field_item_multipicker_exception_name_singular(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Multi_Picker'
        mock_item.name_plural = 'Tests'
        mock_item.options = ['test1', 'test2']

        self.assertRaises(InvalidPostBody, lambda: mock_item.generate_api_post_payload())

    def test_custom_field_item_multipicker_exception_name_plural(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Multi_Picker'
        mock_item.name_singular = 'Testing'
        mock_item.options = ['test1', 'test2']

        self.assertRaises(InvalidPostBody, lambda: mock_item.generate_api_post_payload())

    def test_custom_field_item_multipicker_exception_options(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Multi_Picker'
        mock_item.name_singular = 'Testing'
        mock_item.name_plural = 'Tests'

        self.assertRaises(InvalidPostBody, lambda: mock_item.generate_api_post_payload())

    def test_custom_field_item_rich_text_payload(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Rich_Text'
        mock_item.name_singular = 'Testing'
        expected_payload = {'field_type': 'RICH_TEXT', 'name_singular': 'Testing'}

        self.assertEqual(mock_item.generate_api_post_payload(), expected_payload)

    def test_custom_field_item_rich_text_exception_name(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Rich_Text'

        self.assertRaises(InvalidPostBody, lambda: mock_item.generate_api_post_payload())

    def test_custom_field_item_date_payload(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Date'
        mock_item.name_singular = 'Testing'
        expected_payload = {'field_type': 'DATE', 'name_singular': 'Testing'}

        self.assertEqual(mock_item.generate_api_post_payload(), expected_payload)

    def test_custom_field_item_date_exception_name(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Date'

        self.assertRaises(InvalidPostBody, lambda: mock_item.generate_api_post_payload())

    def test_custom_field_item_object_set_object_set_payload(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Object_Set'
        mock_item.allow_multiple = True
        mock_item.allowed_otypes = ['schema', 'table', 'attribute', 'article', 'glossary_term']
        mock_item.backref_name = 'Testing the Object Set'
        mock_item.name_singular = 'Testing'
        mock_item.name_plural = 'Tests'
        expected_payload = {
            'field_type': 'OBJECT_SET'
            , 'allow_multiple': True
            , 'name_singular': 'Testing'
            , 'allowed_otypes': ['schema', 'table', 'attribute', 'article', 'glossary_term']
            , 'backref_name': 'Testing the Object Set'
            , 'name_plural': 'Tests'
        }

        self.assertEqual(mock_item.generate_api_post_payload(), expected_payload)

    def test_custom_field_item_object_set_people_set_payload(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Object_Set'
        mock_item.allow_multiple = True
        mock_item.allowed_otypes = ['user', 'groupprofile']
        mock_item.backref_name = 'Testing the People Set'
        mock_item.name_singular = 'Testing'
        mock_item.name_plural = 'Tests'
        expected_payload = {
            'field_type': 'OBJECT_SET'
            , 'allow_multiple': True
            , 'name_singular': 'Testing'
            , 'allowed_otypes': ['user', 'groupprofile']
            , 'backref_name': 'Testing the People Set'
            , 'name_plural': 'Tests'
        }

        self.assertEqual(mock_item.generate_api_post_payload(), expected_payload)

    def test_custom_field_item_object_set_reference_payload(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Object_Set'
        mock_item.allow_multiple = False
        mock_item.allowed_otypes = ['schema', 'table', 'attribute', 'article', 'glossary_term']
        mock_item.backref_name = 'Testing the Reference Set'
        mock_item.name_singular = 'Testing'
        expected_payload = {
            'field_type': 'OBJECT_SET'
            , 'allow_multiple': False
            , 'name_singular': 'Testing'
            , 'allowed_otypes': ['schema', 'table', 'attribute', 'article', 'glossary_term']
            , 'backref_name': 'Testing the Reference Set'
        }

        self.assertEqual(mock_item.generate_api_post_payload(), expected_payload)

    def test_custom_field_item_object_set_exception_missing_required_value(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Object_Set'
        mock_item.allowed_otypes = ['schema', 'table', 'attribute', 'article', 'glossary_term']
        mock_item.backref_name = 'Testing the Reference Set'
        mock_item.name_singular = 'Testing'

        self.assertRaises(InvalidPostBody, lambda: mock_item.generate_api_post_payload())

    def test_custom_field_item_object_set_exception_missing_plural_name(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Object_Set'
        mock_item.allow_multiple = True
        mock_item.allowed_otypes = ['user', 'groupprofile']
        mock_item.backref_name = 'Testing the People Set'
        mock_item.name_singular = 'Testing'

        self.assertRaises(InvalidPostBody, lambda: mock_item.generate_api_post_payload())

    def test_custom_field_item_object_set_exception_invalid_otype(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Object_Set'
        mock_item.allow_multiple = True
        mock_item.allowed_otypes = ['user', 'groupprofiles']
        mock_item.backref_name = 'Testing the People Set'
        mock_item.name_singular = 'Testing'
        mock_item.name_plural = 'Tests'

        self.assertRaises(InvalidPostBody, lambda: mock_item.generate_api_post_payload())

    def test_custom_field_object_set_optional_fields(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Object_Set'
        mock_item.allow_multiple = True
        mock_item.allowed_otypes = ['schema', 'table', 'attribute', 'article', 'glossary_term']
        mock_item.backref_name = 'Testing the Object Set'
        mock_item.name_singular = 'Testing'
        mock_item.name_plural = 'Tests'
        mock_item.backref_tooltip_text = 'Testing the Backref Tooltip'
        mock_item.tooltip_text = 'Testing the Tooltip'
        expected_payload = {
            'field_type': 'OBJECT_SET'
            , 'allow_multiple': True
            , 'name_singular': 'Testing'
            , 'allowed_otypes': ['schema', 'table', 'attribute', 'article', 'glossary_term']
            , 'backref_name': 'Testing the Object Set', 'name_plural': 'Tests'
            , 'backref_tooltip_text': 'Testing the Backref Tooltip'
            , 'tooltip_text': 'Testing the Tooltip'
        }

        self.assertEqual(mock_item.generate_api_post_payload(), expected_payload)

    def test_custom_field_item_exception_invalid_field_type(self):

        mock_item = CustomFieldItem()
        mock_item.field_type = 'Object_Sets'

        self.assertRaises(InvalidPostBody, lambda: mock_item.generate_api_post_payload())

    # --- TESTS FOR CUSTOM FIELD VALUE MODEL --- #

    # for GET method
    # this applies to rich text, picker, date custom fields
    def test_custom_field_value_model_string_value(self):

        mock_field_value_response = {
            "field_id": 3,
            "oid": 3,
            "otype": "policy_group",
            "ts_updated": "2022-02-12T13:54:24.192436Z",
            "value": "3 Data Policy"
        }
        mock_string_value = CustomFieldValue.from_api_response(mock_field_value_response)

        expected_value = CustomFieldValue(
            field_id=3,
            oid=3,
            otype="policy_group",
            ts_updated="2022-02-12T13:54:24.192436Z",
            value="3 Data Policy" # <= this will be automatically parsed/converted by data model
        )

        self.assertEqual(mock_string_value, expected_value)

    # for GET method
    # this applies to multi-picker custom fields
    def test_custom_field_value_model_multi_string_value(self):
        mock_field_value_response = {
            "field_id": 3,
            "oid": 3,
            "otype": "policy_group",
            "ts_updated": "2022-02-12T13:54:24.192436Z",
            "value": [
                "red"
                , "orange"
                , "green"
            ]
        }
        mock_string_value = CustomFieldValue.from_api_response(mock_field_value_response)

        expected_value = CustomFieldValue(
            field_id=3,
            oid=3,
            otype="policy_group",
            ts_updated="2022-02-12T13:54:24.192436Z",
            value=[
                "red"
                , "orange"
                , "green"
            ] # <= this will be automatically parsed/converted by data model
        )

        self.assertEqual(mock_string_value, expected_value)

    # for GET method
    # this applies to object set and people set custom fields
    def test_custom_field_value_model_dict_value(self):
        mock_field_value_response = {
            "field_id": 3,
            "oid": 3,
            "otype": "policy_group",
            "ts_updated": "2022-02-12T13:54:24.192436Z",
            "value": [
                {"otype": "user", "oid": 1}
                , {"otype": "group", "oid": 2}
            ]
        }
        mock_string_value = CustomFieldValue.from_api_response(mock_field_value_response)

        expected_value = CustomFieldValue(
            field_id=3,
            oid=3,
            otype="policy_group",
            ts_updated="2022-02-12T13:54:24.192436Z",
            value=[
                {"otype": "user", "oid": 1}
                , {"otype": "group", "oid": 2}
            ] # <= this will be automatically parsed/converted by data model
        )

        self.assertEqual(mock_string_value, expected_value)

    # for GET method
    def test_custom_field_value_parse_string_values(self):

        mock_field_value_response = {
            "field_id": 3,
            "oid": 3,
            "otype": "policy_group",
            "ts_updated": "2022-02-12T13:54:24.192436Z",
            "value": "3 Data Policy"
        }
        mock_string_value = CustomFieldValue.from_api_response(mock_field_value_response)
        expected_string_value = CustomFieldStringValue(value="3 Data Policy")

        self.assertEqual(mock_string_value.value, expected_string_value)

    # for GET method
    def test_custom_field_value_parse_dictionary_value(self):

        mock_field_value_response = {
            "field_id": 8,
            "oid": 10,
            "otype": "business_policy",
            "ts_updated": "2022-04-06T18:37:31.427565Z",
            "value": [
                {"otype": "user", "oid": 1}
                , {"otype": "group", "oid": 2}
            ]
        }

        mock_dict_value = CustomFieldValue.from_api_response(mock_field_value_response)

        expected_dict_value = [
            CustomFieldDictValue(otype="user", oid=1),
            CustomFieldDictValue(otype="group", oid=2)
        ]

        self.assertEqual(mock_dict_value.value, expected_dict_value)

    # for PUT method
    def test_custom_field_value_item_string_value_payload(self):

        mock_item = CustomFieldValueItem(
            field_id = 1
            , oid = 1
            , otype = 'table'
            , value = CustomFieldStringValueItem(value='Testing')
        )

        expected_payload = {
            'field_id': 1
            , 'otype': 'table'
            , 'oid': 1
            , 'value': 'Testing'
        }

        self.assertEqual(mock_item.generate_api_put_payload(), expected_payload)

    # for PUT method
    def test_custom_field_value_item_dict_value_payload(self):

        mock_item = CustomFieldValueItem()
        mock_item.field_id = 1
        mock_item.oid = 1
        mock_item.otype = 'table'
        mock_item.value = []
        mock_item.value.append(CustomFieldDictValueItem(otype='table', oid=1))
        mock_item.value.append(CustomFieldDictValueItem(otype='article', oid=2))

        expected_payload = {
            'field_id': 1
            , 'otype': 'table'
            , 'oid': 1
            , 'value': [
                {'otype': 'table', 'oid': 1}
                , {'otype': 'article', 'oid': 2}
            ]
        }

        self.assertEqual(mock_item.generate_api_put_payload(), expected_payload)

    # for PUT method
    def test_custom_field_value_item_ts_updated_string_payload(self):

        mock_item = CustomFieldValueItem()
        mock_item.field_id = 1
        mock_item.oid = 1
        mock_item.otype = 'table'
        mock_item.value = CustomFieldStringValueItem(value='Testing')
        mock_item.ts_updated = '2023-11-27 4:30 PM'

        expected_payload = {
            'field_id': 1
            , 'oid': 1
            , 'otype': 'table'
            , 'ts_updated': '2023-11-27T16:30:00'
            , 'value': 'Testing'
        }

        self.assertEqual(mock_item.generate_api_put_payload(), expected_payload)

    # for PUT method
    def test_custom_field_value_item_ts_updated_datetime_payload(self):

        mock_item = CustomFieldValueItem()
        mock_item.field_id = 1
        mock_item.oid = 1
        mock_item.otype = 'table'
        mock_item.value = CustomFieldStringValueItem(value='Testing')
        mock_item.ts_updated = datetime(2023, 11, 27, 16, 30, 0, 0)

        expected_payload = {
            'field_id': 1
            , 'oid': 1
            , 'otype': 'table'
            , 'ts_updated': '2023-11-27T16:30:00'
            , 'value': 'Testing'
        }

        self.assertEqual(mock_item.generate_api_put_payload(), expected_payload)

    # for PUT method
    def test_custom_field_value_item_invalid_payload_exception(self):

        mock_item = CustomFieldValueItem()
        mock_item.field_id = 1
        mock_item.oid = 1
        mock_item.otype = 'table'

        self.assertRaises(InvalidPostBody, lambda: mock_item.generate_api_put_payload())


if __name__ == '__main__':
    unittest.main()
