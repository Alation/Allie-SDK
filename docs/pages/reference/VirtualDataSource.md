---
title: Virtual Data Source
parent: SDK Reference
---

# Virtual Data Source
{:.no_toc}

* TOC
{:toc}

## Models

### VirtualDataSourceItem
Sub-model used in the parent Models of `Schema`, `Table`, `Column' and 'Index`.

Attributes:

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| key          | str                   | Key of the Virtual Data Source object |
| description    | str                   | Description of the Virtual Data Source object|   
| title    | str                   | Title of the Virtual Data Source object |

### VirtualDataSourceParams
These optional Model items can be used to update title and descriptions or remove VDS objects.

Attributes:

| Name  | Type  | Description                                                                                                                |
|-------|-------|----------------------------------------------------------------------------------------------------------------------------|
| set_title_descs   | boolean   | This parameter specifies if the title and description of the object passed should be updated. When set to true, will add a title and description to the specified object, if the object is being newly added to a database's metadata. If the object already exists, they will be updated  |
| remove_not_seen | boolean   | This parameter specifies if the technical metadata of a data source should be deleted. |

### VirtualDataSourceSchema
Python object used to create a `Schema` in Alation virtual data source and passed in the parameter `vds_objects` in the function `post_metadata`.

Attributes:
Key, description, title are inherited from VirtualDataSourceItem. The key is required.

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| key          | str                   | Key of the Virtual Data Source object |
| description    | str                   | Description of the Virtual Data Source object|   
| title    | str                   | Title of the Virtual Data Source object |


### VirtualDataSourceTable
Python object used to create a `Table` in Alation and passed in the parameter `vds_objects` as a list in the function `post_metadata`.

Attributes:
Key, description, title are inherited from VirtualDataSourceItem. The key is required

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| key          | str                   | Key of the Virtual Data Source object |
| description    | str                   | Description of the Virtual Data Source object|   
| title    | str                   | Title of the Virtual Data Source object |
| data_location          | str                   | A URI or file path to the location of the underlying data, such as an HDFS URL for a Hive table. |
| db_owner    | str                   | Name of the database account that owns this table.|   
| definition_sql    | str                   | CREATE TABLE statement which was used to create the table. |
| constraint_text          | str                   | Constraint statements which are enforced by the DB. |
| ts_created    | str                   | Timestamp at which the table or view was created. Example: 2018-03-13T22:09:33Z|   
| ts_last_altered    | str                   | Timestamp of the last ALTER statement executed against this table. Example: 2018-03-13T22:09:33Z |
| partitioning_attributes    | str                   | An array of columns which are used to partition the table. Example: ["column1", "column2"]|   
| bucket_attributes    | str                   | An array of columns which are used to bucket the table (in data sources like Hive, bucketing is an alternative mechanism to partitioning for grouping similar data together: LanguageManualDDL-BucketedTables). Example: ["column1", "column2"] |
| sort_attributes          | str                   | An array of columns used to sort the table (in Hive, used with bucketing to store data for faster computation: LanguageManualDDL-BucketedSortedTables). Example: ["column1", "column2"]. |
| synonyms    | str                   | An array of other names that can be used to refer to this table. Each synonym is represented as a JSON comprising schema_name and table_name. Example: [{"schema_name": "schema_a","table_name": "table_a"}, {"schema_name": "schema_b","table_name": "table_b"}]. |   
| skews_info    | str                   | A JSON of the skew column names to an array of their respective skewed column values that appear very often. Example:{"column1": ["column1_value1", "column1_value2"], "column2": ["column2_value1", "column2_value2"]}. |
| table_comment    | str                   | A comment field that stores a description of the table which is ingested from the source system. Example: "This Table is created by ELT". |

### VirtualDataSourceView
Python object used to create a `View` in Alation and passed in the parameter `vds_objects` as a list in the function `post_metadata`.

