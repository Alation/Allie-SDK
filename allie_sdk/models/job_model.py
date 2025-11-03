"""Alation REST API Job Data Models."""

from dataclasses import dataclass, field
from typing import Literal
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
class JobDetails(BaseClass):
    status: Literal["successful", "partially_successful", "failed"]
    msg: str = field(default = None)
    result: str | dict | list = field(default = None)

# --- DOCUMENT POST --- #

@dataclass(kw_only = True)
class JobDetailsDocumentPostResultDetails(BaseClass):
    id: int = field(default = None)
    title: str = field(default = None)

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
class JobDetailsDocumentPost(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, dict):
            if all(var in ("created_term_count", "created_terms") for var in self.result.keys()):
                self.result = JobDetailsDocumentPostResult.from_api_response(self.result)

# --- DOCUMENT PUT --- #

@dataclass(kw_only = True)
class JobDetailsDocumentPutResultDetails(BaseClass):
    id: int = field(default = None)
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
                if len(self.updated_terms) > 0:
                    for value in self.updated_terms:
                        if isinstance(value, dict):
                            updated_terms_out.append(JobDetailsDocumentPutResultDetails.from_api_response(value))
                        else:
                            updated_terms_out.append(value)
                    self.updated_terms = updated_terms_out

@dataclass(kw_only = True)
class JobDetailsDocumentPut(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, dict):
            if all(var in ("updated_term_count", "updated_terms") for var in self.result.keys()):
                self.result = JobDetailsDocumentPutResult.from_api_response(self.result)

# --- DOCUMENT DELETE --- #
@dataclass(kw_only = True)
class JobDetailsDocumentDeleteResult(BaseClass):
    deleted_document_count: int = field(default=None)
    deleted_document_ids: list = field(default_factory=list)
@dataclass(kw_only = True)
class JobDetailsDocumentDelete(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, dict):
            if all(var in ("deleted_document_count", "deleted_document_ids") for var in self.result.keys()):
                self.result = JobDetailsDocumentDeleteResult.from_api_response(self.result)

# --- TERM DELETE --- #
# Interestingly enough the term delete response is not in line with the document responses.
@dataclass(kw_only = True)
class JobDetailsTermDeleteResult(BaseClass):
    deleted_term_count: int = field(default=None)
    deleted_term_ids: list = field(default_factory=list)
@dataclass(kw_only = True)
class JobDetailsTermDelete(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, dict):
            if all(var in ("deleted_term_count", "deleted_term_ids") for var in self.result.keys()):
                self.result = JobDetailsTermDeleteResult.from_api_response(self.result)
# --- CUSTOM FIELD POST --- #

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
            if len(self.result) > 0:
                for value in self.result:
                    if type(value) is dict:
                        if all(var in value.keys() for var in ("msg", "data")):
                            result_out.append(JobDetailsCustomFieldPostResult.from_api_response(value))
                        else:
                            # validation errors from the Data Model get returned as a dict
                            # e.g. errors like "field_type RICH_TEXTS is not supported."
                            result_out.append(value)
                    elif isinstance(value, JobDetailsCustomFieldPostResult):
                        result_out.append(value)
                    else:
                        # somehow the job status returns a string representation of a dict
                        try:
                            value_dict = json.loads(value)

                            if isinstance(value_dict, dict):
                                if all(var in value_dict.keys() for var in ("msg", "data")):
                                    result_out.append(JobDetailsCustomFieldPostResult.from_api_response(value_dict))
                                else:
                                    result_out.append(value)
                        except json.JSONDecodeError:
                            # handle anything coming from errors
                            result_out.append(value)

                self.result = result_out

# --- RDBMS ALL --- #

@dataclass(kw_only = True)
class JobDetailsRdbmsResultMapping(BaseClass):
    id: int = field(default = None)
    key: str = field(default = None)

@dataclass(kw_only = True)
class JobDetailsRdbmsResult(BaseClass):
    response: str = field(default = None)
    mapping: list[JobDetailsRdbmsResultMapping] = field(default_factory = list)
    errors: list = field(default_factory = list)
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.mapping, list):
            mapping_out = []
            if len(self.mapping) > 0:
                for value in self.mapping:
                    if isinstance(value, dict):
                        mapping_out.append(JobDetailsRdbmsResultMapping.from_api_response(value))
                    else:
                        mapping_out.append(value)

                self.mapping = mapping_out

@dataclass(kw_only = True)
class JobDetailsRdbms(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, list):
            result_out = []
            if len(self.result) > 0:
                for value in self.result:
                    if isinstance(value, dict):
                        if all(var in value.keys() for var in ("response", "mapping", "errors")):
                            result_out.append(JobDetailsRdbmsResult.from_api_response(value))
                    else:
                        # handle anything coming from errors
                        result_out.append(value)
                self.result = result_out

# --- VIRTUAL DATASOURCE POST --- #

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

# --- DATA QUALITY --- #

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
            if all(var in ("fields", "values", "created_object_attribution", "flag_counts", "total_duration") for var in self.result.keys()):
                self.result = JobDetailsDataQualityResult.from_api_response(self.result)

# --- DOCUMENT HUB FOLDER POST --- #

