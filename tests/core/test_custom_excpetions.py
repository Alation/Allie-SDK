"""Test the Core Custom Exceptions"""

from dataclasses import dataclass, field
import unittest

from allie_sdk.core.custom_exceptions import *


@dataclass
class TestParams1:
    __test__ = False
    test: str = field(default=None)


@dataclass
class TestParams2:
    __test__ = False
    test: str = field(default=None)


@dataclass
class TestPayload1:
    __test__ = False
    test: str = field(default=None)


@dataclass
class TestPayload2:
    __test__ = False
    test: str = field(default=None)


class TestCustomExceptions(unittest.TestCase):

    def test_validate_query_params_no_exception(self):

        mock_params = TestParams1()
        validate_query_params(mock_params, TestParams1)

    def test_validate_query_params_raise_exception(self):

        mock_params = TestParams2()

        self.assertRaises(UnsupportedQueryParams, lambda: validate_query_params(mock_params, TestParams1))

    def test_validate_rest_payload_no_exception(self):

        mock_payload = [TestPayload1(), TestPayload1()]
        validate_rest_payload(mock_payload, (TestPayload1,))

    def test_validate_rest_payload_raise_exception(self):

        mock_payload = [TestPayload1(), TestPayload2()]

        self.assertRaises(UnsupportedPostBody, lambda: validate_rest_payload(mock_payload, (TestPayload1,)))

    def test_validate_rest_payload_no_exception_multiple_types(self):

        mock_payload = [TestPayload1(), TestPayload2()]
        validate_rest_payload(mock_payload, (TestPayload1, TestPayload2))



if __name__ == '__main__':
    unittest.main()