Attributes:
Key, description, title are inherited from VirtualDataSourceItem. The key is required

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| key          | str                   | Key of the Virtual Data Source object |
| description    | str                   | Description of the Virtual Data Source object|   
| title    | str                   | Title of the Virtual Data Source object |
| data_location          | str                   | A URI or file path to the location of the underlying data, such as an HDFS URL for a Hive table. |
| db_owner    | str                   | Name of the database account that owns this table.|   
| view_sql    | str                   | CREATE VIEW statement which was used to create the view. |
| view_sql_expanded          | str                   | CREATE VIEW statement with fully qualified object references. |
| ts_created    | str                   | Timestamp at which the table or view was created. Example: 2018-03-13T22:09:33Z|   
| ts_last_altered    | str                   | Timestamp of the last ALTER statement executed against this table. Example: 2018-03-13T22:09:33Z |
| partitioning_attributes    | str                   | An array of columns which are used to partition the table. Example: ["column1", "column2"]|   
| bucket_attributes    | str                   | An array of columns which are used to bucket the table (in data sources like Hive, bucketing is an alternative mechanism to partitioning for grouping similar data together: LanguageManualDDL-BucketedTables). Example: ["column1", "column2"] |
| sort_attributes          | str                   | An array of columns used to sort the table (in Hive, used with bucketing to store data for faster computation: LanguageManualDDL-BucketedSortedTables). Example: ["column1", "column2"]. |
| synonyms    | str                   | An array of other names that can be used to refer to this table. Each synonym is represented as a JSON comprising schema_name and table_name. Example: [{"schema_name": "schema_a","table_name": "table_a"}, {"schema_name": "schema_b","table_name": "table_b"}]. |   
| skews_info    | str                   | A JSON of the skew column names to an array of their respective skewed column values that appear very often. Example:{"column1": ["column1_value1", "column1_value2"], "column2": ["column2_value1", "column2_value2"]}. |
| table_comment    | str                   | A comment field that stores a description of the table which is ingested from the source system. Example: "This Table is created by ELT". |

### VirtualDataSourceColumn
Python object used to create a `Column` in Alation and passed in the parameter `vds_objects` as a list in the function `post_metadata`.

Attributes:
Key, description, title are inherited from VirtualDataSourceItem. The key is required

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| key          | str                   | Key of the Virtual Data Source object |
| description    | str                   | Description of the Virtual Data Source object|   
| title    | str                   | Title of the Virtual Data Source object |
| column_type          | str                   | The type of the column. The value for this parameter can be any of the column types supported by the underlying database.. |
| position    | str                   | Position of the column in the table which contains it. NOTE: 1) This value needs to be a positive integer. 2) When specifying a column, please make sure the table it corresponds to is already a part of the database's metadata..|   
| column_comment    | str                   | A comment field that stores a description of the column which is ingested from the source system. |
| nullable          | str                   | Field to indicate if the column can be nullable. Set this to true if the column is a nullable field, false otherwise. |

### VirtualDataSourceIndex
Python object used to create a `Index` in Alation and passed in the parameter `vds_objects` as a list in the function `post_metadata`.

