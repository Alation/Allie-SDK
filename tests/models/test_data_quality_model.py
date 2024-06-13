"""Test the Alation REST API Data Quality Models"""

import unittest
from allie_sdk.models.data_quality_model import *


class TestDataQualityModels(unittest.TestCase):

    def test_data_quality_field(self):

        data_quality_field_response = {
            "key": "1.dq.test",
            "name": "expect_table_row_count_to_be_between",
            "description": "Table contains between 10000-15000 rows",
            "type": "STRING",
            "ts_created": "2022-06-01T18:26:54.663432Z"
        }
        dq_field = DataQualityField.from_api_response(data_quality_field_response)

        mock_dq_field = DataQualityField(
            key='1.dq.test',
            name='expect_table_row_count_to_be_between',
            description='Table contains between 10000-15000 rows',
            type='STRING',
            ts_created='2022-06-01T18:26:54.663432Z'
        )

        self.assertEqual(dq_field, mock_dq_field)

    def test_data_quality_field_item_payload(self):

        mock_dq_field = DataQualityFieldItem(
            field_key="1.dq.test",
            name="Testing the DQ Field",
            type="BOOLEAN"
        )
        expected_payload = {
            "field_key": "1.dq.test", "name": "Testing the DQ Field", "type": "BOOLEAN"
        }

        self.assertEqual(mock_dq_field.generate_api_post_payload(), expected_payload)

    def test_data_quality_field_item_exception_missing_key(self):

        mock_dq_field = DataQualityFieldItem(
            name="Testing the DQ Field",
            type="BOOLEAN",
            description="This is a test!"
        )

        self.assertRaises(InvalidPostBody, lambda: mock_dq_field.generate_api_post_payload())

    def test_data_quality_field_item_exception_missing_name(self):

        mock_dq_field = DataQualityFieldItem(
            field_key="1.dq.test",
            type="BOOLEAN",
            description="This is a test!"
        )

        self.assertRaises(InvalidPostBody, lambda: mock_dq_field.generate_api_post_payload())

    def test_data_quality_field_item_exception_missing_type(self):

        mock_dq_field = DataQualityFieldItem(
            field_key="1.dq.test",
            name="Testing the DQ Field",
            description="This is a test!"
        )

        self.assertRaises(InvalidPostBody, lambda: mock_dq_field.generate_api_post_payload())

    def test_data_quality_field_item_exception_invalid_type(self):

        mock_dq_field = DataQualityFieldItem(
            field_key="1.dq.test",
            name="Testing the DQ Field",
            description="This is a test!",
            type="VARCHAR"
        )

        self.assertRaises(InvalidPostBody, lambda: mock_dq_field.generate_api_post_payload())

    def test_data_quality_value(self):

        data_quality_value_response =  {
            "object_key": "10.northstar_logistics.customer",
            "object_name": "customer",
            "otype": "table",
            "oid": 716,
            "source_object_key": "10.northstar_logistics.customer.shipping_state",
            "source_object_name": "shipping_state",
            "source_otype": "attribute",
            "source_oid": 64837,
            "value_id": 389,
            "value_value": 97.76,
            "value_quality": "ALERT",
            "value_last_updated": "2023-09-18T00:48:32.428817Z",
            "value_external_url": "https://datagovernance.alationproserv.com/1/5/dashboard",
            "field_key": "10.northstar_logistics.customer.rule.15",
            "field_name": "Shipping_State is not null",
            "field_description": "Rows Fail: 12, Pass: 523, Ignore: 0"
        }
        dq_value = DataQualityValue.from_api_response(data_quality_value_response)

        mock_dq_value = DataQualityValue(
            object_key="10.northstar_logistics.customer",
            object_name="customer",
            otype="table",
            oid=716,
            source_object_key="10.northstar_logistics.customer.shipping_state",
            source_object_name="shipping_state",
            source_otype="attribute",
            source_oid=64837,
            value_id=389,
            value_value=97.76,
            value_quality="ALERT",
            value_last_updated="2023-09-18T00:48:32.428817Z",
            value_external_url="https://datagovernance.alationproserv.com/1/5/dashboard",
            field_key="10.northstar_logistics.customer.rule.15",
            field_name="Shipping_State is not null",
            field_description="Rows Fail: 12, Pass: 523, Ignore: 0"
        )

        self.assertEqual(dq_value, mock_dq_value)

    def test_data_quality_value_delete_payload(self):

        mock_dq_value = DataQualityValue(
            field_key='1.dq.test',
            object_key='1.table.test'
        )
        expected_payload = {'field_key': '1.dq.test', 'object_key': '1.table.test'}

        self.assertEqual(mock_dq_value.generate_api_delete_payload(), expected_payload)

    def test_data_quality_value_delete_exception_missing_field_key(self):

        mock_dq_value = DataQualityValue(
            object_key='1.table.test'
        )

        self.assertRaises(InvalidPostBody, lambda: mock_dq_value.generate_api_delete_payload())

    def test_data_quality_value_delete_exception_missing_object_key(self):

        mock_dq_value = DataQualityValue(
            field_key='1.dq.test',
        )

        self.assertRaises(InvalidPostBody, lambda: mock_dq_value.generate_api_delete_payload())

    def test_data_quality_value_item_payload(self):

        mock_dq_value = DataQualityValueItem(
            field_key='1.dq.test',
            object_key='1.table.test',
            object_type='table',
            status='good',
            value='The test passes',
            url='https://test.com'
        )
        expected_payload = {
            'field_key': '1.dq.test', 'object_key': '1.table.test', 'object_type': 'TABLE',
            'status': 'GOOD', 'value': 'The test passes', 'url': 'https://test.com'
        }

        self.assertEqual(mock_dq_value.generate_api_post_payload(), expected_payload)

    def test_data_quality_value_exception_missing_field_key(self):

        mock_dq_value = DataQualityValueItem(
            object_key='1.table.test',
            object_type='table',
            status='good',
            value='The test passes',
            url='https://test.com'
        )

        self.assertRaises(InvalidPostBody, lambda: mock_dq_value.generate_api_post_payload())

    def test_data_quality_value_exception_missing_object_key(self):

        mock_dq_value = DataQualityValueItem(
            field_key='1.dq.test',
            object_type='table',
            status='good',
            value='The test passes',
            url='https://test.com'
        )

        self.assertRaises(InvalidPostBody, lambda: mock_dq_value.generate_api_post_payload())

    def test_data_quality_value_exception_missing_object_type(self):

        mock_dq_value = DataQualityValueItem(
            field_key='1.dq.test',
            object_key='1.table.test',
            status='good',
            value='The test passes',
            url='https://test.com'
        )

        self.assertRaises(InvalidPostBody, lambda: mock_dq_value.generate_api_post_payload())

    def test_data_quality_value_exception_missing_status(self):

        mock_dq_value = DataQualityValueItem(
            field_key='1.dq.test',
            object_key='1.table.test',
            object_type='table',
            value='The test passes',
            url='https://test.com'
        )

        self.assertRaises(InvalidPostBody, lambda: mock_dq_value.generate_api_post_payload())

    def test_data_quality_value_exception_missing_value(self):

        mock_dq_value = DataQualityValueItem(
            field_key='1.dq.test',
            object_key='1.table.test',
            object_type='table',
            status='good',
            url='https://test.com'
        )

        self.assertRaises(InvalidPostBody, lambda: mock_dq_value.generate_api_post_payload())

    def test_data_quality_value_exception_invalid_object_type(self):

        mock_dq_value = DataQualityValueItem(
            field_key='1.dq.test',
            object_key='1.table.test',
            object_type='bi_report',
            status='good',
            value='The test passes',
            url='https://test.com'
        )

        self.assertRaises(InvalidPostBody, lambda: mock_dq_value.generate_api_post_payload())

    def test_data_quality_value_exception_invalid_status(self):

        mock_dq_value = DataQualityValueItem(
            field_key='1.dq.test',
            object_key='1.table.test',
            object_type='bi_report',
            status='pass',
            value='The test passes',
            url='https://test.com'
        )

        self.assertRaises(InvalidPostBody, lambda: mock_dq_value.generate_api_post_payload())


if __name__ == '__main__':
    unittest.main()
