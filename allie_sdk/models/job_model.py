"""Alation REST API Job Data Models."""

from dataclasses import dataclass, field

from ..core.data_structures import BaseClass
import json

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


"""
Job results are not standardised. Nearly every endpoint and method use some custom data model.
Ideally we create specific data classes for each API endpoints and method combination.
Previously the transformation from the returned dict to an object based on a data classes 
was done in a global/core module (`job.py`).
This didn't provide any context (endpoint name and method).

The solution to this was to have `job.py` return just the vanilla job object and then
to do the transformation/mapping in the specific methods. This provides the necessary context.
"""


@dataclass(kw_only = True)
class JobDetailsDocumentPostResultDetails(BaseClass):
    id: int = field(default = None)
    title: str = field(default = None)

@dataclass(kw_only = True)
class JobDetailsDocumentPutResultDetails(BaseClass):
    id: int = field(default = None)

@dataclass(kw_only = True)
class JobDetailsDocumentPostResult(BaseClass):
    created_term_count: int = field(default = None)
    created_terms: list = field(default_factory = list)

    def __post_init__(self):
        if self.created_terms:
            if isinstance(self.created_terms, list):
                # self.created_terms = [JobDetailsDocumentPostResultDetails.from_api_response(value) for value in self.created_terms]
                # we can't use above approach since when we create a JobDetails object for testing (in example)
                # we'd define nested classes as well. We only want to convert if it is a dict and not if it is a class already.
                created_terms_out = []
                created_objects_dict_counter = 0
                for value in self.created_terms:
                    if isinstance(value, dict):
                        created_objects_dict_counter += 1
                        created_terms_out.append(JobDetailsDocumentPostResultDetails.from_api_response(value))

                # we only want to override self.created_terms if we found nested dict objects
                # otherwise we want to keep the class based objects (say we create nested class based objects for tests
                # in example)
                if created_objects_dict_counter > 0:
                    self.created_terms = created_terms_out


@dataclass(kw_only = True)
class JobDetailsDocumentPutResult(BaseClass):
    updated_term_count: int = field(default = None)
    updated_terms: list = field(default_factory = list)
    #
    def __post_init__(self):
        # Make sure the nested details gets converted to the proper data class
        if self.updated_terms:
            if isinstance(self.updated_terms, list):
                updated_terms_out = []
                updated_objects_dict_counter = 0
                for value in self.updated_terms:
                    if isinstance(value, dict):
                        updated_objects_dict_counter += 1
                        updated_terms_out.append(JobDetailsDocumentPutResultDetails.from_api_response(value))
                if updated_objects_dict_counter > 0:
                    self.updated_terms = updated_terms_out

@dataclass(kw_only = True)
class JobDetails(BaseClass):
    status: str = field(default = None)
    msg: str = field(default = None)
    result: str | dict | list = field(default = None)


@dataclass(kw_only = True)
class JobDetailsDocumentPost(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, dict):
            self.result = JobDetailsDocumentPostResult.from_api_response(self.result)

@dataclass(kw_only = True)
class JobDetailsDocumentPut(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, dict):
            self.result = JobDetailsDocumentPutResult.from_api_response(self.result)


@dataclass(kw_only = True)
class JobDetailsCustomFieldPostResultData(BaseClass):
    field_ids: list[int] = field(default_factory = list)

@dataclass(kw_only = True)
class JobDetailsCustomFieldPostResult(BaseClass):
    msg: str = field(default = None)
    data: dict = field(default_factory = dict)
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.data, dict):
            self.data = JobDetailsCustomFieldPostResultData.from_api_response(self.data)

@dataclass(kw_only = True)
class JobDetailsCustomFieldPost(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, list):
            result_out = []
            result_counter = 0
            for value in self.result:
                if isinstance(value, dict):
                    result_counter += 1
                    result_out.append(JobDetailsCustomFieldPostResult.from_api_response(value))
            if result_counter > 0:
                self.result = result_out

