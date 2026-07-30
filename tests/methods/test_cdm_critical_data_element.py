"""Test the Alation Critical Data Manager (CDM / CDE) Critical Data Element Methods."""
import requests

from allie_sdk.methods.cdm_critical_data_element import *
from allie_sdk.models.critical_data_element_model import CriticalDataElementParams


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
            query_params=CriticalDataElementParams(status="CERTIFIED")
        )

        assert requests_mock.last_request.qs.get("status") == ["certified"]

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
