---
title: Tags
parent: SDK Reference
---

# Tags
{:.no_toc}

* TOC
{:toc}

## Models

### Tag
Individual list item returned in the response of the functions `get_tags`, `get_a_tag`, `add_tag_to_object`, and `update_tag`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| id | int | Tag ID |
| name | str | Tag name |
| description | str | Tag description |
| number_of_objects_tagged | int | Number of objects that currently have the tag |
| ts_created | datetime | ISO-8601 formatted timestamp of when the tag was created |
| url | str | Relative Alation URL for the tag |

### TaggedObjectRef
Reference to an object that has a specific tag assigned.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| url | str | Relative Alation URL for the tagged object |
| otype | str | Object type of the tagged object |
| id | int or str | Object identifier |

### TaggedObject
Individual list item returned by `get_objects_tagged_with_specific_tag`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| ts_tagged | datetime | ISO-8601 formatted timestamp of when the tag was added to the object |
| object | TaggedObjectRef | Reference to the tagged object |

### TagObjectItem
Python object used to add a tag to an object and passed in the parameter `object` in the function `add_tag_to_object`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| oid | int or str | Object identifier |
| otype | str | Object type of the tagged object |

### TagItem
Python object used to update a tag and passed in the parameter `tag` in the function `update_tag`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| name | str | New tag name |
| description | str | New tag description |

### TagParams
Optional item used to filter the response returned by `get_tags`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| oid | int or str | Object identifier. Must be used together with `otype`. |
| otype | str | Object type. Must be used together with `oid`. |
| limit | int | Maximum number of records returned |
| skip | int | Number of records to skip |
| order_by | str | Sort order supported by the Tags API |

### TaggedObjectParams
Optional item used to filter the response returned by `get_objects_tagged_with_specific_tag`.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| limit | int | Maximum number of records returned |
| skip | int | Number of records to skip |
| order_by | str | Sort order. Supported values include `ts_tagged` and `-ts_tagged`. |
| exclude_deleted | bool | Exclude deleted objects from the response |

## Methods

### get_tags

```
get_tags(query_params: TagParams = None) -> list[Tag]
```

Get tags in the Alation catalog.

Args:
* query_params (TagParams): REST API GET filter values.

Returns:
* list[Tag]: Alation tags.

### get_a_tag

```
get_a_tag(tag_id: int) -> Tag
```

Get the details of a specific tag.

Args:
* tag_id (int): Tag ID.

Returns:
* Tag: Tag details.

### get_objects_tagged_with_specific_tag

```
get_objects_tagged_with_specific_tag(tag_name: str, query_params: TaggedObjectParams = None) -> list[TaggedObject]
```

Get all objects tagged with a specific tag.

Args:
* tag_name (str): Tag name. Special characters are URL encoded automatically.
* query_params (TaggedObjectParams): REST API GET filter values.

Returns:
* list[TaggedObject]: Tagged objects.

### add_tag_to_object

```
add_tag_to_object(tag_name: str, object: TagObjectItem) -> Tag
```

Add a tag to an object.

Args:
* tag_name (str): Tag name. If the tag does not yet exist, Alation creates it.
* object (TagObjectItem): Object to tag.

Returns:
* Tag: The created or reused tag.

### update_tag

```
update_tag(tag_id: int, tag: TagItem) -> Tag
```

Update a tag name or description.

Args:
* tag_id (int): Tag ID.
* tag (TagItem): Updated tag values.

Returns:
* Tag: Updated tag.

### remove_tag_from_object

```
remove_tag_from_object(tag_name: str, otype: str, oid: int | str) -> JobDetails
```

Remove a tag from an object.

Args:
* tag_name (str): Tag name. Special characters are URL encoded automatically.
* otype (str): Object type.
* oid (int | str): Object identifier.

Returns:
* JobDetails: Success or failure details for the delete request.

## Examples

See `/examples/example_tag.py`.
