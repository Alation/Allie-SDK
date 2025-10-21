---
title: Virtual File System
parent: SDK Reference
---

# Dataflows Lineage V2
{:.no_toc}

* TOC
{:toc}

## Models

### Dataflow
Python object used to define a dataflow object to be created `create_or_replace_dataflows`.

Attributes:

| Name | Required | Type | Description                                                                                                                                                                                 |
|--|:--------:|------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| external_id |   TRUE   | str  | The external id of the dataflow object. To access this dataflow object uniquely.. "API/" previx is required.                                                                                |
| title |  FALSE   | str  | Title of the dataflow.                                                                                                                                                                      |  
| description |  FALSE   | str  | The description of the dataflow.                                                                                                                                                            |  
| content |  FALSE   | str  | The transformation logic, SQL statement.                                                                                                                                                    | 
| group_name|  FALSE   | str  | The name of the dataflow source group that the dataflow belongs to. Case sensitive. If an exact match is found then it would be used, otherwise it will create a new dataflow source group. | 
|

### DataflowPathObject
Python object used to define a lineage path.

Attributes:

| Name        | Required | Type | Description                                                                   |
|-------------|:--------:|------|-------------------------------------------------------------------------------|
| otype       |   TRUE   | str  | Type of the object for this lineage segment. (table, attibute, dataflow, etc) 
| key         |   TRUE   | str  | ULM key to identify the lineage path object                                   |  


### DataflowPayload
Python object used to define dataflow objects and lineage paths to be created `create_or_replace_dataflows`.

Attributes:

| Name             | Required | Type | Description                                                                                                                                                          |
|------------------|:--------:|------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| dataflow_objects |  FALSE   | list | The external id of the dataflow object. To access this dataflow object uniquely.. "API/" previx is required.                                                         |
| paths            |  FALSE   | list | "paths" is an array of "path"s. Each "path" specifies the details of sources (-> dataflows) -> targets lineage by listing elements of each step, or "segment", of the lineages in order.Each "segment" may contain data objects and/or dataflows, but the first and the last "segment" of a "path" SHOULD NOT contain any dataflows. 
                                                                                                                                                                    |  

### DataflowPatchItem
Python object used to define dataflow items to update/patch `patch_dataflows`.

Attributes:

| Name | Required | Type | Description                                                                                                                                                       |
|--|:--------:|------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id |   TRUE   | str  | The id of the dataflow object.                                                                                |
| title |  FALSE   | str  | Title of the dataflow.                                                                                                                                            |  
| description |  FALSE   | str  | The description of the dataflow.                                                                                                                                  |  
| content |  FALSE   | str  | The transformation logic, SQL statement.                                                                                                                          | 
| group_name|  FALSE   | str  | The name of the dataflow source group that the dataflow belongs to. Case sensitive. If an exact match is found then it would be used, otherwise it will create a new dataflow source group. | 
|

## Methods
## Methods
### get_dataflows

```
get_dataflows(object_ids: list, query_params: DataflowParams) -> DataflowPayload
```
Get Dataflow objects with related lineage paths 

Args:
* object_ids (list): Optional argument to filter dataflow object by.
* query_params: (DataflowParams) : Filter by param (id, external_id)

Returns:
* DataFlowPayload: Resulting object containing a list of requested DataFlow objects and their lineage paths.

### create_or_replace_dataflows

```
create_or_replace_dataflows(payload: DataflowPayload) -> list[JobDetailsDataflowPost]
```
Create/Replace Dataflow objects with related lineage paths

Args:
* payload (DataflowPayload): Data Class containing lsts of DataFlow and DataFlowPaths objects create or update.

Returns:
* List of JobDetails: Status report of the executed background jobs.

### update_dataflows

```
update_dataflows(payload: list[DataflowPatchItem] -> list[JobDetailsDataflowPost]
```
Update Dataflow objects definition. This method cannot be used to update lineage paths. 

Args:
* payload (DataflowPatchItem(list)): List of DataFlows (DataFLowPatchItem) to update

Returns:
* List of JobDetails: Status report of the executed background jobs.

### delete_dataflows

```
delete_dataflows(object_ids: list, query_params: DataflowParams) -> list[JobDetailsDataflowPost]
```
Get Dataflow objects with related lineage paths 

Args:
* object_ids (list): Optional argument to filter dataflow object by.
* query_params: (DataflowParams) : Filter by param (id, external_id)

Returns:
* List of JobDetails: Status report of the executed background jobs.

## Examples

See `/examples/example_dataflow.py`.