"""Alation REST API Job Data Models."""

from dataclasses import dataclass, field

from ..core.data_structures import BaseClass


@dataclass
class AsyncJobDetails(BaseClass):
    # in some result sets job id is `job_id` while in others `id`
    job_id: int = field(default = None)
    id: int = field(default = None)
    href: str = field(default = None)

    def __post_init__(self):
        if self.id and self.job_id is None:
            self.job_id = self.id

@dataclass(kw_only = True)
class JobDetailsResultCreatedObjects(BaseClass):
    id: int = field(default = None)
    title: str = field(default = None)
@dataclass(kw_only = True)
class JobDetailsResult(BaseClass):
    created_term_count: int = field(default = None)
    # created_terms:list = field(default_factory = list)
    created_terms: list[JobDetailsResultCreatedObjects] = field(default_factory = list)
    def __post_init__(self):
        # Make sure the nested details gets converted to the proper data class
        # Since there is no consistent structure we need to cater for the various API endpoints
        # Catering for Document PUT results
        if self.created_terms:
            if isinstance(self.created_terms, list):
                # self.created_terms = [JobDetailsResultCreatedObjects.from_api_response(value) for value in self.created_terms]
                # we can't use above approach since when we create a JobDetails object for testing (in example)
                # we'd define nested classes as well. We only want to convert if it is a dict and not if it is a class already.
                self.created_terms = []
                for value in self.created_terms:
                    if isinstance(value, dict):
                        self.created_terms.append(JobDetailsResultCreatedObjects.from_api_response(value))
        # TODO: Catering for other endpoint results
@dataclass
class JobDetails(BaseClass):
    status: str = field(default = None)
    msg: str = field(default = None)
    result: str | JobDetailsResult = field(default = None)
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, dict):
            self.result = JobDetailsResult.from_api_response(self.result)

