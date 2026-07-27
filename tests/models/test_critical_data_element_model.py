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

    def test_from_api_response_full_populated_object(self):
        # Mirrors a real, fully-populated CDE returned by GET /cde/.
        payload = {
            "id": 2233,
            "key": "550e8400-e29b-41d4-a716-446655440010",
            "id_no": 1001,
            "name": "Customer Social Security Number",
            "description": "Personal identifier for customer tax purposes",
            "version": 2,
            "status": "CERTIFIED",
            "cde_risk_level": "High",
            "domains": [{"id": 10, "name": "Customer Data", "source_key": "alation://domain/10"}],
            "stewards": [{"id": 201, "name": "Data Steward", "source_key": "alation://user/201"}],
            "owners": [{"id": 123, "name": "Privacy Officer", "source_key": "alation://user/123"}],
            "sources": [{"id": 321, "name": "Security Number", "source_key": "alation://glossary_term/123"}],
            "approvers": [{"id": 123, "name": "Privacy Officer", "source_key": "alation://user/123"}],
            "contributors": [{"id": 123, "name": "Privacy Officer", "source_key": "alation://user/123"}],
            "data_assets_counts": {"all": 23, "control_points": 8, "related": 13, "suggested": 2},
            "quality_score": 85.5,
            "curation_score": 0.88,
            "ts_created": "2026-03-09T09:00:00Z",
            "ts_updated": "2026-03-09T10:30:00Z",
            "created_by": {"id": 123, "name": "Privacy Officer", "source_key": "alation://user/123"},
            "updated_by": {"id": 456, "name": "Compliance Manager", "source_key": "alation://user/456"},
        }

        cde = CriticalDataElement.from_api_response(payload)

        # Scalars typed.
        assert cde.id == 2233
        assert cde.id_no == 1001
        assert cde.version == 2
        assert cde.status == "CERTIFIED"
        assert cde.cde_risk_level == "High"
        assert cde.quality_score == 85.5
        assert cde.curation_score == 0.88
        # Nested exposed as raw passthrough (not dropped).
        assert cde.owners == [{"id": 123, "name": "Privacy Officer", "source_key": "alation://user/123"}]
        assert cde.domains[0]["name"] == "Customer Data"
        assert cde.data_assets_counts["control_points"] == 8
        assert cde.created_by["id"] == 123
        assert cde.updated_by["name"] == "Compliance Manager"
        # Timestamps converted.
        assert isinstance(cde.ts_created, datetime)

    def test_from_api_response_soft_deleted_fields(self):
        # Soft-delete audit fields (present on deleted elements) are captured.
        cde = CriticalDataElement.from_api_response(
            {"id": 1, "name": "x", "deleted": True,
             "ts_deleted": "2026-07-27T04:02:19.321128Z",
             "deleted_by": {"id": 792, "name": "Adam Weisser", "source_key": "alation://user/151"}}
        )
        assert cde.deleted is True
        assert isinstance(cde.ts_deleted, datetime)
        assert cde.deleted_by["id"] == 792

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
        params = CriticalDataElementParams(search="Customer")
        assert params.generate_params_dict() == {"search": "Customer"}

    def test_params_repeatable_filters(self):
        params = CriticalDataElementParams(
            status={"CANDIDATE", "CERTIFIED"},
            risk_level={1, 2},
            version={1},
            key={"uuid-a", "uuid-b"},
        )
        result = params.generate_params_dict()
        assert result["status"] == {"CANDIDATE", "CERTIFIED"}
        assert result["risk_level"] == {1, 2}
        assert result["version"] == {1}
        assert result["key"] == {"uuid-a", "uuid-b"}

    def test_params_domain_keys_bracket_notation(self):
        # domain_keys must be serialized under the bracketed key name.
        params = CriticalDataElementParams(domain_keys={"domain1", "domain2"})
        result = params.generate_params_dict()
        assert "domain_keys" not in result
        assert result["domain_keys[]"] == {"domain1", "domain2"}

    def test_params_empty_sets_are_dropped(self):
        # Unset repeatable filters (empty sets) must not appear in the query string.
        assert CriticalDataElementParams().generate_params_dict() == {}
