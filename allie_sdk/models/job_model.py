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
class JobDetailsResultDetails(BaseClass):
    id: int = field(default = None)
    title: str = field(default = None)
    def __post_init__(self):
        if self.title is not None:
            self.title = self.title
@dataclass(kw_only = True)
class JobDetailsResult(BaseClass):
    # for document post request
    created_term_count: int = field(default = None)
    created_terms: list[JobDetailsResultDetails] = field(default_factory = list)
    # for document put request
    updated_term_count: int = field(default = None)
    updated_terms: list[JobDetailsResultDetails] = field(default_factory = list)
    #
    def __post_init__(self):
        # Make sure the nested details gets converted to the proper data class
        # Since there is no consistent structure we need to cater for the various API endpoints

        # for document post request
        if self.created_terms:
            if isinstance(self.created_terms, list):
                # self.created_terms = [JobDetailsResultDetails.from_api_response(value) for value in self.created_terms]
                # we can't use above approach since when we create a JobDetails object for testing (in example)
                # we'd define nested classes as well. We only want to convert if it is a dict and not if it is a class already.
                created_terms_out = []
                created_objects_dict_counter = 0
                for value in self.created_terms:
                    if isinstance(value, dict):
                        created_objects_dict_counter += 1
                        created_terms_out.append(JobDetailsResultDetails.from_api_response(value))

                # we only want to override self.created_terms if we found nested dict objects
                # otherwise we want to keep the class based objects (say we create nested class based objects for tests
                # in example)
                if created_objects_dict_counter > 0:
                    self.created_terms = created_terms_out
        # for document put request
        if self.updated_terms:
            if isinstance(self.updated_terms, list):
                updated_terms_out = []
                updated_objects_dict_counter = 0
                for value in self.updated_terms:
                    if isinstance(value, dict):
                        updated_objects_dict_counter += 1
                        updated_terms_out.append(JobDetailsResultDetails.from_api_response(value))
                if updated_objects_dict_counter > 0:
                    self.updated_terms = updated_terms_out
        # TODO: Catering for other endpoint results

# required for custom field POST
@dataclass(kw_only = True)
class JobDetailsCustomFieldResultData(BaseClass):
    field_ids: list[int] = field(default_factory = list)

@dataclass(kw_only = True)
class JobDetailsCustomFieldResult(BaseClass):
    msg: str = field(default = None)
    data: dict = field(default_factory = dict)
    def __post_init__(self):
        if isinstance(self.data, dict):
            self.data = JobDetailsCustomFieldResultData.from_api_response(self.data)

@dataclass(kw_only = True)
class JobDetails(BaseClass):
    status: str = field(default = None)
    msg: str = field(default = None)
    result: str | dict | list = field(default = None)
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, dict):
            self.result = JobDetailsResult.from_api_response(self.result)
        if isinstance(self.result, list):
            self.result = JobDetailsCustomFieldResult.from_api_response(self.result)

"""
TODO:
The problem is we don't have a context: Ideally we create specific data classes for the API endpoints.
Currently the transformation to data classes is done in a global/core module - hence no context.
Solution: We could move this logic to the actual methods so that we have better control over the
transformation to data classes.

Actually, this wouldn't really help, since how to apply the classes to the nested elements is defined here?

=> make dedicated models per API endpoint. But inherit from a base model.

JobDetailsBase

JobDetailsDocumentPut(JobDetailsBase)
"""
