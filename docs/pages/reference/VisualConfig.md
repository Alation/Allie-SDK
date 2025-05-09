---
title: VisualConfig
parent: SDK Reference
---

# Visual Config
{:.no_toc}

* TOC
{:toc}


## Known Shortcomings

We would like to highlight that currently the Visual Config API provided via the Alation platform has a few shortcomings:

- If you change the title of the visual config, the title gets suffixed with `custom field`. This bug is reported.
- It's not possible to update the document hub id with the `PUT` request.
- The document hub id is missing as a response of the `GET` request.


## Models

### VisualConfigBase

Sub-model used in the parent Models of `VisualConfig` and `VisualConfigItem`.

| field                    | type | description |
|--------------------------|------|---------- |
| id                       | integer | Unique ID of the visual config. |
| component_list_in_config | array | Containing `VisualConfigComponent` or `VisualGroupedComponents` |
| title                    | string | Title of the template for this visual config. |
| layout_otype             | string | Object type that the visual config is associated with. |

### VisualConfig

The main representation of a visual config.

Based on `VisualConfigBase`. Additional fields:

| field                    | type | description |
|--------------------------|------|---------- |
| id                       | integer | Unique ID of the visual config. |

### VisualConfigItem

The representation of a visual config for `POST` and `PUT` requests.

Based on `VisualConfigBase`. Additional fields:

| field                  | type | description                                  |
|------------------------|------|----------------------------------------------|
| collection_type_id                       | integer | Unique ID of the document hub. Option field. |

### VisualConfigComponent

Represents the visual configuration for a given field. 

| field               | type | description                                  |
|---------------------|------|----------------------------------------------|
| rendered_otype      | str  | Rendered object type for the visual config component |
| rendered_oid        | int  | The unique ID of the field to include in this component. If it's a custom field, this property is required. |
| page_defined_type   | str  | If the component_type is PAGE_DEFINED, this field is required and must be set to the page defined type. Otherwise, its value is null. |
| component_type |  str | Type of the component: BUILT_IN refers to a field that's defined and provided by Alation but whose value is editable. PAGE_DEFINED refers to a read-only field that's associated with a particular object type and whose value is derived from the object itself. USER_DEFINED refers to a custom field that's defined by catalog admins. |
| panel | str | Panel where the component is rendered. MAIN refers to the wide left panel, and SIDEBAR refers to the narrow right panel on a catalog page. |


### VisualGroupedComponent

Represents the grouping of visual components:

| field               | type | description                                  |
|---------------------|------|----------------------------------------------|
| label | str | Label for the group component. aka Group Name |
| open_by_default | bool | Indicates if a group component should be open by default. |
| panel | str | Panel where the component is rendered. MAIN refers to the wide left panel, and SIDEBAR refers to the narrow right panel on a catalog page. |
| is_group | bool | Specifies if the component is a group. It must always be set to true, as it is intended only for grouped components.
| components | list of `VisualConfigComponent` | | 

## Methods

### get_visual_configs

```
get_visual_configs(self, otype:str=None) -> list[VisualConfig]
```

Query multiple Alation Visual Configs and return their details.

Args:

- otype: Object Type (optional). Filter by object type.

Returns:

- `list[VisualConfig]`: List of Visual Configs

Raises:

- `requests.HTTPError`: If the API returns a non-success status code.

### get_a_visual_config

```
get_a_visual_config(self, visual_config_id:int) -> VisualConfig
```

Query one Alation Visual Config and return the details.

Args:

- visual_config_id: Alation Visual Config ID.

Returns:

- `VisualConfig`: an Alation Visual Config

Raises:

- `requests.HTTPError`: If the API returns a non-success status code.

### create_visual_config

```
create_visual_config(self, visual_config:VisualConfigItem) -> JobDetails
```

Create an Alation Visual Config.

Args:
    - `visual_config`: VisualConfigItem. This is the main payload.

Returns:
    `JobDetails`: an object of type JobDetails

Raises:
    `requests.HTTPError`: If the API returns a non-success status code.

### update_visual_config

```
update_visual_config(self, visual_config:VisualConfigItem, visual_config_id:int) -> JobDetails:
```

Update an Alation Visual Config.

Args:

- `visual_config`: VisualConfigItem. This is the main payload.
- `visual_config_id`: The id of the Visual Config to update.

Returns:

- `JobDetails`: an object of type JobDetails

Raises:

- `requests.HTTPError`: If the API returns a non-success status code.

### delete_visual_config
       
```
delete_visual_config(self, visual_config_id:int) -> JobDetails:
```

Delete an Alation Visual Config

Args:

- `visual_config_id`: Alation Visual Config ID.

Returns:

- `JobDetails`: an object of type JobDetails

Raises:

- `requests.HTTPError`: If the API returns a non-success status code.

## Examples

See `/examples/example_visual_config.py`.