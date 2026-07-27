"""Test the Critical Data Manager (CDM / CDE) Job data models."""
from datetime import datetime

from allie_sdk.models.cde_job_model import *


class TestCDEJobModel:

    def test_from_api_response_ignores_unknown_keys(self):
        job = CDEJob.from_api_response(
            {"id": 1, "key": "abc-123", "type": "API_BULK_CREATION",
             "status": "FINISHED", "unexpected": "x"}
        )
        assert job.id == 1
        assert job.key == "abc-123"
        assert job.type == "API_BULK_CREATION"
        assert job.status == "FINISHED"

    def test_from_api_response_converts_timestamps(self):
        job = CDEJob.from_api_response(
            {"id": 1, "ts_created": "2026-07-16T10:20:30.000000Z"}
        )
        assert isinstance(job.ts_created, datetime)

    def test_is_terminal(self):
        assert CDEJob(status="FINISHED").is_terminal is True
        assert CDEJob(status="ERROR").is_terminal is True
        assert CDEJob(status="CANCELED").is_terminal is True
        assert CDEJob(status="QUEUED").is_terminal is False
        assert CDEJob(status="IN_PROGRESS").is_terminal is False
        assert CDEJob(status=None).is_terminal is False

    def test_is_successful(self):
        assert CDEJob(status="FINISHED").is_successful is True
        assert CDEJob(status="ERROR").is_successful is False

    def test_params_drops_unset_values(self):
        params = CDEJobParams(type="API_BULK_CREATION")
        assert params.generate_params_dict() == {"type": "API_BULK_CREATION"}
