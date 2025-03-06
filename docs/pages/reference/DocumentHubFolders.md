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
- custom_fields (list of CustomFieldValueItem objects)

For a detailed description of these fields see [official Alation documentation](https://developer.alation.com/dev/reference/updatefolders).

### DocumentHubFolder

This data model represents the properties/fields that are returned by the `GET` request.

Based on model `DocumentHubFolderBase`.

Additional fields:

- id (int)
- template_id (int)
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

### create_document_hub_folders

Create document hub folders in Bulk

Args:
- `document_hub_folders`: list of `DocumentHubFolderPostItem` objects. 

Returns: 
- List of `JobDetailsDocumentHubFolderPost`: Status report of the executed background jobs.


For a detailed description see [official Alation documentation](https://developer.alation.com/dev/reference/getfolders-1).

### update_document_hub_folders

Update Document Hub Folders in Bulk

Args:
- document hub folders: This is the main payload which is a list of `DocumentHubFolderPutItem` objects.

Returns:
- List of `JobDetailsDocumentHubFolderPut`: Status report of the executed background jobs.

For a detailed description see [official Alation documentation](https://developer.alation.com/dev/reference/postfolders-1).

### update_document_hub_folders

Update Document Hub Folders in Bulk

Args:
- document_hub_folders: This is the main payload which is a list of `DocumentHubFolderPutItem` objects.

Returns:
- List of `JobDetailsDocumentHubFolderPut`: Status report of the executed background jobs.

For a detailed description see [official Alation documentation](https://developer.alation.com/dev/reference/updatefolders).

## Examples

See `/examples/example_document_hub_folder.py`.