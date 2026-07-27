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

    def test_generate_api_post_payload_with_optional_fields(self):
        item = CriticalDataElementItem(
            name="Customer SSN",
            status="DRAFT",
            risk_level_value=3,
            risk_level_label="High",
            risk_rationale="Contains PII",
            owners=[{"id": 123, "name": "Privacy Officer", "source_key": "alation://user/123"}],
            domains=[{"id": 10, "name": "Customer Data", "source_key": "alation://domain/10"}],
            fields=[{"key": "k1", "derived_requirements": []}],
            pdes=[{
                "relationship": "control_point", "name": "PDE1", "source_key": "PDE1 Key",
                "path": [{"type": "schema", "name": "S1"}],
            }],
        )
        payload = item.generate_api_post_payload()

        assert payload["name"] == "Customer SSN"
        assert payload["risk_level_value"] == 3
        assert payload["risk_level_label"] == "High"
        assert payload["risk_rationale"] == "Contains PII"
        assert payload["owners"][0]["source_key"] == "alation://user/123"
        assert payload["domains"][0]["id"] == 10
        assert payload["fields"] == [{"key": "k1", "derived_requirements": []}]
        assert payload["pdes"][0]["relationship"] == "control_point"

    def test_generate_api_put_payload_omits_pdes(self):
        # pdes is a create-only field; it must not appear in the update payload.
        item = CriticalDataElementItem(
            name="X",
            owners=[{"id": 1, "name": "O", "source_key": "alation://user/1"}],
            pdes=[{"relationship": "control_point", "name": "PDE1"}],
        )
        payload = item.generate_api_put_payload()

        assert payload["name"] == "X"
        assert payload["owners"][0]["id"] == 1
        assert "pdes" not in payload

    def test_fields_validation_missing_key(self):
        item = CriticalDataElementItem(name="x", fields=[{"derived_requirements": []}])
        with pytest.raises(InvalidPostBody, match=r"fields\[0\].*key"):
            item.generate_api_post_payload()

    def test_fields_validation_missing_inner_value(self):
        item = CriticalDataElementItem(
            name="x",
            fields=[{
                "key": "k1",
                "derived_requirements": [{"key": "dr1", "fields": [{"key": "f1"}]}],
            }],
        )
        with pytest.raises(InvalidPostBody, match=r"fields\[0\].derived_requirements\[0\].fields\[0\].*value"):
            item.generate_api_post_payload()

    def test_fields_validation_applies_to_update_too(self):
        item = CriticalDataElementItem(name="x", fields=[{"key": "k1"}])
        with pytest.raises(InvalidPostBody, match="derived_requirements"):
            item.generate_api_put_payload()

    def test_pdes_validation_invalid_relationship(self):
        item = CriticalDataElementItem(
            name="x",
            pdes=[{"name": "P", "relationship": "bogus", "source_key": "k",
                   "path": [{"type": "t", "name": "n"}]}],
        )
        with pytest.raises(InvalidPostBody, match="relationship must be one of"):
            item.generate_api_post_payload()

    def test_pdes_validation_missing_path(self):
        item = CriticalDataElementItem(
            name="x",
            pdes=[{"name": "P", "relationship": "related", "source_key": "k"}],
        )
        with pytest.raises(InvalidPostBody, match=r"pdes\[0\].*path"):
            item.generate_api_post_payload()

    def test_pdes_validation_path_level_missing_type(self):
        item = CriticalDataElementItem(
            name="x",
            pdes=[{"name": "P", "relationship": "related", "source_key": "k",
                   "path": [{"name": "n"}]}],
        )
        with pytest.raises(InvalidPostBody, match=r"pdes\[0\].path\[0\].*type"):
            item.generate_api_post_payload()

    def test_from_api_response_risk_object_and_fields(self):
        # get responses return a risk_level OBJECT (plus risk_rationale/confidence) and
        # the read-side overlay-standard `fields` — all exposed as raw passthrough.
        cde = CriticalDataElement.from_api_response(
            {
                "id": 1,
                "name": "x",
                "risk_level": {"value": 3, "label": "High", "number_of_levels": 3},
                "risk_rationale": "Contains PII",
                "risk_confidence": 0.95,
                "fields": [{"key": "k1", "name": "Data Privacy Standard", "type": "OVERLAY"}],
            }
        )
        assert cde.risk_level == {"value": 3, "label": "High", "number_of_levels": 3}
        assert cde.risk_rationale == "Contains PII"
        assert cde.risk_confidence == 0.95
        assert cde.fields[0]["type"] == "OVERLAY"

    def test_risk_level_default_labels_reference(self):
        # Fixed 1-3 value scale; labels are the tenant-configurable defaults.
        assert CDE_RISK_LEVEL_DEFAULT_LABELS == {1: "Low", 2: "Medium", 3: "High"}

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
