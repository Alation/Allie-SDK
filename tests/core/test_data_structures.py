"""Test the Core Data Structure Objects."""


from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
import unittest

from allie_sdk.core.data_structures import BaseClass, BaseParams


@dataclass
class TestClass(BaseClass):
    __test__ = False
    id: int = field(default=None)
    name: str = field(default=None)
    organization: str = field(default=None)


@dataclass
class TestParams(BaseParams):
    __test__ = False
    id: set = field(default_factory=set)
    name: set = field(default_factory=set)
    organization: set = field(default_factory=set)


class TestBaseClass(unittest.TestCase):

    def test_from_api_response_all_values(self):

        mock_api_response = {'id': 1, 'name': 'Alation', 'organization': 'Sales'}
        mock_class = TestClass.from_api_response(mock_api_response)
        expected_class = TestClass(id=1, name='Alation', organization='Sales')

        self.assertEqual(mock_class, expected_class)

    def test_from_api_response_subset_of_values(self):

        mock_api_response = {'id': 1, 'name': 'Alation',}
        mock_class = TestClass.from_api_response(mock_api_response)
        expected_class = TestClass(id=1, name='Alation')

        self.assertEqual(mock_class, expected_class)

    def test_timezone_conversion_utc(self):

        mock_class = TestClass()
        mock_time = '2022-12-27T16:44:53.414125Z'
        parsed_time = mock_class.convert_timestamp(mock_time)

        self.assertEqual(parsed_time, datetime(2022, 12, 27, 16, 44, 53, 414125))

    def test_timezone_conversion_pst(self):

        mock_class = TestClass()
        mock_time = '2023-11-06T08:26:07.928812-08:00'
        parsed_time = mock_class.convert_timestamp(mock_time)

        self.assertEqual(
            parsed_time, datetime(2023, 11, 6, 8, 26, 7, 928812, tzinfo=timezone(timedelta(days=-1, seconds=57600))))


class TestBaseParams(unittest.TestCase):

    def test_generate_params_dict_all_values(self):

        mock_class = TestParams()
        mock_class.id.update([1, 2, 3,])
        mock_class.name.add('Alation')
        mock_class.organization.add('Sales')
        expected_dictionary = {'id': {1, 2, 3}, 'name': {'Alation'}, 'organization': {'Sales'}}

        self.assertEqual(mock_class.generate_params_dict(), expected_dictionary)

    def test_generate_params_dict_subset_of_values(self):

        mock_class = TestParams()
        mock_class.id.update([1, 2, 3,])
        mock_class.name.add('Alation')
        expected_dictionary = {'id': {1, 2, 3}, 'name': {'Alation'}}

        self.assertEqual(mock_class.generate_params_dict(), expected_dictionary)


if __name__ == '__main__':
    unittest.main()
