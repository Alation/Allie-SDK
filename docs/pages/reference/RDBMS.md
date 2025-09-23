---
title: RDBMS
parent: SDK Reference
---

# RDBMS
{:.no_toc}

* TOC
{:toc}

## Models

### BaseRDBMS
Sub-model used in the parent Models of `Schema`, `Table`, and `Column`.

Attributes:

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| id          | int                   | ID of the RDBMS object |
| title    | str                   | Title of the RDBMS object |
| description    | str                   | Description of the RDBMS object|   
| name | str                   | Name of the RDBMS object|
| ds_id | int                   | Data source ID for the RDBMS object |
| key | str                   | Period delimited, Fully Qualified Name of the RDBMS object |
| url | str                   | Relative url of the object in alation. |
| custom_fields | list                   | A list of `CustomFieldValueItem` objects containing custom field information relative to the RDBMS object |

### BaseRDBMSItem
Sub-model used in the parent Models of `SchemaItem`, `TableItem`, and `ColumnItem`. These python objects are used to create RDBMS objects in Alation.

Attributes:

| Name         | Required | Type                  | Description                                                  |
|--------------|:--------:|-----------------------|--------------------------------------------------------------|
| title  |  FALSE    | str         | The title of the RDBMS object | 
| description |  FALSE     | str                   | Description of the RDBMS object| 
| key |  TRUE  | str                   | Period delimited, Fully Qualified Name of the RDBMS object |
| custom_fields |  FALSE  | list                   | A list of `CustomFieldValueItem` objects containing custom field information relative to the RDBMS object |

### BaseRDBMSParams
Sub-model used in the parent Models of `SchemaParams`, `TableParams`, and `ColumnParams`. These optional Model items used to filter the response of the returned data from the get functions.

Attributes:

| Name  | Type  | Description                                                                                                                |
|-------|-------|----------------------------------------------------------------------------------------------------------------------------|
| id   | set   | filter by id of the object  |
| name | set   | filter by object name |
| ds_id | set   | Unique identifier of the data source |
| id__gt | set   | filter by id greater than a value |
| id__gte | set   | filter by id greater than or equal to a value |
| id__lt | set   | filter by id lesser than a value |
| id__lte | set   | filter by id lesser than or equal to a value |
| name__contains | set   | filter by object name containing the given string |
| name__startswith | set   | filter by object name starting with the given string |
| name__endswith | set   | filter by object name ending with the given string |
| ds_id__gt | set   | filter by data source id greater than a value |
| ds_id__gte | set   | filter by data source id greater than or equal to a value |
| ds_id__lt | set   | filter by data source id lesser than a value |
| ds_id__lte | set   | filter by data source id lesser than or equal to a value |

### Schema
Individual list item returned in the response of the function `get_schemas` that represents a schema in Alation.

Attributes:

| Name         | Type                  | Description                                                  |
|--------------|-----------------------|--------------------------------------------------------------|
| db_comment   | str         | Comments on the schema from the data source. Defaults to empty text if not passed in the request. | 


### SchemaItem
Python object used to create a `Schema` in Alation and passed in the parameter `schemas` as a list in the function `post_schemas`.

Attributes:

| Name         | Type                  | Description                                                  |
|--------------|-----------------------|--------------------------------------------------------------|
| db_comment   | str         | Comments on the schema from the data source. Defaults to empty text if not passed in the request. |

### SchemaPatchItem
Python object used to update an existing `Schema` in Alation and passed in the parameter `schemas` as a list in the function `patch_schemas`.

Attributes:

| Name         | Required | Type | Description |
|--------------|:--------:|------|-------------|
| id           | TRUE     | int  | Identifier of the schema to be updated. |
| title        | FALSE    | str  | The title of the schema. |
| description  | FALSE    | str  | Description of the schema. |
| db_comment   | FALSE    | str  | Comments on the schema from the data source. |
| custom_fields | FALSE   | list | A list of `CustomFieldValueItem` objects containing custom field information relative to the schema. |

