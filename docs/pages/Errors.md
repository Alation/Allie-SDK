---
title: Request Status and Errors
nav_order: 7
---

{:.no_toc}

# Errors


There are at least **four error types** that an **Allie-SDK based request call** can return:

- **Data type validation error**:  For `POST`, `PUT` and `PATCH` payloads **Allie SDK** validates the data type(s) you submit for the payload (usually via  the `validate_rest_payload()` method). 
- **Value Validation**: For `POST`, `PUT` and `PATCH` payloads **Allie SDK** in some cases checks whether valid values were set for certain fields (usually this is implemented as part of the `generate_api_post_payload()` method).
- **Batch error**: **Allie SDK** will batch your payload if it is above a certain threshold. If anything goes wrong with batching your payload, an error will be thrown. Applies to **async jobs** only and the following methods: `POST`, `PUT`, `PATCH`.
- **Request error**: errors returned from the `requests` module. 
- **Invalid Payload**: Some **Async Alation API endpoints** validate the payload before submitting the request. If the payload is invalid, an error will be reported, usually with hints on how to fix the problem.


> **Important**: The execution of a job might be successful, but this doesn't mean that the request was overall successful. In some cases (e.g. for the Data Quality API endpoint) the API endpoints returns some additional information (e.g. that a certain object was not found and that hence the object couldn't be created). So while overall the status is shown as successful, always check the returned response to understand if your request was really successful.


We made an effort make the **data structure** of these error messages **consistent** by mapping them to a **data class** of type `JobDetails` or similar. In a nutshell, the top level structure will always contain the following **properties**:

- `status`: this is either:
  - `successful`
  - `partially_successful` (e.g. with data dictionary upload)
  - `failed`
- `msg`: a brief error message.
- `result`: any other details

So you should always be able to use the `status` property to evaluate whether a job was executed successfully or not.

> **Note**: If you find that this is not the case with a specific API call, please issue an [Issue](https://github.com/Alation/Allie-SDK/issues) on **GitHub**.


Async `POST`, `PUT` and `PATCH` requests should always return a **list** of objects based on the `JobDetails` data class or similar. Why is a list returned you might wonder? This is because Allie-SDK batches your payload and for each batch one job is executed.

Synchronous `POST`, `PUT`, `PATCH` and also `DELETE` requests return usually one object based on the `JobDetails` data class or similar.


## Request error

This is an error returned from the `requests` module on any of the methods (`GET`, `PATCH`, `POST`, `PUT`).

Example of this could be: 

- connection problem
- wrong endpoint URL
- etc

A note to Allie-SDK developers: This is handled by the `_map_request_error_to_job_details` method in `request_handler.py`.

## Invalid Payload

Some Async Alation API endpoints validate the payload before submitting the request. If the payload is invalid, no **job id** will be returned but instead details about what makes the payload invalid. Allie-SDK logs these payload violations. The reason why we only log it and not return it is because you can't really base any subsequent logic on it: In example, if the payload validation returns an error that the data source id does not exist, we cannot magically fix this within the code. So these errors are best just logged out.

## Batch error

> **Note**: This applies to **async** jobs only and the following methods: `POST`, `PUT`, `PATCH`.

These are any errors resulting from attempting to batch your payload.

A note to Allie-SDK developers: This is handled by the `_map_batch_error_to_job_details` method in `async_handler.py`.


