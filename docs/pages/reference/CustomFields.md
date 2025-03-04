---
title: Custom Fields
parent: SDK Reference
---

# Custom Fields
{:.no_toc}

* TOC
{:toc}

## Models

### CustomField
Individual list item returned in the response of the function `get_custom_fields` that represents a custom field in Alation.

Attributes:

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| id          | int                   | The API ID of the custom field in Alation                                                      |
| allow_multiple   | bool                   | Filter to allow the API to return more than one custom field. Only used when field_type is `OBJECT_SET``. |
| allowed_otypes | list                   | Indicates what object types are allowed as values for this field.                  |
| backref_name | str                   | The text shown as the title for a Custom Field Backreference on an Object Set, People Set, or Reference Field. |
| backref_tooltip_text | str         | The tooltip text shown when hovering over the title of a Custom Field Backreference on an Object Set, People Set, or Reference Field. |
| builtin_name | str         | A special, read-only string value used to uniquely identify built-in Custom Fields provided by Alation. |
| field_type | str         | The type of Custom Field |
| name_plural | str         | The plural name for the Custom Field |
| name_singular | str         | The singular name for the Custom Field |
| options | list         | Required and used only when the field_type is `PICKER` or `MULTI_PICKER`. Provides a list of string values for the available options that can be selected with these fields. |
| tooltip_text | str         | The tooltip text shown when hovering over the title of a Custom Field |

### CustomFieldItem
Python object used to create a `CustomField` in Alation and passed in the parameter `custom_fields` as a list in the function `post_custom_fields`.

Attributes:

| Name         | Required | Type                  | Description                                                  |
|--------------|:--------:|-----------------------|--------------------------------------------------------------|
| allow_multiple        |  FALSE    | bool         | Used only when `field_type` is `OBJECT_SET` (Object Set, People Set, or Reference Field). `false` means the Field is a Reference Field, while `true` means the Field is either Object Set or People Set. Defaults to `false` if not specified.                                     |
| allowed_otypes  |  FALSE   | list                   | Required and used only when `field_type` is `OBJECT_SET` (Object Set, People Set, or Reference Field). Indicates what object types are allowed as values for this field.                              |
| backref_name  |  FALSE   | str                   | The text shown as the title for a Custom Field Backreference on an Object Set, People Set, or Reference Field. Required when `field_type` is set to `OBJECT_SET`. | 
| backref_tooltip_text  |  FALSE   | str              | The tooltip text shown when hovering over the title of a Custom Field Backreference on an Object Set, People Set, or Reference Field. | 
| field_type  |  FALSE   | str              | The type of Custom Field, one of `DATE`, `MULTI_PICKER`, `OBJECT_SET`, `PICKER`, or `RICH_TEXT` | 
| name_plural  |  FALSE   | str              | The plural name for the Custom Field. Required when `field_type` is set to `MULTI_PICKER`, or when `field_type` is set to `OBJECT_SET` and `allow_multiple` is set to `true` (Object Set and People Set Fields only; Reference Fields do not use this). | 
| name_singular  |  FALSE   | str              | The singular name for the Custom Field. Always required. |
| options  |  FALSE   | list              | Required and used only when the `field_type` is `PICKER` or `MULTI_PICKER`. Provides a list of string values for the available options that can be selected with these fields.
|
| tooltip_text  |  FALSE   | str              | The tooltip text shown when hovering over the title of a Custom Field.|

### CustomFieldParams
Optional item used to filter the response of the returned data from the function `get_custom_fields`.

Attributes:

| Name  | Type  | Description                                                                                                                |
|-------|-------|----------------------------------------------------------------------------------------------------------------------------|
| id   | set   | Filter by Custom Field ID   |
| allow_multiple | bool   | Filter by allow_multiple. Only used when `field_type` is `OBJECT_SET`.|
| field_type | set   | The field type to filter by |
| name_plural | set   | Filter by an exact match on name_plural. |
| name_plural__contains | set   | Filter by a case-sensitive substring on name_plural. |
| name_plural__icontains | set   | Filter by a case-insensitive substring on name_plural. |
| tooltip_text | set   | Filter by an exact match on tooltip_text. |
| name_singular | set   | Filter by an exact match on name_singular. |
| name_singular__contains | set   | Filter by a case-sensitive substring on name_singular. |
| name_singular__icontains | set   | Filter by a case-insensitive substring on name_singular. |
| tooltip_text | set   | Filter by an exact match on tooltip_text. |
| tooltip_text__contains | set   | Filter by a case-sensitive substring on tooltip_text. |
| tooltip_text__icontains | set   | Filter by a case-insensitive substring on tooltip_text. |

### CustomFieldStringValue

Python object used in the Models `BaseCustomFieldValue`: A single string values for custom fields that we receive as part of the response/returned payload gets mapped to this data class.

Attributes:

| Name         | Required | Type                  | Description                                                  |
|--------------|:--------:|-----------------------|--------------------------------------------------------------|
| value  |  FALSE   | str                   | A string value | 


### CustomFieldStringValueItem

Inherits from `CustomFieldStringValue`.

Python object used to return a string value in the Models `CustomFieldValueItem`.

### CustomFieldDictValue

Python object used to return a dictionary value in the Models `BaseCustomFieldValue`.

Attributes:

| Name  | Required | Type                  | Description                                                  |
|-------|:--------:|-----------------------|--------------------------------------------------------------|
| otype |  FALSE   | str                   | The Alation otype of the object | 
| oid   |  FALSE   | int                   | The Alation oid of the object | 

### CustomFieldDictValueItem

Inherits from `CustomFieldDictValue`.

Python object used to return a dictionary in the Models `CustomFieldValueItem`.

### BaseCustomFieldValue
Sub-model used in the parent Model of `CustomFieldValue`.

Attributes:

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| field_id          | int                   | The id of the specified Custom Field as an integer.                                                      |
| ts_updated   | datetime                   | ISO-8601 formatted timestamp of when the value was last updated.|
| otype | str                   | The type of the object.|  
| oid | int                   | The id of the object.|
| value | str                   | Contents of Field Values. Data structure depends on the type of field.                |

### CustomFieldValue
Individual list item returned in the response of the function `get_custom_field_values`

Attributes:


| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| field_name          | str                   | The name of the field                                                     |

### CustomFieldValueParams
Optional item used to filter the response of the returned data from the function `get_custom_field_values`.

Attributes:

| Name  | Type  | Description                                                                                                                |
|-------|-------|----------------------------------------------------------------------------------------------------------------------------|
| oid   | set   | The object id of the specified object with a Custom Field Value   |
| otype   | set   | The object type(s) with the Custom Field Value as a string   |
| field_id   | set   | The id of the specified Custom Field   |

## Methods

### get_custom_fields

```
get_custom_fields(query_params: CustomFieldParams = None) -> list:
```

Get the details of all Alation Custom Fields.

Args:
* query_params (`CustomFieldParams`): REST API Get Filter Values.

Returns:
* list: list of Alation Custom Fields

### get_custom_field_values

```
get_custom_field_values(query_params: CustomFieldValueParams = None) -> list:
```

Get the details of all Alation Custom Field Values.


Args:
* query_params (`CustomFieldValueParams`): REST  API Get Filter Values.

Returns:
* list: list of Alation Custom Field Values.

### get_a_builtin_custom_field

```
get_a_builtin_custom_field(field_name: str) -> CustomField:
```

Get the details of a Builtin Alation Custom Field.

Args:
* field_name (str): Name of the Builtin Custom Field. Possible values: title, description, business_glossary_status, steward.

Returns:
* `CustomField`: Alation Custom Field.

### get_a_custom_field

```
get_a_custom_field(field_id: int) -> CustomField:
```

Get the details of an Alation Custom Field.

Args:
* field_id (int): ID of the Alation Custom Field.

Returns:
* `CustomField`: Alation Custom Field.

### post_custom_fields

```
post_custom_fields(custom_fields: list) -> list[JobDetailsCustomFieldPost]:
```

Post (Create) Alation Custom Fields.

Args:
* custom_fields (list): Alation Custom Fields to be created.

Returns:
* list of job details

### put_custom_field_values

```
put_custom_field_values(custom_field_values: list, batch_size: int = 10000) -> list[JobDetails]:
```

Put (Update) Alation Custom Field Values.

Args:
* custom_field_values (list): Alation Custom Field Values to be updated.
* batch_size (int): REST API PUT Body Size Limit.

Returns:
* list of job details

## Examples

See `/examples/example_custom_field.py`.



