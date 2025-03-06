---
title: Data Health
parent: SDK Reference
---

# Data Health
{:.no_toc}

* TOC
{:toc}

## Models

### DataQualityField

Individual list item returned in the response of the function `get_data_quality_fields`.

Attributes:

| Name          | Type      | Description                                                                                  |
|---------------|-----------|----------------------------------------------------------------------------------------------|
| key           | str       | The unique key that was assigned to the rule on ingestion.                                   |
| name          | str       | The human-readable label for the rule.                                                       |
| description   | str       | The assigned description of the given rule.                                                  |
| type          | str       | The data type of values associated with rule. Values are `NUMERIC`, `STRING`, or `BOOLEAN`.  |
| ts_created    | datetime  | The ISO 8601 formatted date of when the rule was created.                                    |

###  DataQualityFieldItem
Python object used to create a DataQualityRule in Alation and passed with multiple objects in the list parameter `dq_fields` in the function `post_data_quality_fields`.

Attributes:

| Name          | Required  | Type  | Description                                                                                          |
|---------------|:---------:|-------|------------------------------------------------------------------------------------------------------|
| field_key     |   TRUE    | str   | The unique key for the rule being set up in Alation.                                                 |
| name          |   TRUE    | str   | The human-readable label for the rule.                                                               |
| type          |   TRUE    | str   | The data type of values associated with rule. Allowed values are `NUMERIC`, `STRING`, or `BOOLEAN`.  |
| description   |   FALSE   | str   | Allows for decoration of the rule to fully describe the context of the rule .                        |

###  DataQualityFieldParams
Optional item used to filter the response of the returned data from the function `get_data_quality_fields`.

Attributes:

| Name | Type | Description                                                   |
|------|------|---------------------------------------------------------------|
| key  | set  | The unique key(s) that was assigned to the rule on ingestion. |

###  DataQualityValue
Individual list item returned in the response of the function `get_data_quality_values`.

Attributes:

| Name                  | Type      | Description                                                                                                                |
|-----------------------|-----------|----------------------------------------------------------------------------------------------------------------------------|
| object_key            | str       | The applied object's api_key. It is used to uniquely identify an object in Alation.                                        |
| object_name           | str       | The applied object's name.                                                                                                 |
| otype                 | str       | The applied object's object type. An otype is used in conjunction with its oid to uniquely identify an object in Alation.  |
| oid                   | int       | The applied object's id. An oid is used in conjunction with its otype is used to uniquely identify an object in Alation.   |
| source_object_key     | str       | The original object's api_key that the rule was applied on.                                                                |
| source_object_name    | str       | The original object's name.                                                                                                |
| source_otype          | str       | The original object's otype that the rule was applied on.                                                                  |
| source_oid            | int       | The original object's oid that the rule was applied on.                                                                    |
| value_id              | int       | The applied value's id.                                                                                                    |
| value_value           | any       | The applied value's value.                                                                                                 |
| value_quality         | str       | The applied value's quality.                                                                                               |
| value_last_updated    | datetime  | The value's last updated timestamp in ISO-8601 format.                                                                     |
| value_external_url    | str       | The applied value external url.                                                                                            |
| field_key             | str       | The applied field's key.                                                                                                   |
| field_name            | str       | The applied field's name.                                                                                                  |
| field_description     | str       | The applied field's description.                                                                                           |

###  DataQualityValueItem
Python object used to create a DataQualityValue in Alation and passed with multiple objects in the list parameter `dq_values` in the function `post_data_quality_values`.

Attributes:

| Name          | Required  | Type  | Description                                                                                                             |
|---------------|:---------:|-------|-------------------------------------------------------------------------------------------------------------------------|
| field_key     |   TRUE    | str   | Unique key for a rule that has been set up in Alation. The field must already exist or in the fields array to be valid. |
| object_key    |   TRUE    | str   | The api key descriptor for a catalog object.                                                                            |
| object_type   |   TRUE    | str   | Required descriptor with values of `ATTRIBUTE`, `TABLE`, `SCHEMA` that act as a hint for api key resolution.            |
| status        |   TRUE    | str   | The status of the object on application of the rule. Allowed values are `GOOD`, `WARNING`, or `ALERT`.                  |
| value         |   TRUE    | any   | The value associated with the execution of a rule on target object.                                                     |
| url           |   FALSE   | str   | External or relative URL that allows pointing to specific site for further information about rule.                      |
| last_updated  |   FALSE   | str   | ISO 8601 formatted date time string indicating when the value was last updated.                                         |

###  DataQualityValueParams
Optional item used to filter the response of the returned data from the function `get_data_quality_values`.

Attributes:

| Name              | Type  | Description                                                                           |
|-------------------|-------|---------------------------------------------------------------------------------------|
| object_key        | set   | Filter values on those applied indirectly by the related object's api_keys.           |
| source_object_key | set   | Filter values on those applied directly to a source object's api_key.                 |
| field_key         | set   | The unique key that was assigned to the rule on ingestion.                            |
| value_quality     | set   | Filter values by their quality.                                                       |
| hide_related      | bool  | Setting this to true will hide values that have been propagated to related objects.   |

## Methods
###  get_data_quality_fields

```
get_data_quality_fields(query_params: DataQualityFieldParams = None) -> list
```

Query multiple Alation data quality fields.

Args:
* query_params (DataQualityFieldParams): REST API Get Filter Values

Returns:
* list: Alation data quality fields with each item represented as a `DataQualityField` object

###  get_data_quality_values

```
get_data_quality_values(query_params: DataQualityValueParams = None) -> list[DataQualityValue]
```

Query multiple Alation data quality values.

Args:
* query_params (DataQualityValueParams): REST API Get Filter Values

Returns:
* list: Alation data quality values with each item represented as a `DataQualityValue` object

###  post_data_quality_fields

```
post_data_quality_fields(dq_fields: list) -> list[JobDetailsDataQuality]
```

Post (Create) Alation data quality fields.

Args:
* dq_fields (list): Alation data quality fields to be created. Each item in the list must be a `DataQualityFieldItem` object

Returns:
* list of job details

###  delete_data_quality_fields

```
delete_data_quality_fields(dq_fields: list) -> list[JobDetailsDataQuality]:
```

Delete Alation data quality fields.

Args:
* dq_fields (list): Alation data quality fields to be deleted. Each item in the list must be a `DataQualityField` object

Returns:
* list of job details

###  post_data_quality_values

```
post_data_quality_values(dq_values: list) -> list[JobDetailsDataQuality]
```

Post (Create) Alation data quality values.

Args:
* dq_values (list): Alation data quality values to be created. Each item in the list must be a `DataQualityValueItem` object

Returns:
* bool: list of job details

###  delete_data_quality_values

```
delete_data_quality_values(dq_values: list) -> list[JobDetailsDataQuality]
```

Delete Alation data quality values.

Args:
* dq_values (list): Alation data quality values to be deleted. Each item in the list must be a `DataQualityValue` object
  
Returns:
* bool: list of job details

## Examples

See `/examples/example_data_quality.py`.