Attributes:
Key, description, title are inherited from VirtualDataSourceItem. The key, index_type and column_names are required

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| key          | str                   | Key of the Virtual Data Source object |
| description    | str                   | Description of the Virtual Data Source object|   
| title    | str                   | Title of the Virtual Data Source object |
| index_type          | str                   | The type of the index. The value for this field can be one among: ‘PRIMARY’, ‘SECONDARY’, ‘PARTITIONED_PRIMARY’, ‘UNIQUE’, ‘OTHER’. Example: "PRIMARY" The presence of this field distinguishes index object from a column. NOTE: 1) When specifying an index, please make sure the table it corresponds to is already a part of the database's metadata. 2) Even in case of index upsert(details below), this field is required. |
An array of column names on which the index is defined.
Example: ["column1"]
If the index is composite, this array will have multiple column names.
NOTE:
1) This cannot be an empty array.
2) When specifying an index, please make sure the columns it corresponds to is already a part of the database's metadata.
3) In case of index upsert(details below), this field can be optional.
4) The order in which the column names are specified is important. Since this implies the sequencing of the column in case of composite indices.|   
| data_structure    | str                   | The underlying data structure used by the index. The value for this field can be one among: ‘BTREE’, ‘HASH’, ’BITMAP’, ‘DENSE’, ‘SPARSE’, ‘REVERSE’, ‘OTHER’, ‘NONE’.
Example: "BTREE"
Default: "NONE" |
| index_type_detail          | str                   |  string containing custom detailed information about the index.
Example: "MULTI_COLUMN_STATISTICS" |
| is_ascending          | str                   | Set this boolean to True, if the index is created in ascending order, else set False.
NOTE: This is not valid for composite index. |
| filter_condition    | str                   | Filter condition used while creating index for a portion of rows in the table.
Example: "([filteredIndexCol]>(0))"
NOTE: This is not valid for composite index. |   
| is_foreign_key    | str                   | Set this boolean to True, if the index is a foreign key.
NOTE: When this is true, fields: ‘foreign_key_table_name‘ and ‘foreign_key_column_names‘ are required. |
| foreign_key_table_name          | str                   | The key of the parent table object which the foreign index refers to.
Example: "7.schema_a.table_a"
NOTE: This is required only if ‘is_foreign_key‘ is set to True.
Please make sure the table it corresponds to is already a part of the database's metadata. |
| foreign_key_column_names    | str                   | Description of the Virtual Data Source object|   
| title    | str                   | An array of column names on the parent table object which the foreign index refers to.
Example: ["column1"]
NOTE:
1) This is required only if ‘is_foreign_key‘ is set to True.
2) Please make sure the columns it corresponds to is already a part of the database's metadata.
3) The number of columns here should match the number of columns in ‘column_names’ field. |


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
get_schemas(query_params: SchemaParams = None) -> list
```

Query multiple Alation RDBMS Schemas.

Args:
* query_params (SchemaParams): REST API Get Filter Values.

Returns:
* list: Alation RDBMS Schemas.

### post_schemas

```
post_schemas(ds_id: int, schemas: list) -> bool
```

Post (Create or Update) Alation Schema Objects.


Args:
* ds_id (int): ID of the Alation Schemas' Parent Datasource.
* schemas (list): Alation Schemas to be created or updated.

Returns:
* bool: Success of the API POST Call(s)

### get_tables

```
get_tables(query_params: TableParams = None) -> list
```

Query multiple Alation RDBMS Tables.

Args:
* query_params (TableParams): REST API Get Filter Values.

Returns:
* list: Alation RDBMS Tables.

### post_tables

```
post_tables(ds_id: int, tables: list) -> bool
```

Post (Create or Update) Alation Table Objects.


Args:
* ds_id (int): ID of the Alation Tables' Parent Datasource.
* tables (list): Alation Tables to be created or updated.

Returns:
* bool: Success of the API POST Call(s)

### get_columns

```
get_columns(query_params: ColumnParams = None) -> list
```

Query multiple Alation RDBMS Columns.

Args:
* query_params (ColumnParams): REST API Get Filter Values.

Returns:
* list: Alation RDBMS Columns.

### post_columns

```
post_columns(ds_id: int, columns: list) -> bool
```

Post (Create or Update) Alation Column Objects.


Args:
* ds_id (int): ID of the Alation Columns' Parent Datasource.
* columns (list): Alation Columns to be created or updated.

Returns:
* bool: Success of the API POST Call(s)


## Examples
### Get Schemas
```python
import allie_sdk as allie

alation = allie.Alation(
    host='<HOST>',
    user_id=<USER_ID>,
    refresh_token='<REFRESH_TOKEN>')

# Get Schemas  
params = allie.SchemaParams(ds_id=3)
    get_schemas_result = alation.rdbms.get_schemas(query_params=params)
```

### Create Schemas
```python
import allie_sdk as allie

alation = allie.Alation(
    host='<HOST>',
    user_id=<USER_ID>,
    refresh_token='<REFRESH_TOKEN>')

# Create Schemas 
schema = allie.SchemaItem(title='Finance Schema', description='This is the Finance schema', key='2.finance')
post_schemas_result = alation.rdbms.post_schemas(ds_id=2, schemas=[schema])
```