### SchemaParams
Optional item used to filter the response of the returned data from the function `get_schemas`.

Attributes:

Inherits attributes from `BaseRDBMSParams`

### Table
Individual list item returned in the response of the function `get_tables` that represents a table in Alation.

Attributes:

| Name         | Type                  | Description                                                  |
|--------------|-----------------------|--------------------------------------------------------------|
| table_type   | str         | The type of the table. Value can be `TABLE`, `VIEW` or `SYNONYM`. Defaults to `TABLE`. | 
| schema_id  | int         | Id of the schema object associated with the table | 
| schema_name  | str         | Name of the schema object associated with the table | 
| sql  | str         | Data definition language (SQL query) associated with table or view. | 
| table_comment  | str         | Comments/information on the table from the source database. | 

### TableItem
Python object used to create a `Table` in Alation and passed in the parameter `tables` as a list in the function `post_tables`.

Attributes:

| Name         | Required | Type                  | Description                                                  |
|--------------|:--------:|-----------------------|--------------------------------------------------------------|
| table_comment |  FALSE    | str         | Comments/information on the table from the source database. Defaults to empty text if not passed in the request. |
| table_type |  FALSE    | str         | The type of the table. Value can be `TABLE`, `VIEW` or `SYNONYM`. Defaults to `TABLE`. |  
| table_type_name |  FALSE    | str         | The datasource specific name. |  
| owner |  FALSE    | str         | Name of the database account that owns this table. | 
| sql |  FALSE    | str         | Data definition language (SQL query) associated with table or view. | 
| base_table_key |  FALSE    | str         | The API key for referencing the base table when the table type is a `SYNONYM`. Note: Make sure the base_table_key is a valid and exists in the catalog. |
| partition_definition |  FALSE    | str         | The name/information of the partition from the source database.|
| partition_columns |  FALSE    | list         | List of partition columns. |

### TablePatchItem
Python object used to update an existing `Table` in Alation and passed in the parameter `tables` as a list in the function `patch_tables`.

Attributes:

| Name         | Required | Type                  | Description                                                  |
|--------------|:--------:|-----------------------|--------------------------------------------------------------|
| id |  TRUE    | int         | Identifier of the catalog table to update. |
| title |  FALSE    | str         | Updated title of the table. |
| description |  FALSE    | str         | Updated description of the table. |
| table_comment |  FALSE    | str         | Comments/information on the table from the source database. |
| table_type |  FALSE    | str         | Updated type of the table. Value can be `TABLE`, `VIEW` or `SYNONYM`. |
| table_type_name |  FALSE    | str         | Updated datasource specific name. |
| owner |  FALSE    | str         | Updated owner of the table. |
| sql |  FALSE    | str         | Updated DDL (SQL query) associated with the table or view. |
| base_table_key |  FALSE    | str         | Updated API key for referencing the base table when the table type is a `SYNONYM`. |
| partition_definition |  FALSE    | str         | Updated partition information from the source database. |
| partition_columns |  FALSE    | list         | Updated list of partition columns. |
| custom_fields |  FALSE    | list         | A list of `CustomFieldValueItem` objects containing updated custom field information. |

### TableParams
Optional Model item used to filter the response of the returned data from the get function `get_tables`.

Attributes:

