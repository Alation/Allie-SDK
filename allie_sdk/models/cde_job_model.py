"""Alation Critical Data Manager (CDM / CDE) — Job Data Models.

CDE jobs are distinct from the core Alation background jobs: they have their own
endpoint (``/cde-service/integration/job/``), are identified by a uuid ``key``, and use
their own status vocabulary (``QUEUED``/``IN_PROGRESS``/``FINISHED``/``ERROR``/``CANCELED``).

See: https://developer.alation.com/dev/reference/cde-api-overview
"""

from dataclasses import dataclass, field
from datetime import datetime

from ..core.data_structures import BaseClass, BaseParams

# CDE job status vocabulary. These mirror the constants in
# ``allie_sdk/core/cde_request_handler.py`` (the poller); they are duplicated here rather
# than imported to avoid a circular import (``core.request_handler`` already imports the
# models package, so a model importing back into ``core`` closes the loop).
CDE_JOB_TERMINAL_STATUSES = ("FINISHED", "ERROR", "CANCELED")
CDE_JOB_ACTIVE_STATUSES = ("QUEUED", "IN_PROGRESS")


@dataclass
class CDEJob(BaseClass):
    """A Critical Data Manager (CDE) background job.

    Returned by the job methods and by write operations that run asynchronously
    (e.g. bulk-create). Terminal statuses are ``FINISHED`` / ``ERROR`` / ``CANCELED``.
    """
    id: int = field(default=None)
    key: str = field(default=None)  # uuid used to correlate an async write to its job
    type: str = field(default=None)  # e.g. API_BULK_CREATION
    status: str = field(default=None)
    result: dict | list = field(default=None)  # per-item outcomes / errors
    ts_created: datetime = field(default=None)
    ts_updated: datetime = field(default=None)

    def __post_init__(self):
        if isinstance(self.ts_created, str):
            self.ts_created = self.convert_timestamp(self.ts_created)
        if isinstance(self.ts_updated, str):
            self.ts_updated = self.convert_timestamp(self.ts_updated)

    @property
    def is_terminal(self) -> bool:
        """Whether the job has reached a terminal state."""
        return str(self.status or "").upper() in CDE_JOB_TERMINAL_STATUSES

    @property
    def is_successful(self) -> bool:
        """Whether the job finished successfully."""
        return str(self.status or "").upper() == "FINISHED"


@dataclass
class CDEJobParams(BaseParams):
    """Filter parameters for GET ``/cde-service/integration/job/``.

    Note:
        ``skip``/``limit`` pagination is handled by the request handler, so callers
        should generally not set them here.
    """
    type: str = field(default=None)
    status: str = field(default=None)
    order_by: str = field(default=None)
