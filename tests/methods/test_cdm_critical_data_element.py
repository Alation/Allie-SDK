"""Test the Alation Critical Data Manager (CDM / CDE) Critical Data Element Methods."""
import pytest
import requests

from allie_sdk.methods.cdm_critical_data_element import *
from allie_sdk.models.cde_job_model import CDEJob
from allie_sdk.models.critical_data_element_model import (
    CriticalDataElementItem,
    CriticalDataElementParams,
)
from allie_sdk.core.custom_exceptions import InvalidPostBody, UnsupportedPostBody


CDE_TOKEN_STRING = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.cde_payload.cde_signature"


class TestCDMCriticalDataElement:

    def setup_method(self):
        self.cde = AlationCDMCriticalDataElement(
            access_token="alation-access-token",
            session=requests.session(),
            host="https://test.com",
        )
        # Keep pagination page size small so multi-page behaviour is easy to exercise.
        self.cde.cde_page_size = 2

    def _register_auth(self, requests_mock):
        requests_mock.register_uri(
            "POST", "/cde-service/integration/auth/", text=CDE_TOKEN_STRING
        )

    def test_get_critical_data_elements_bare_array(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri(
            "GET",
            "/cde-service/integration/cde/",
            json=[{"id": 1, "name": "Customer ID", "status": "CERTIFIED"}],
        )

        result = self.cde.get_critical_data_elements()

        assert len(result) == 1
        assert isinstance(result[0], CriticalDataElement)
        assert result[0].name == "Customer ID"
        # CDE calls must carry the CDEToken header (never Token).
        assert requests_mock.last_request.headers.get("CDEToken") == CDE_TOKEN_STRING
        assert requests_mock.last_request.headers.get("Token") is None

    def test_get_critical_data_elements_wrapped_shape(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri(
            "GET",
            "/cde-service/integration/cde/",
            json={"items": [{"id": 5, "name": "Account No"}]},
        )

        result = self.cde.get_critical_data_elements()

        assert len(result) == 1
        assert result[0].id == 5

    def test_get_critical_data_elements_paginates(self, requests_mock):
        self._register_auth(requests_mock)
        full_page = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]
        short_page = [{"id": 3, "name": "c"}]

        def _responder(request, context):
            context.status_code = 200
            skip = int(request.qs.get("skip", ["0"])[0])
            return full_page if skip == 0 else short_page

        requests_mock.register_uri("GET", "/cde-service/integration/cde/", json=_responder)

        result = self.cde.get_critical_data_elements()

        assert [c.id for c in result] == [1, 2, 3]

    def test_get_critical_data_elements_with_status_filter(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri(
            "GET", "/cde-service/integration/cde/", json=[]
        )

        self.cde.get_critical_data_elements(
            query_params=CriticalDataElementParams(status={"CERTIFIED"})
        )

        assert requests_mock.last_request.qs.get("status") == ["certified"]

    def test_get_critical_data_elements_repeatable_and_bracket_filters(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri("GET", "/cde-service/integration/cde/", json=[])

        self.cde.get_critical_data_elements(
            query_params=CriticalDataElementParams(
                status={"CANDIDATE", "PENDING_OWNERS_APPROVAL"},
                risk_level={1, 2},
                domain_keys={"domain1", "domain2"},
                latest_only=True,
            )
        )

        qs = requests_mock.last_request.qs
        # Repeatable filters are serialized as multiple values.
        assert sorted(qs.get("status")) == ["candidate", "pending_owners_approval"]
        assert sorted(qs.get("risk_level")) == ["1", "2"]
        # domain_keys uses the bracketed key name.
        assert sorted(qs.get("domain_keys[]")) == ["domain1", "domain2"]
        assert qs.get("latest_only") == ["true"]

    def test_get_critical_data_elements_empty(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri("GET", "/cde-service/integration/cde/", json=[])

        assert self.cde.get_critical_data_elements() == []

    def test_get_critical_data_element_by_id(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri(
            "GET",
            "/cde-service/integration/cde/42/",
            json={"id": 42, "name": "Customer ID", "status": "DRAFT"},
        )

        result = self.cde.get_critical_data_element(42)

        assert isinstance(result, CriticalDataElement)
        assert result.id == 42
        assert result.status == "DRAFT"

    # --- single create ----------------------------------------------------

    def test_create_critical_data_element(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri(
            "POST",
            "/cde-service/integration/cde/",
            json={"id": 7, "name": "Customer ID", "status": "CANDIDATE"},
            status_code=201,
        )

        result = self.cde.create_critical_data_element(
            CriticalDataElementItem(name="Customer ID", status="CANDIDATE")
        )

        assert isinstance(result, CriticalDataElement)
        assert result.id == 7
        # Request carried the CDEToken (never Token) and the expected body.
        assert requests_mock.last_request.headers.get("CDEToken") == CDE_TOKEN_STRING
        assert requests_mock.last_request.headers.get("Token") is None
        assert requests_mock.last_request.json() == {
            "name": "Customer ID", "status": "CANDIDATE"
        }

    def test_create_critical_data_element_with_optional_fields_and_allow_duplicates(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri(
            "POST", "/cde-service/integration/cde/",
            json={"id": 9, "name": "Customer SSN"}, status_code=201,
        )

        self.cde.create_critical_data_element(
            CriticalDataElementItem(
                name="Customer SSN",
                risk_level_value=3,
                owners=[{"id": 123, "name": "Privacy Officer", "source_key": "alation://user/123"}],
            ),
            allow_duplicates=True,
        )

        body = requests_mock.last_request.json()
        assert body["name"] == "Customer SSN"
        assert body["risk_level_value"] == 3
        assert body["owners"][0]["source_key"] == "alation://user/123"
        assert body["options"] == {"allow_duplicates": True}

    def test_create_critical_data_element_requires_name(self, requests_mock):
        self._register_auth(requests_mock)
        with pytest.raises(InvalidPostBody):
            self.cde.create_critical_data_element(CriticalDataElementItem(description="no name"))

    def test_create_critical_data_element_rejects_wrong_type(self, requests_mock):
        self._register_auth(requests_mock)
        with pytest.raises(UnsupportedPostBody):
            self.cde.create_critical_data_element({"name": "not an item"})

    # --- bulk create ------------------------------------------------------

    def test_create_bulk_waits_for_job(self, requests_mock):
        self._register_auth(requests_mock)
        bulk = requests_mock.register_uri(
            "POST", "/cde-service/integration/cde/bulk/", json={"job_key": "job-123"}
        )
        # The poller finds the job terminal.
        requests_mock.register_uri(
            "GET",
            "/cde-service/integration/job/",
            json=[{"id": 1, "key": "job-123", "status": "FINISHED", "result": {"created": 2}}],
        )

        result = self.cde.create_critical_data_elements_bulk(
            [CriticalDataElementItem(name="a"), CriticalDataElementItem(name="b")],
            poll_interval=0,
        )

        assert isinstance(result, CDEJob)
        assert result.status == "FINISHED"
        # Verify the bulk request body shape.
        bulk_body = bulk.last_request.json()
        assert bulk_body["cdes"] == [{"name": "a"}, {"name": "b"}]
        assert bulk_body["options"] == {"allow_duplicates": False}

    def test_create_bulk_no_wait_returns_key(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri(
            "POST", "/cde-service/integration/cde/bulk/", json={"key": "job-999"}
        )

        result = self.cde.create_critical_data_elements_bulk(
            [CriticalDataElementItem(name="a")], wait_for_completion=False
        )

        assert result == "job-999"

    def test_create_bulk_allow_duplicates_passed_through(self, requests_mock):
        self._register_auth(requests_mock)
        bulk = requests_mock.register_uri(
            "POST", "/cde-service/integration/cde/bulk/", json={"job_key": "j"}
        )
        requests_mock.register_uri(
            "GET",
            "/cde-service/integration/job/",
            json=[{"id": 1, "key": "j", "status": "FINISHED"}],
        )

        self.cde.create_critical_data_elements_bulk(
            [CriticalDataElementItem(name="a")], allow_duplicates=True, poll_interval=0
        )

        assert bulk.last_request.json()["options"] == {"allow_duplicates": True}

    def test_create_bulk_rejects_over_max(self, requests_mock):
        self._register_auth(requests_mock)
        too_many = [CriticalDataElementItem(name=f"cde-{i}") for i in range(CDE_BULK_MAX + 1)]
        with pytest.raises(ValueError, match="at most"):
            self.cde.create_critical_data_elements_bulk(too_many)

    def test_create_bulk_raises_when_no_job_key(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri(
            "POST", "/cde-service/integration/cde/bulk/", json={"unexpected": "shape"}
        )
        with pytest.raises(ValueError, match="no job key"):
            self.cde.create_critical_data_elements_bulk([CriticalDataElementItem(name="a")])

    # --- update -----------------------------------------------------------

    def test_update_critical_data_element(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri(
            "PUT",
            "/cde-service/integration/cde/42/",
            json={"id": 42, "name": "Renamed", "description": "new desc"},
            status_code=200,
        )

        result = self.cde.update_critical_data_element(
            42, CriticalDataElementItem(name="Renamed", description="new desc")
        )

        assert isinstance(result, CriticalDataElement)
        assert result.name == "Renamed"
        assert requests_mock.last_request.json() == {"name": "Renamed", "description": "new desc"}
        assert requests_mock.last_request.headers.get("CDEToken") == CDE_TOKEN_STRING
        assert requests_mock.last_request.headers.get("Token") is None

    def test_update_critical_data_element_omits_status(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri(
            "PUT", "/cde-service/integration/cde/42/", json={"id": 42, "name": "X"}
        )

        # status is set on the item but must NOT be sent on an update.
        self.cde.update_critical_data_element(
            42, CriticalDataElementItem(name="X", status="CERTIFIED")
        )

        assert requests_mock.last_request.json() == {"name": "X"}

    def test_update_critical_data_element_rejects_wrong_type(self, requests_mock):
        self._register_auth(requests_mock)
        with pytest.raises(UnsupportedPostBody):
            self.cde.update_critical_data_element(42, {"name": "not an item"})

    # --- delete -----------------------------------------------------------

    def test_delete_critical_data_element(self, requests_mock):
        self._register_auth(requests_mock)
        delete = requests_mock.register_uri(
            "DELETE", "/cde-service/integration/cde/42/", status_code=204
        )

        result = self.cde.delete_critical_data_element(42)

        assert result is None
        assert delete.called
        assert requests_mock.last_request.headers.get("CDEToken") == CDE_TOKEN_STRING

    def test_delete_critical_data_elements_bulk(self, requests_mock):
        self._register_auth(requests_mock)
        bulk_delete = requests_mock.register_uri(
            "POST",
            "/cde-service/integration/cde/bulk_delete/",
            json={"detail": "Critical Data Elements deleted successfully"},
            status_code=200,
        )

        result = self.cde.delete_critical_data_elements_bulk([1, 2, 3])

        assert result is None
        assert bulk_delete.called
        assert requests_mock.last_request.json() == {"ids": [1, 2, 3]}
        assert requests_mock.last_request.headers.get("CDEToken") == CDE_TOKEN_STRING

    def test_delete_critical_data_elements_bulk_rejects_empty(self, requests_mock):
        self._register_auth(requests_mock)
        with pytest.raises(ValueError, match="at least one"):
            self.cde.delete_critical_data_elements_bulk([])