@dataclass(kw_only = True)
class JobDetailsRdbmsResultMapping(BaseClass):
    id: int = field(default = None)
    key: str = field(default = None)
@dataclass(kw_only = True)
class JobDetailsRdbmsResult(BaseClass):
    response: str = field(default = None)
    mapping: list[dict] = field(default_factory = list)
    errors: list = field(default_factory = list)
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.mapping, list):
            mapping_out = []
            mapping_counter = 0
            for value in self.mapping:
                if isinstance(value, dict):
                    mapping_counter += 1
                    mapping_out.append(JobDetailsRdbmsResultMapping.from_api_response(value))
            if mapping_counter > 0:
                self.mapping = mapping_out
@dataclass(kw_only = True)
class JobDetailsRdbms(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, list):
            result_out = []
            result_counter = 0
            for value in self.result:
                if isinstance(value, dict):
                    result_counter += 1
                    result_out.append(JobDetailsRdbmsResult.from_api_response(value))
            if result_counter > 0:
                self.result = result_out


@dataclass(kw_only = True)
class JobDetailsVirtualDatasourcePostResult(BaseClass):
    number_received:int = field(default = None)
    updated_objects:int = field(default = None)
    error_objects:list = field(default_factory = list)
    error: str = field(default = None)
@dataclass(kw_only = True)
class JobDetailsVirtualDatasourcePost(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, str):
            result_tmp = json.loads(self.result)
            self.result = JobDetailsVirtualDatasourcePostResult.from_api_response(result_tmp)

@dataclass(kw_only=True)
class JobDetailsDataQualityResultActionStats(BaseClass):
    count: int = field(default = 0)
    sample: list = field(default_factory = list)

@dataclass(kw_only=True)
class JobDetailsDataQualityResultAction(BaseClass):
    created: dict | JobDetailsDataQualityResultActionStats = field(default_factory = dict)
    updated: dict | JobDetailsDataQualityResultActionStats = field(default_factory = dict)
    deleted: dict | JobDetailsDataQualityResultActionStats = field(default_factory = dict)
    not_found: dict | JobDetailsDataQualityResultActionStats = field(default_factory = dict)

    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.created, dict):
            self.created = JobDetailsDataQualityResultActionStats.from_api_response(self.created)
        if isinstance(self.updated, dict):
            self.updated = JobDetailsDataQualityResultActionStats.from_api_response(self.updated)
        if isinstance(self.deleted, dict):
            self.deleted = JobDetailsDataQualityResultActionStats.from_api_response(self.deleted)
        if isinstance(self.not_found, dict):
            self.not_found = JobDetailsDataQualityResultActionStats.from_api_response(self.not_found)

@dataclass(kw_only=True)
class JobDetailsDataQualityResultCreatedObjectAttribution(BaseClass):
    success_count: int = field(default = 0)
    failure_count: int = field(default = 0)
    success_sample: list = field(default_factory = list)
    failure_sample: list = field(default_factory = list)
@dataclass(kw_only=True)
class JobDetailsDataQualityResult(BaseClass):
    fields: dict | JobDetailsDataQualityResultAction = field(default_factory = dict)
    values: dict | JobDetailsDataQualityResultAction = field(default_factory = dict)
    created_object_attribution: dict | JobDetailsDataQualityResultCreatedObjectAttribution = field(default_factory = dict)
    flag_counts: dict = field(default_factory = dict)
    total_duration: float = field(default = None)

    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.fields, dict):
            self.fields = JobDetailsDataQualityResultAction.from_api_response(self.fields)
        if isinstance(self.values, dict):
            self.values = JobDetailsDataQualityResultAction.from_api_response(self.values)
        if isinstance(self.created_object_attribution, dict):
            self.created_object_attribution = JobDetailsDataQualityResultCreatedObjectAttribution.from_api_response(self.created_object_attribution)

@dataclass(kw_only = True)
class JobDetailsDataQuality(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, dict):
            self.result = JobDetailsDataQualityResult.from_api_response(self.result)