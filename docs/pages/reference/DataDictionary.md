---
title: Data Dictionary
parent: SDK Reference
---

# Data Dictionary
{: .no_toc }

* TOC
{:toc}

## Models

### UploadDataDictionaryRequestPayload
Payload helper used with `upload_data_dictionary` to describe the multipart form data required by the API.

Key attributes:

| Name | Required | Type | Description |
|------|:--------:|------|-------------|
| overwrite_values | TRUE | bool | When `true`, values in Alation are overwritten by the upload. |
| allow_reset | FALSE | bool | Reset existing values when the file contains blank entries. Only used when `overwrite_values` is `true`. |
| file | TRUE | Path \| bytes \| file-like | The CSV/TSV file contents to upload. |
| file_name | FALSE | str | Overrides the filename sent in the multipart request. |
| content_type | FALSE | str | MIME type of the uploaded file. Defaults to `text/csv`. |

### AsyncTaskDetails
Represents the asynchronous task created when a data dictionary upload is accepted. Use `task.links` for follow-up requests.

### DataDictionaryTaskDetails
Describes the status of an upload task, including progress information and the final result once the task completes.

### DataDictionaryTaskError
Represents a single error emitted during processing. Inspect the nested `details` attribute for the affected record range.

## Methods

### `upload_data_dictionary(object_type, object_id, payload)`

Upload a data dictionary file for a supported catalog object. Returns `AsyncTaskDetails` describing the asynchronous task.

```python
payload = allie.UploadDataDictionaryRequestPayload(
    overwrite_values=True,
    allow_reset=False,
    file="/path/to/dictionary.csv",
)

task = alation.data_dictionary.upload_data_dictionary("data", 5, payload)
print(task.task.id)
```

### `get_data_dictionary_task_details(task_id)`

Fetches a `DataDictionaryTaskDetails` record for the supplied task id. Use this to monitor task progress until the `state` is `COMPLETED`.

```python
details = alation.data_dictionary.get_data_dictionary_task_details(task.task.id)
print(details.state, details.status)
```

### `get_data_dictionary_task_errors(task_id)`

Returns a list of `DataDictionaryTaskError` objects describing failures encountered during processing. The list is empty when no errors were reported.

```python
errors = alation.data_dictionary.get_data_dictionary_task_errors(task.task.id)
for error in errors:
    print(error.timestamp, error.error_message)
```
