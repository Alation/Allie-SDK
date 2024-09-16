---
title: Errors
nav_order: 7
---

# Errors
{:.no_toc}

There are at least **three error types** that an **Allie-SDK based request call** can return:

- **Error details returned by API endpoint**
- **Exception error**:
- **Batch error**: If anything goes wrong with batching your payload. Applies Async jobs only and the following methods: `POST`, `PUT`, `PATCH`.


We made an effort make the **data structure** of these error messages **consistent** by mapping them to a **data class** of type `JobDetails` or similar. In a nutshell, the top level structure will always contain the following **properties**:

- `status`: this is either `success` or `failed`
- `msg`: a brief error message.
- `result`: any other details

So you should always be able to use the `status` property to evaluate whether a job was executed successfully or not.

> **Note**: If you find that this is not the case with a specific API call, please issue an **Issue** on **GitHub**.x

## Error details returned by API endpoint

Example of this could be information returned by the API endpoint that a certain element or value within your payload is not valid.

## Request error

This is an error returned from the request module on any of the methods (`GET`, `PATCH`, `POST`, `PUT`).

This is handled by the `_map_request_error_to_job_details` method in `request_handler.py`.

## Batch error

> **Note**: This applies to **async** jobs only and the following methods: `POST`, `PUT`, `PATCH`.

These are any errors resulting from attempting to batch your payload.

This is handled by the `_map_batch_error_to_job_details` method in `async_handler.py`.

# Allie-SDK development

## Notes on design decisions

We could already map the error data to `JobDetails` within the `_map_request_error_to_job_details` and `_map_batch_error_to_job_details` methods, however, that would mean that on the main function level (e.g. `put_custom_field_values`) we would need to check whether a list with object based on a data class gets returned (e.g. `JobDetails`) or a list with dicts. So it this point the logic could get a bit complex and every main function would have to implement this logic.

Instead, we decided to simple return a dict with the `_map_request_error_to_job_details` and `_map_batch_error_to_job_details` methods, so that on the main function level (e.g. `put_custom_field_values`) we can just call `JobDetails.from_api_response(item)` for anything that gets returned.

This in turn means that variations of `JobDetails` will have to implement some logic to store these error data within their structure, but in this case it is managed only in one place, so it's easier to maintain.
