---
title: Jobs
parent: SDK Reference
---

# Jobs
{:.no_toc}

* TOC
{:toc}

## Models

There are many data models associated to Jobs, mainly for the reason that the nested elements are not always the same. Here's a brief overview of the current models:

| **API Endpoint**                 | **Data class**                    |
| -------------------------------- |-----------------------------------|
| **Business Policy POST**         | JobDetails                        |
| **Business Policy PUT**          | JobDetails                        |
| **Custom Field POST**            | JobDetailsCustomFieldPost         |
| **Custom Field Value Async PUT** | JobDetails                        |
| **Data Quality Fields DELETE**   | JobDetailsDataQuality             |
| **Data Quality Fields POST**     | JobDetailsDataQuality             |
| **Data Quality Value DELETE**    | JobDetailsDataQuality             |
| **Data Quality Value POST**      | JobDetailsDataQuality             |
| **Document DELETE**              | JobDetailsDocumentDelete          |
| **Document Hub Folder DELETE**   | JobDetailsDocumentHubFolderDelete |
| **Document Hub Folder POST**     | JobDetailsDocumentHubFolderPost   |
| **Document Hub Folder PUT**      | JobDetailsDocumentHubFolderPut    |
| **Document POST**                | JobDetailsDocumentPost            |
| **Document PUT**                 | JobDetailsDocumentPut             |
| **RDBMS Column POST**            | JobDetailsRdbms                   |
| **RDBMS Table POST**             | JobDetailsRdbms                   |
| **RDMBS Schema POST**            | JobDetailsRdbms                   |
| **Term POST**                    | JobDetailsDocumentPost            |
| **Term PUT**                     | JobDetailsDocumentPut             |
| **Virtual Data Source POST**     | JobDetailsVirtualDatasourcePost   |
| **Virtual Filesystem POST**      | JobDetails                        |



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