| Name  | Type  | Description                                                                                                                |
|-------|-------|----------------------------------------------------------------------------------------------------------------------------|
| schema_id   | set   | filter by schema id  |
| schema_name | set   | filter by schema name |
| name__iexact | set   | filter by object name case insensitive exact match |
| name__icontains | set   | filter by object name containing the given string, case insensitive match|
| name__istartswith | set   | filter by object name starting with the given string, case insensitive match |
| name__iendswith | set   | filter by object name ending with the given string, case insensitive match |
| schema_id__gt | set   | filter by schema id greater than a value |
| schema_id__gte | set   | filter by schema id greater than or equal to a value |
| schema_id__lt | set   | filter by schema id lesser than a value |
| schema_id__lte | set   | filter by schema id lesser than or equal to a value |
| schema_name__iexact | set   | filter by schema name case insensitive exact match |
| schema_name__contains | set   | filter by schema name containing the given string |
| schema_name__icontains | set   | filter by schema name containing the given string, case insensitive match |
| schema_name__startswith | set   | filter by schema name starting with the given string |
| schema_name__istartswith | set   | filter by schema name starting with the given string, case insensitive match |
| schema_name__endswith | set   | filter by schema name ending with the given string |
| schema_name__iendswith | set   | filter by schema name ending with the given string, case insensitive match |

### ColumnIndex
Model of the index that the column is associated with.

Attributes:

| Name         | Type                  | Description                                                  |
|--------------|-----------------------|--------------------------------------------------------------|
| isPrimaryKey   | bool         | If the column is a primary key then `true` else `false`. | 
| isForeignKey  | bool         | If the column is part of a foreign key then `true` else `false`. Associated column in the `referencedColumnId` field. | 
| referencedColumnId  | str         | API key of the column being referenced from the datasource. | 
| isOtherIndex  | bool         | If the column is a part of any other index it is `true` else `false`. Associated column in the referencedColumnId field. | 

### Column
Individual list item returned in the response of the function `get_columns` that represents a column in Alation.

Attributes:

| Name         | Type                  | Description                                                  |
|--------------|-----------------------|--------------------------------------------------------------|
| column_type   | str         | The string describing the type of the column | 
| index  | ColumnIndex         | Define the index that the column is associated with, it is of type `ColumnIndex` | 
| nullable  | bool         | Field to indicate if the column can contain null values. | 
| schema_id  | int         | filter by schema id | 
| table_id  | str         | filter by table id | 
| table_name  | str         | filter by table name | 
| position  | int         | Position of the column in the table. | 

### ColumnItem
Python object used to create a `Column` in Alation and passed in the parameter `columns` as a list in the function `post_columns`.

Attributes:

    index: ColumnIndex = field(default=None)

| Name         | Required | Type                  | Description                                                  |
|--------------|:--------:|-----------------------|--------------------------------------------------------------|
| column_type |  TRUE    | str         | The string describing the type of the column. eg. int, varchar(100) |
| column_comment |  FALSE    | str         | A comment field that stores a description of the column which is ingested from the source system. |  
| nullable |  FALSE    | bool         | Field to indicate if the column can contain null values.  |  
| position |  FALSE    | str         | Position of the column in the table. Defaults to 0 if not passed in the request. | 
| index |  FALSE    | ColumnIndex         | Define the index that the column is associated with. It is of type ColumnIndex | 

### ColumnParams
Optional Model item used to filter the response of the returned data from the get function `get_columns`.


Attributes:

    table_name__endswith: set = field(default_factory=set)

| Name  | Type  | Description                                                                                                                |
|-------|-------|----------------------------------------------------------------------------------------------------------------------------|
| name__iexact | set   | filter by object name case insensitive exact match |
| name__icontains | set   | filter by object name containing the given string, case insensitive match|
| name__istartswith | set   | filter by object name starting with the given string, case insensitive match |
| name__iendswith | set   | filter by object name ending with the given string, case insensitive match |
| table_id   | set   | filter by table id  |
| table_name   | set   | filter by table name  |
| table_id__gt | set   | filter by table id greater than a value |
| table_id__gte | set   | filter by table id greater than or equal to a value |
| table_id__lt | set   | filter by table id lesser than a value |
| table_id__lte | set   | filter by table id lesser than or equal to a value |
| table_name__iexact | set   | filter by table name case insensitive exact match |
| table_name__icontains | set   | filter by table name containing the given string, case insensitive match|
| table_name__istartswith | set   | filter by table name starting with the given string, case insensitive match |
| table_name__iendswith | set   | filter by table name ending with the given string, case insensitive match |
| table_name__contains | set   | filter by table name containing the given string |
| table_name__startswith | set   | filter by table name starting with the given string |
| table_name__endswith | set   | filter by table name ending with the given string |
| schema_id   | set   | filter by schema id  |
| schema_id__gt | set   | filter by schema id greater than a value |
| schema_id__gte | set   | filter by schema id greater than or equal to a value |
| schema_id__lt | set   | filter by schema id lesser than a value |
| schema_id__lte | set   | filter by schema id lesser than or equal to a value |