@dataclass(kw_only = True)
class JobDetailsDocumentHubFolderPostResultCreatedFolder(BaseClass):
    id:int = field(default = None)
    title:str = field(default = None)

@dataclass(kw_only = True)
class JobDetailsDocumentHubFolderPostResult(BaseClass):
    created_folder_count:int = field(default = 0)
    created_folders: list = field(default_factory = list)

    def __post_init__(self):
        if isinstance(self.created_folders, list):

            created_folders_out = []
            for cf in self.created_folders:
                if isinstance(cf, dict):
                    created_folders_out.append(JobDetailsDocumentHubFolderPostResultCreatedFolder.from_api_response(cf))
            if len(created_folders_out) > 0:
                self.created_folders = created_folders_out

@dataclass(kw_only = True)
class JobDetailsDocumentHubFolderPost(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, dict):
            if all(var in ("created_folder_count", "created_folders") for var in self.result.keys()):
                self.result = JobDetailsDocumentHubFolderPostResult.from_api_response(self.result)

# --- DOCUMENT HUB FOLDER PUT --- #

@dataclass(kw_only = True)
class JobDetailsDocumentHubFolderPutResultUpdatedFolder(BaseClass):
    id:int = field(default = None)
    title:str = field(default = None)
@dataclass(kw_only = True)
class JobDetailsDocumentHubFolderPutResult(BaseClass):
    updated_folder_count:int = field(default = 0)
    updated_folders: list = field(default_factory = list)

    def __post_init__(self):
        if isinstance(self.updated_folders, list):

            updated_folders_out = []
            for cf in self.updated_folders:
                if isinstance(cf, dict):
                    updated_folders_out.append(JobDetailsDocumentHubFolderPutResultUpdatedFolder.from_api_response(cf))
            if len(updated_folders_out) > 0:
                self.updated_folders = updated_folders_out
@dataclass(kw_only = True)
class JobDetailsDocumentHubFolderPut(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, dict):
            if all(var in ("updated_folder_count", "updated_folders") for var in self.result.keys()):
                self.result = JobDetailsDocumentHubFolderPutResult.from_api_response(self.result)

# --- DOCUMENT HUB FOLDER DELETE --- #
@dataclass(kw_only = True)
class JobDetailsDocumentHubFolderDeleteResult(BaseClass):
    deleted_folder_count: int = field(default=None)
    deleted_folder_ids: list = field(default_factory=list)
@dataclass(kw_only = True)
class JobDetailsDocumentHubFolderDelete(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, dict):
            if all(var in ("deleted_folder_count", "deleted_folder_ids") for var in self.result.keys()):
                self.result = JobDetailsDocumentHubFolderDeleteResult.from_api_response(self.result)

# --- DATAFLOW POST/PATCH --- #
@dataclass(kw_only = True)
class JobDetailsDataflowPost(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, list):
            result_out = []
            if len(self.result) > 0:
                for value in self.result:
                    if isinstance(value, dict):
                        if all(var in value.keys() for var in ("response", "mapping")):
                            result_out.append(JobDetailsDataflowPostResult.from_api_response(value))
                    else:
                        # handle anything coming from errors
                        result_out.append(value)
                self.result = result_out

@dataclass(kw_only = True)
class JobDetailsDataflowPostResultMapping(BaseClass):
    id: int = field(default = None)
    external_id: str = field(default = None)
    replaced: str = field(default = None)

@dataclass(kw_only = True)
class JobDetailsDataflowPostResult(BaseClass):
    response: str = field(default = None)
    mapping: list[dict] = field(default_factory = list)

    def __post_init__(self):
        if isinstance(self.mapping, list):
            mapping_out = []
            if len(self.mapping) > 0:
                for value in self.mapping:
                    if isinstance(value, dict):
                        mapping_out.append(JobDetailsDataflowPostResultMapping.from_api_response(value))
                    else:
                        mapping_out.append(value)

                self.mapping = mapping_out


# --- DATAFLOW DELETE --- #
@dataclass(kw_only = True)
class JobDetailsDataflowDelete(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, list):
            result_out = []
            if len(self.result) > 0:
                for value in self.result:
                    if isinstance(value, dict):
                        if all(var in value.keys() for var in ("response", "mapping", "failed")):
                            result_out.append(JobDetailsDataflowDeleteResult.from_api_response(value))
                    else:
                        # handle anything coming from errors
                        result_out.append(value)
                self.result = result_out

@dataclass(kw_only = True)
class JobDetailsDataflowDeleteResultMapping(BaseClass):
    id: int = field(default = None)
    external_id: str = field(default = None)
    impacted_dfos: list = field(default_factory = list)

@dataclass(kw_only = True)
class JobDetailsDataflowDeleteResult(BaseClass):
    response: str = field(default = None)
    mapping: list[dict] = field(default_factory = list)
    failed: list[dict] = field(default_factory = list)

    def __post_init__(self):
        if isinstance(self.mapping, list):
            mapping_out = []
            if len(self.mapping) > 0:
                for value in self.mapping:
                    if isinstance(value, dict):
                        mapping_out.append(JobDetailsDataflowDeleteResultMapping.from_api_response(value))
                    else:
                        mapping_out.append(value)

                self.mapping = mapping_out
