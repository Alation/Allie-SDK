"""Test the Critical Data Element (CDM / CDE) data models."""
from datetime import datetime

import pytest

from allie_sdk.models.critical_data_element_model import *
from allie_sdk.core.custom_exceptions import InvalidPostBody


class TestCriticalDataElementModel:

    def test_from_api_response_ignores_unknown_keys(self):
        cde = CriticalDataElement.from_api_response(
            {"id": 1, "name": "Customer ID", "status": "CERTIFIED", "unexpected": "x"}
        )
        assert cde.id == 1
        assert cde.name == "Customer ID"
        assert cde.status == "CERTIFIED"

    def test_from_api_response_converts_timestamps(self):
        cde = CriticalDataElement.from_api_response(
            {"id": 1, "name": "x", "ts_created": "2026-07-16T10:20:30.000000Z"}
        )
        assert isinstance(cde.ts_created, datetime)
        assert cde.ts_created.year == 2026

    def test_generate_api_post_payload_minimal(self):
        item = CriticalDataElementItem(name="Customer ID")
        assert item.generate_api_post_payload() == {"name": "Customer ID"}

    def test_generate_api_post_payload_full(self):
        item = CriticalDataElementItem(
            name="Customer ID", description="The unique customer identifier", status="CANDIDATE"
        )
        assert item.generate_api_post_payload() == {
            "name": "Customer ID",
            "description": "The unique customer identifier",
            "status": "CANDIDATE",
        }

    def test_generate_api_post_payload_requires_name(self):
        with pytest.raises(InvalidPostBody):
            CriticalDataElementItem(description="no name").generate_api_post_payload()

    def test_generate_api_put_payload_includes_set_fields(self):
        item = CriticalDataElementItem(name="Renamed", description="new")
        assert item.generate_api_put_payload() == {"name": "Renamed", "description": "new"}

    def test_generate_api_put_payload_excludes_status(self):
        # status is not an update field; it must be omitted even if set.
        item = CriticalDataElementItem(name="X", status="CERTIFIED")
        assert item.generate_api_put_payload() == {"name": "X"}

    def test_generate_api_put_payload_partial(self):
        assert CriticalDataElementItem(description="only desc").generate_api_put_payload() == {
            "description": "only desc"
        }

    def test_params_drops_unset_values(self):
        params = CriticalDataElementParams(status="CERTIFIED")
        assert params.generate_params_dict() == {"status": "CERTIFIED"}
