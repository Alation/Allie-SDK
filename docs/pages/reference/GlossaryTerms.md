---
title: Glossary Terms
parent: SDK Reference
---

# Glossary Terms
{:.no_toc}

* TOC
{:toc}

## Models

### BaseGlossaryTerm
Sub-model used in the parent Models of `GlossaryTerm` and `GlossaryTerm`.

Attributes:

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| id          | int                   | Term object ID |
| title    | str                   | Title of the Term object |
| description    | str                   | Description of the Term object|   
| template_id | int                   | The ID of the custom template assigned to the Term|
| glossary_ids | list                   | An list containing the glossary IDs that the Term is a member of |
| custom_fields | list                   | A list of `CustomFieldValueItem` objects containing custom field information relative to the custom template ID |

### GlossaryTerm
Individual list item returned in the response of the function `get_glossary_terms` that represents a term in Alation.

Attributes:

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| deleted   | bool                   | Determines if a Term is deleted |
| ts_deleted | datetime                   | ISO-8601 formatted timestamp of when the term was deleted |
| ts_created | datetime                   | ISO-8601 formatted timestamp of when the term was created |
| ts_updated | datetime                   | ISO-8601 formatted timestamp of when the term was updated |

### GlossaryTermItem
Python object used to create a `GlossaryTerm` in Alation and passed in the parameter `glossary_terms` as a list in the functions `post_glossary_terms` and `put_glossary_terms`.

Attributes:

Inherits attributes from `BaseGlossaryTerm`

### GlossaryTermParams
Optional item used to filter the response of the returned data from the function `get_glossary_terms`.

Attributes:

| Name  | Type  | Description                                                                                                                |
|-------|-------|----------------------------------------------------------------------------------------------------------------------------|
| id   | set   | The ID of the Term  |
| search | str   | Filter by Term title |
| deleted | bool   | Will return only deleted Terms when set to True. |


## Methods
### get_glossary_terms

```
get_glossary_terms(query_params: GlossaryTermParams = None) -> list[GlossaryTerm]
```

Get the details of all Alation Glossary Terms.

Args:
* query_params (GlossaryTermParams): REST API Get Filter Values.

Returns:
* list: Alation Glossary Terms

### post_glossary_terms

```
post_glossary_terms(glossary_terms: list) -> list[JobDetailsDocumentPost]
```

Post (Create) Alation Glossary Terms.


Args:
* glossary_terms (list): Alation Glossary Terms to be created.

Returns:
* List of JobDetails: Status report of the executed background jobs.

### put_glossary_terms

```
put_glossary_terms(glossary_terms: list) -> list[JobDetailsDocumentPut]
```

Put (Update) Alation Glossary Terms.

Args:
* glossary_terms (list): Alation Glossary Terms to be updated.

Returns:
* List of JobDetails: Status report of the executed background jobs.

### delete_glossary_terms

```
delete_glossary_terms(glossary_terms: list) -> JobDetailsTermDelete
```

Delete Alation Glossary Terms.

Args:
* glossary_terms (list): Alation Glossary Terms to be deleted.

Returns:
* Job details


## Examples

See `/examples/example_glossary_term.py`.


