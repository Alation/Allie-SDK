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
Sub-model used in the parent Models of `Schema`, `Table`, `Column` and `Index`.

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
| partitioning_attributes    | list                   | An array of columns which are used to partition the table. Example: ["column1", "column2"]|   
| bucket_attributes    | list                   | An array of columns which are used to bucket the table (in data sources like Hive, bucketing is an alternative mechanism to partitioning for grouping similar data together: LanguageManualDDL-BucketedTables). Example: ["column1", "column2"] |
| sort_attributes          | list                   | An array of columns used to sort the table (in Hive, used with bucketing to store data for faster computation: LanguageManualDDL-BucketedSortedTables). Example: ["column1", "column2"]. |
| synonyms    | list                   | An array of other names that can be used to refer to this table. Each synonym is represented as a JSON comprising schema_name and table_name. Example: [{"schema_name": "schema_a","table_name": "table_a"}, {"schema_name": "schema_b","table_name": "table_b"}]. |   
| skews_info    | dict                   | A JSON of the skew column names to an array of their respective skewed column values that appear very often. Example:{"column1": ["column1_value1", "column1_value2"], "column2": ["column2_value1", "column2_value2"]}. |
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
| db_owner    | str                   | Name of the database account that owns this table.|   
| view_sql    | str                   | CREATE VIEW statement which was used to create the view. |
| view_sql_expanded          | str                   | CREATE VIEW statement with fully qualified object references. |
| ts_created    | str                   | Timestamp at which the table or view was created. Example: 2018-03-13T22:09:33Z|   
| ts_last_altered    | str                   | Timestamp of the last ALTER statement executed against this table. Example: 2018-03-13T22:09:33Z |
| partitioning_attributes    | list                   | An array of columns which are used to partition the table. Example: ["column1", "column2"]|   
| bucket_attributes    | list                   | An array of columns which are used to bucket the table (in data sources like Hive, bucketing is an alternative mechanism to partitioning for grouping similar data together: LanguageManualDDL-BucketedTables). Example: ["column1", "column2"] |
| sort_attributes          | list                   | An array of columns used to sort the table (in Hive, used with bucketing to store data for faster computation: LanguageManualDDL-BucketedSortedTables). Example: ["column1", "column2"]. |
| synonyms    | list                   | An array of other names that can be used to refer to this table. Each synonym is represented as a JSON comprising schema_name and table_name. Example: [{"schema_name": "schema_a","table_name": "table_a"}, {"schema_name": "schema_b","table_name": "table_b"}]. |   
| skews_info    | dict                   | A JSON of the skew column names to an array of their respective skewed column values that appear very often. Example:{"column1": ["column1_value1", "column1_value2"], "column2": ["column2_value1", "column2_value2"]}. |
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
| position    | int                   | Position of the column in the table which contains it. <br> NOTE: <br> 1) This value needs to be a positive integer. <br> 2) When specifying a column, please make sure the table it corresponds to is already a part of the database's metadata..|   
| column_comment    | str                   | A comment field that stores a description of the column which is ingested from the source system. |
| nullable          | bool                   | Field to indicate if the column can be nullable. Set this to true if the column is a nullable field, false otherwise. |

### VirtualDataSourceIndex
Python object used to create an `Index` in Alation and passed in the parameter `vds_objects` as a list in the function `post_metadata`.

Attributes:
Key, description, title are inherited from VirtualDataSourceItem. The key, index_type and column_names are required

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| key          | str                   | Key of the Virtual Data Source object |
| description    | str                   | Description of the Virtual Data Source object|   
| title    | str                   | Title of the Virtual Data Source object |
| index_type          | str                   | The type of the index. The value for this field can be one among: ‘PRIMARY’, ‘SECONDARY’, ‘PARTITIONED_PRIMARY’, ‘UNIQUE’, ‘OTHER’. Example: "PRIMARY" The presence of this field distinguishes index object from a column. <br> NOTE: <br> 1) When specifying an index, please make sure the table it corresponds to is already a part of the database's metadata.<br> 2) Even in case of index upsert, this field is required.  | 
| column_names          | list                   | An array of column names on which the index is defined. Example: ["column1"] If the index is composite, this array will have multiple column names. <br> NOTE:<br> 1) This cannot be an empty array. <br>2) When specifying an index, please make sure the columns it corresponds to is already a part of the database's metadata. <br>3) In case of index upsert(details below), this field can be optional. <br>4) The order in which the column names are specified is important. Since this implies the sequencing of the column in case of composite indices. | 
| data_structure    | str                   | The underlying data structure used by the index. The value for this field can be one among: ‘BTREE’, ‘HASH’, ’BITMAP’, ‘DENSE’, ‘SPARSE’, ‘REVERSE’, ‘OTHER’, ‘NONE’. Example: "BTREE" Default: "NONE" |
| index_type_detail          | str                   |  string containing custom detailed information about the index. Example: "MULTI_COLUMN_STATISTICS" |
| is_ascending          | bool                   | Set this boolean to True, if the index is created in ascending order, else set False. NOTE: This is not valid for composite index. |
| filter_condition    | str                   | Filter condition used while creating index for a portion of rows in the table. Example: "([filteredIndexCol]>(0))" <br> NOTE: This is not valid for composite index. |   
| is_foreign_key    | bool                   | Set this boolean to True, if the index is a foreign key. <br> NOTE: When this is true, fields: ‘foreign_key_table_name‘ and ‘foreign_key_column_names‘ are required. |
| foreign_key_table_name          | str                   | The key of the parent table object which the foreign index refers to. Example: "7.schema_a.table_a" <br> NOTE: This is required only if ‘is_foreign_key‘ is set to True. Please make sure the table it corresponds to is already a part of the database's metadata. |
| foreign_key_column_names    | list                   |  An array of column names on the parent table object which the foreign index refers to. Example: ["column1"] <br> NOTE: <br> 1) This is required only if ‘is_foreign_key‘ is set to True.<br> 2) Please make sure the columns it corresponds to is already a part of the database's metadata. <br>3) The number of columns here should match the number of columns in ‘column_names’ field. |   



## Methods
### post_metadata

```
post_metadata(ds_id: int, vds_objects: list, query_params: VirtualDataSourceParams = None) -> list[JobDetailsVirtualDatasourcePost]
```
Add/Update/Remove Virtual Data Source Objects

Args:
* ds_id (int): Virtual data source id.
* vds_objects (list): Virtual Data Source object list.
* query_params: (VirtualDataSourceParams): Query Params for the POST request.

Returns:
* List of JobDetailsVirtualDatasourcePost: Status report of the executed background jobs.



## Examples

See `/examples/example_virtual_data_source.py`.