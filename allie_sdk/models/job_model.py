"""Alation REST API Job Data Models."""

from dataclasses import dataclass, field

from ..core.data_structures import BaseClass


@dataclass
class AsyncJobDetails(BaseClass):
    # in some result sets job id is `job_id` while in others `id`
    job_id: int = field(default = None)
    id: int = field(default = None)
    href: str = field(default = None)
    job_name: str = field(default = None)

    def __post_init__(self):
        if self.id and self.job_id is None:
            self.job_id = self.id


@dataclass
class JobDetails(BaseClass):
    status: str = field(default = None)
    msg: str = field(default = None)
    result: str = field(default = None)