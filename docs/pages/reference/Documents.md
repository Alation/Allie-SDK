---
title: Documents
parent: SDK Reference
---

# Documents
{:.no_toc}

* TOC
{:toc}

## Models

### DocumentBase
Sub-model used in the parent Models of `Document`, `DocumentPostItem`, and `DocumentPutItem`.

Attributes:

| Name            | Type | Description                                                                                                     |
|-----------------|------|-----------------------------------------------------------------------------------------------------------------|
| title           | str  | The title of the document                                                                                       |
| description     | str  | The description of the document                                                                                 |
| template_id     | int  | The ID of the custom template assigned to the document                                                          |   
|         parent_folder_id        | int  | The ID of the folder to assign as the parent of the document                                                    |
| nav_link_folder_ids      | list | An array containing the folder IDs that the document has navigation links to                                    |
| document_hub_id | int  | The ID of the Document Hub assigned to the document                                                             |
| custom_fields   | list | A list of `CustomFieldValueItem` objects containing custom field information relative to the custom template ID |

### Document
Individual list item returned in the response of the function `get_documents` that represents a document in Alation.

Attributes:

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| id          | int                   | The ID of the document        |
| deleted   | bool                   | Will return only deleted documents when set to True |
| ts_deleted | datetime                   | ISO-8601 formatted timestamp of when the document was deleted |
| ts_created | datetime                   | ISO-8601 formatted timestamp of when the document was created |
| ts_updated | datetime                   | ISO-8601 formatted timestamp of when the document was updated |

### DocumentPutItem
Python object used to create a `Document` in Alation and passed in the parameter `documents` as a list in the function `update_documents`.

Attributes:

| Name         | Required | Type                  | Description                                                  |
|--------------|:--------:|-----------------------|--------------------------------------------------------------|
| id           |  TRUE    | int         | The ID of the document object to update | 

### DocumentParams
Optional item used to filter the response of the returned data from the function `get_documents`.

Attributes:

| Name            | Type  | Description                                                                                                                |
|-----------------|-------|----------------------------------------------------------------------------------------------------------------------------|
| id              | int   | Filter by document ID   |
| folder_id       | int   | The ID of the folder whose documents you want to get.|
| document_hub_id | int   | The ID of the Document Hub whose documents you want to get. |
| search          | str   | Filter by document title |
| deleted         | bool   | Will return only deleted documents when set to True. |
| values          | str  | A comma-separated list of fields to be included in the response. When provided, the API will return only the specified set of fields for each object in the response. If not supplied, the API will return all fields by default. |



## Methods
### get_documents

```
get_documents(query_params:DocumentParams = None) -> list[Document]
```

Query multiple Alation Documents and return their details

Args:
* query_params (`DocumentParams`): REST API Documents Query Parameters.
Returns:
* list: Alation Documents

### create_documents

```
create_documents(documents: list[DocumentPostItem]) -> list[JobDetailsDocumentPost]
```

Create documents in Bulk


Args:
* documents: list of `DocumentPostItem` objects

Returns:
* List of JobDetails: Status report of the executed background jobs.

### update_documents

```
update_documents(documents: list[DocumentPutItem]) -> list[JobDetailsDocumentPut]
```

Update Documents in Bulk

Args:
* documents: list of `DocumentPutItem` objects

Returns:
* List of JobDetails: Status report of the executed background jobs.

### delete_documents

```
delete_documents(documents:list[Document]) -> JobDetailsDocumentDelete:
```

Bulk delete documents

Args:
* documents (list): List of `Document` objects

Returns:
* List of JobDetails: Status report of the executed background jobs.


## Examples

See `/examples/example_document.py`.



