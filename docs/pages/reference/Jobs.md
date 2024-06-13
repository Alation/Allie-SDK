---
title: Jobs
parent: SDK Reference
---

# Jobs
{:.no_toc}

* TOC
{:toc}

## Models

### AsyncJobDetails
Model representing an asynchrous Alation job

Attributes:

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| id          | int                   | Job object ID |
| job_id          | int                   | Job object ID |
| href          | str                   | href of the Job |

{: .note }
In some result sets job id is `job_id` while in others `id`


### JobDetails
Model representing an Alation job

Attributes:

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| status   | str                   | Indicates the status of the job. Status can be one of the following: `running`, `successful`, `failed` |
| msg | str                   | Message describing the time taken to complete the job and the timestamp of job completion. |
| result | str                   | Contains detailed information about the job. The format of the result depends on the API that initiated the job. |

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