## Methods

### get_schemas

```
get_schemas(query_params: SchemaParams = None) -> list[Schema]
```

Query multiple Alation RDBMS Schemas.

Args:
* query_params (SchemaParams): REST API Get Filter Values.

Returns:
* list: Alation RDBMS Schemas.

### post_schemas

```
post_schemas(ds_id: int, schemas: list) -> list[JobDetailsRdbms]
```

Post (Create or Update) Alation Schema Objects.


Args:
* ds_id (int): ID of the Alation Schemas' Parent Datasource.
* schemas (list): Alation Schemas to be created or updated.

Returns:
* list of job details

### patch_schemas

```python
patch_schemas(ds_id: int, schemas: list[SchemaPatchItem]) -> list[allie_sdk.models.job_model.JobDetailsRdbms]
```

Patch (Update) Alation Schema Objects.

Args:
   - `ds_id` (int): ID of the Alation Schemas' Parent Datasource.
   - `schemas` (list[SchemaPatchItem]): Alation Schemas to be updated.

Returns:
   - `list[JobDetailsRdbms]`: result of the job

Raises:
   - `requests.HTTPError`: If the API returns a non-success status code.

### get_tables

```
get_tables(query_params: TableParams = None) -> list[Table]
```

Query multiple Alation RDBMS Tables.

Args:
* query_params (TableParams): REST API Get Filter Values.

Returns:
* list: Alation RDBMS Tables.

### post_tables

```
post_tables(ds_id: int, tables: list) -> list[JobDetailsRdbms]
```

Post (Create or Update) Alation Table Objects.


Args:
* ds_id (int): ID of the Alation Tables' Parent Datasource.
* tables (list): Alation Tables to be created or updated.

Returns:
* list of job details

### patch_tables

```python
patch_tables(ds_id: int, tables: list[TablePatchItem]) -> list[allie_sdk.models.job_model.JobDetailsRdbms]
```

Patch (Update) Alation Table Objects.

Args:
   - `ds_id` (int): ID of the Alation Tables' Parent Datasource.
   - `tables` (list[TablePatchItem]): Alation Tables to be updated.

Returns:
   - `list[JobDetailsRdbms]`: result of the job

Raises:
   - `requests.HTTPError`: If the API returns a non-success status code.

### get_columns

```
get_columns(query_params: ColumnParams = None) -> list[Column]
```

Query multiple Alation RDBMS Columns.

Args:
* query_params (ColumnParams): REST API Get Filter Values.

Returns:
* list: Alation RDBMS Columns.

### post_columns

```
post_columns(ds_id: int, columns: list) -> list[JobDetailsRdbms]
```

Post (Create or Update) Alation Column Objects.


Args:
* ds_id (int): ID of the Alation Columns' Parent Datasource.
* columns (list): Alation Columns to be created or updated.

Returns:
* list of job details

### patch_columns

```python
patch_columns(ds_id: int, columns: list[ColumnPatchItem]) -> list[allie_sdk.models.job_model.JobDetailsRdbms]
```

Patch (Update) Alation Column Objects.

Args:
   - `ds_id` (int): ID of the Alation Columns' Parent Datasource.
   - `columns` (list): Alation Columns to be updated.

Returns:
   - `list[JobDetailsRdbms]`: result of the job

Raises:
   - `requests.HTTPError`: If the API returns a non-success status code.

## Examples

See `/examples/example_rdbms.py`.



