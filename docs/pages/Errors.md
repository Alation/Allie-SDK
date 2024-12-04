---
title: Request Status and Errors
nav_order: 7
---

# Request Status

Request types:

`GET`: There's no status returned here, you either get the data returned that you asked for or nothing at all or an error message.

`DELETE`:

- TODO: No status, msg, result top level!

`POST`:

- async:
  - success: status `successful`
  - payload content validation fails: status `failed`
  - other errors: status `failed`, although, it might fail before that?
- sync: ?
  - success: status `successful`
  - payload content validation fails: status `failed`
  - other errors: it will fail right away???

'PUT':

`PATCH`:



# Errors
{:.no_toc}

There are at least **three error types** that an **Allie-SDK based request call** can return:

- **Data model validation error**: in some cases the `generate_api_post_payload` method of a given data class validates the input structure and will throw an error if certain conditions are not met. This process is usually triggered by the `validate_rest_payload` method within the Allie-SDK methods. (in example: `allie_sdk.core.custom_exceptions.InvalidPostBody`).
- **Request error**: examples are connection error, invalid payload etc.
- **Batch error**: If anything goes wrong with batching your payload. Applies Async jobs only and the following methods: `POST`, `PUT`, `PATCH`.

> **Important**: The execution of a job might be successful, but this doesn't mean that the request was overall successful. In some cases (e.g. data quality) the API endpoints returns some additional information (e.g. that a certain object was not found and that hence the object couldn't be created). So while overall the status is shown as successful, always check the returned response to understand if your request was really successful.


We made an effort make the **data structure** of these error messages **consistent** by mapping them to a **data class** of type `JobDetails` or similar. In a nutshell, the top level structure will always contain the following **properties**:

- `status`: this is either `successful` or `failed`
- `msg`: a brief error message.
- `result`: any other details

So you should always be able to use the `status` property to evaluate whether a job was executed successfully or not.

> **Note**: If you find that this is not the case with a specific API call, please issue an **Issue** on **GitHub**.x


## Request error

This is an error returned from the request module on any of the methods (`GET`, `PATCH`, `POST`, `PUT`).

Example of this could be: 

- information returned by the API endpoint that a certain element or value within your payload is not valid. 
- connection problem
- wrong endpoint URL
- etc

This is handled by the `_map_request_error_to_job_details` method in `request_handler.py`.


### Invalid Payload

Some Async Alation API endpoints validate the payload before submitting the request. If the payload is invalid, no job id will be returned but instead details about what makes the payload invalid. Allie-SDK logs these payload violations. The reason why we only log it and not return it is because you can't really base any subsequent logic on it: In example, if the payload validation returns an error that the data source id does not exist, we cannot magically fix this within the code. So these errors are best just logged out.



## Batch error

> **Note**: This applies to **async** jobs only and the following methods: `POST`, `PUT`, `PATCH`.

These are any errors resulting from attempting to batch your payload.

This is handled by the `_map_batch_error_to_job_details` method in `async_handler.py`.


