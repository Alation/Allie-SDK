---
title: Jobs
parent: SDK Reference
---

# Jobs
{:.no_toc}

* TOC
{:toc}

## Models

There are many data models associated to Jobs, mainly for the reason that the nested elements are not always the same. Here's a brief overview of the current models (this is not a complete list):

| **API Endpoint** | Method             | **Data class**                    |
|------------|--------------------|-----------------------------------|
| Business Policy | POST               | JobDetails                        |
| Business Policy | PUT                | JobDetails                        |
| Custom Field | POST               | JobDetailsCustomFieldPost      |
| Custom Field Value Async | PUT                | JobDetails                     |
| Data Quality Fields | DELETE             | JobDetailsDataQuality          |
| Data Quality Fields | POST               | JobDetailsDataQuality        |
| Data Quality Value | DELETE             | JobDetailsDataQuality      |
| Data Quality Value | POST               | JobDetailsDataQuality    |
| Document   | DELETE             | JobDetailsDocumentDelete |
| Document Hub Folder | DELETE             | JobDetailsDocumentHubFolderDelete |
| Document Hub Folder | POST               | JobDetailsDocumentHubFolderPost |
| Document Hub Folder | PUT                | JobDetailsDocumentHubFolderPut  |
| Document  | POST               | JobDetailsDocumentPost        |
| Document   | PUT                | JobDetailsDocumentPut     |
| RDBMS Column |  POST | JobDetailsRdbms               |
| RDBMS Table |  POST | JobDetailsRdbms               |
| RDMBS Schema | POST | JobDetailsRdbms             |
| Term  |  POST | JobDetailsDocumentPost    |
| Term   | PUT   | JobDetailsDocumentPut  |
| User - Remove Duplicated User Accounts | POST               | JobDetails |
| Virtual Data Source  |  POST | JobDetailsVirtualDatasourcePost |
| Virtual Filesystem  |  POST | JobDetails           |

## Methods

### __init__

```
__init__(access_token: str, session: requests.Session, host: str, job_response: dict)
```

Creates an instance of the Job object.

Args:
* access_token (str): Alation REST API Access Token.
* session (requests.Session): Python requests common session.
* host (str): Alation URL.
* job_response (dict): Alation REST API Async Job Details.

### check_job_status

```
check_job_status()
```

Query the Alation Background Job and Log Status until Job has completed


### _get_job

```
_get_job() -> JobDetails
```

Query the Alation Job.

Returns:
* JobDetails: Alation Job.

## For Allie-SDK Developers

### Design Decisions

Job results are not standardised. Nearly every endpoint and method use some custom data model.
Ideally we create specific data classes for each API endpoint and method combination.

Previously the transformation from the returned dict to an object based on a data classes was done in a global/core module (`job.py`). This didn't provide any context (endpoint name and method).

The solution to this was to have `job.py` return just the vanilla job object and then to do the transformation/mapping in the specific methods (e.g. `post_custom_fields` in `custom_field.py`). This provides the necessary context.


Example of vanilla job details returned by a successful custom field POST request:

```python
[
    {
        'status': 'successful'
        , 'msg': 'Job finished in 0.025975 seconds at 2024-09-17 12:50:42.653908+00:00'
        , 'result': [
            '{"msg": "Starting bulk creation of Custom Fields...", "data": {}}'
            , '{"msg": "Finished bulk creation of Custom Fields", "data": {"field_ids": [10323]}}'
        ]
    }
]
```

Note that the result includes several messages, seemingly one from the start of the process and the final one. In the specific method `post_custom_fields` in `custom_field.py` we map this to the relevant data class.


#### Errors

We could already map the error data to `JobDetails` within the `_map_request_error_to_job_details` and `_map_batch_error_to_job_details` methods, however, that would mean that on the main function level (e.g. `put_custom_field_values`) we would need to check whether a list with object based on a data class gets returned (e.g. `JobDetails`) or a list with dicts. So at this point the logic could get a bit complex and every main function would have to implement this logic.

Instead, we decided to simple return a dict with the `_map_request_error_to_job_details` and `_map_batch_error_to_job_details` methods, so that in the main function level (e.g. `put_custom_field_values`) we can just call `JobDetails.from_api_response(item)` for anything that gets returned.

This in turn means that variations of `JobDetails` will have to implement some logic to store these error data within their structure, but in this case it is managed only in one place, so it's easier to maintain.

Errors are sometimes returned as a list or dictionary:

Example of an error returned as a list (in this case by the custom field PUT API endpoint):

```
[{'options': ['Expected a list of items but got type "str".']}]
```

Example of an error returned as a dict (in this case by the Custom Field Value PUT API endpoint):

```
{'code': '400000', 'detail': 'Please check the API documentation for more details on the spec.', 'errors': [{'non_field_errors': ['No support for updating `description` field for `data`.']}], 'title': 'Invalid Payload'}
```

In general we don't make an attempt to map these error structures to a specific data structure since it would take a long time to cover all error messages. Since we want to make sure that the results returned by Allie-SDK functions are always consistent, we nest these error messages/structures within the `result` property of a `JobDetails` (or similar) based object.

To make sure we integrate these errors correctly into the `JobDetails` (or similar) structure, we need to be extra careful with the nested data structure mapping. In the example below, we map `result` to `JobDetailsDocumentPostResult` if the properties `created_term_count` and `created_terms` are present in the dictionary. In all other cases the error details, whether of type list or dict, will be left untouched and hence just stay as is within the existing structure:

```python
@dataclass(kw_only = True)
class JobDetailsDocumentPost(JobDetails):
    def __post_init__(self):
        # Make sure the nested result gets converted to the proper data class
        if isinstance(self.result, dict):
            if all(var in ("created_term_count", "created_terms") for var in self.result.keys()):
                self.result = JobDetailsDocumentPostResult.from_api_response(self.result)
```