---
title: Document Hub Folders
parent: SDK Reference
---

# Document Hub Folders
{:.no_toc}

* TOC
{:toc}

## Models

### DocumentHubFolderBase

This data class includes properties/fields that are common to:

- `DocumentHubFolder`
- `DocumentHubFolderPostItem`
- `DocumentHubFolderPutItem`

Additionally it includes the `_create_fields_payload` which is used only for:

- `DocumentHubFolderPostItem`
- `DocumentHubFolderPutItem`

Fields:

- title (string)
- description (string)
- document_hub_id (int)
- template_id (int)
- custom_fields (list of CustomFieldValueItem objects)

`template_id` is now supported for folder create and update payloads. Use it when the API expects the folder template context, especially when sending `custom_fields`.

For a detailed description of these fields see [official Alation documentation](https://developer.alation.com/dev/reference/updatefolders).

### DocumentHubFolder

This data model represents the properties/fields that are returned by the `GET` request.

Based on model `DocumentHubFolderBase`.

Additional fields:

- id (int)
- template_id (int)
- parent_folder_id (int)
- child_documents_count (int)
- child_folders_count (int)
- nav_links_count (int)
- deleted (bool)
- ts_deleted (str)
- ts_created (str)
- ts_updated (str)

For a detailed description of these fields see [official Alation documentation](https://developer.alation.com/dev/reference/getfolders-1).

### DocumentHubFolderPostItem

This data model represents the properties/fields for one particular document hub folder object for the `POST` request.

Based on model `DocumentHubFolderBase`.

Additional fields: None

For a detailed description of these fields see [official Alation documentation](https://developer.alation.com/dev/reference/postfolders-1).

### DocumentHubFolderPutItem

This data model represents the properties/fields for one particular document hub folder object for the `PUT` request.

Based on model `DocumentHubFolderBase`.

Additional fields:

- id (int)
- parent_folder_id (int)

For a detailed description of these fields see [official Alation documentation](https://developer.alation.com/dev/reference/updatefolders).

### DocumentHubFolderParams

This data model represents the **query parameters** used for the `GET` request.

Fields:

- id (int)
- document_hub_id (int)
- search (str)
- deleted (bool)
- values (str)

For a detailed description of these fields see [official Alation documentation](https://developer.alation.com/dev/reference/getfolders-1).

## Methods

### get_document_hub_folders

Get document hub folders.

Args:
- `query_params`: optional `DocumentHubFolderParams` object. Supported query parameters are `id`, `document_hub_id`, `search`, `deleted`, and `values`.

Returns:
- `list[DocumentHubFolder]`

For a detailed description see [official Alation documentation](https://developer.alation.com/dev/reference/getfolders-1).

### create_document_hub_folders

Create document hub folders in Bulk

Args:
- `document_hub_folders`: list of `DocumentHubFolderPostItem` objects. 

Notes:
- `title` and `document_hub_id` are required.
- `template_id` is supported in the payload.
- If you submit `custom_fields`, include the matching `template_id` used by the folder template.

Returns: 
- List of `JobDetailsDocumentHubFolderPost`: Status report of the executed background jobs.


For a detailed description see [official Alation documentation](https://developer.alation.com/dev/reference/postfolders-1).

### update_document_hub_folders

Update Document Hub Folders in Bulk

Args:
- `document_hub_folders`: This is the main payload which is a list of `DocumentHubFolderPutItem` objects.

Returns:
- List of `JobDetailsDocumentHubFolderPut`: Status report of the executed background jobs.

Notes:
- `id` is required.
- `template_id` is supported in the payload.
- `parent_folder_id` is supported in the payload.
- If you submit `custom_fields`, include the matching `template_id` used by the folder template.

For a detailed description see [official Alation documentation](https://developer.alation.com/dev/reference/updatefolders).

### delete_document_hub_folders

Delete document hub folders in bulk.

Args:
- `document_hub_folders`: list of `DocumentHubFolder` objects. Only the `id` is required for deletion.

Returns:
- `JobDetailsDocumentHubFolderDelete`

For a detailed description see [official Alation documentation](https://developer.alation.com/dev/reference/deletefolders-1).

## Examples

See `/examples/example_document_hub_folder.py`.
