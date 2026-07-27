"""Test the Alation Critical Data Manager (CDM / CDE) Job Methods."""
import pytest
import requests

from allie_sdk.methods.cdm_job import *
from allie_sdk.models.cde_job_model import CDEJob, CDEJobParams


CDE_TOKEN_STRING = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.cde_payload.cde_signature"


class TestCDMJob:

    def setup_method(self):
        self.job = AlationCDMJob(
            access_token="alation-access-token",
            session=requests.session(),
            host="https://test.com",
        )

    def _register_auth(self, requests_mock):
        requests_mock.register_uri(
            "POST", "/cde-service/integration/auth/", text=CDE_TOKEN_STRING
        )

    def test_get_cde_jobs(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri(
            "GET",
            "/cde-service/integration/job/",
            json=[{"id": 1, "key": "abc", "type": "API_BULK_CREATION", "status": "FINISHED"}],
        )

        result = self.job.get_cde_jobs()

        assert len(result) == 1
        assert isinstance(result[0], CDEJob)
        assert result[0].status == "FINISHED"
        # CDE calls must carry the CDEToken header (never Token).
        assert requests_mock.last_request.headers.get("CDEToken") == CDE_TOKEN_STRING
        assert requests_mock.last_request.headers.get("Token") is None

    def test_get_cde_jobs_with_type_filter(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri("GET", "/cde-service/integration/job/", json=[])

        self.job.get_cde_jobs(query_params=CDEJobParams(type="API_BULK_CREATION"))

        assert requests_mock.last_request.qs.get("type") == ["api_bulk_creation"]

    def test_get_cde_jobs_empty(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri("GET", "/cde-service/integration/job/", json=[])

        assert self.job.get_cde_jobs() == []

    def test_get_cde_job_by_id(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri(
            "GET",
            "/cde-service/integration/job/55/",
            json={"id": 55, "key": "xyz", "status": "IN_PROGRESS"},
        )

        result = self.job.get_cde_job(55)

        assert isinstance(result, CDEJob)
        assert result.id == 55
        assert result.status == "IN_PROGRESS"

    def test_cancel_cde_job(self, requests_mock):
        self._register_auth(requests_mock)
        cancel = requests_mock.register_uri(
            "POST", "/cde-service/integration/job/55/cancel/", json={"status": "CANCELED"}
        )

        self.job.cancel_cde_job(55)

        assert cancel.called
        assert requests_mock.last_request.method == "POST"

    def test_wait_for_cde_job_polls_until_terminal(self, requests_mock):
        self._register_auth(requests_mock)
        # The job list endpoint returns the job progressing through statuses.
        requests_mock.register_uri(
            "GET",
            "/cde-service/integration/job/",
            [
                {"json": [{"id": 1, "key": "job-key", "status": "QUEUED"}]},
                {"json": [{"id": 1, "key": "job-key", "status": "IN_PROGRESS"}]},
                {"json": [{"id": 1, "key": "job-key", "status": "FINISHED",
                           "result": {"created": 3}}]},
            ],
        )

        result = self.job.wait_for_cde_job("job-key", poll_interval=0)

        assert isinstance(result, CDEJob)
        assert result.status == "FINISHED"
        assert result.is_successful is True

    def test_wait_for_cde_job_returns_on_error_status(self, requests_mock):
        self._register_auth(requests_mock)
        requests_mock.register_uri(
            "GET",
            "/cde-service/integration/job/",
            json=[{"id": 1, "key": "job-key", "status": "ERROR", "result": {"msg": "boom"}}],
        )

        result = self.job.wait_for_cde_job("job-key", poll_interval=0)

        assert result.status == "ERROR"
        assert result.is_terminal is True
        assert result.is_successful is False

    def test_wait_for_cde_job_times_out(self, requests_mock):
        self._register_auth(requests_mock)
        # Job never reaches a terminal state.
        requests_mock.register_uri(
            "GET",
            "/cde-service/integration/job/",
            json=[{"id": 1, "key": "job-key", "status": "IN_PROGRESS"}],
        )

        with pytest.raises(TimeoutError):
            self.job.wait_for_cde_job("job-key", poll_interval=0, timeout=0.05)
