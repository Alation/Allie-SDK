---
title: Datasources
parent: SDK Reference
---

# Datasources
{:.no_toc}

* TOC
{:toc}

## Models

### OCFDatasource

Individual list item returned in the response of the function `get_ocf_datasources` that represents a data source in Alation.


Attributes:

| Name                                  | Type      | Description                                                  |
| ------------------------------------- | --------- | ------------------------------------------------------------ |
| uri                                   | str       | Jdbc uri for connecting to datasources. Please ensure you either give  host, port or just uri parameter. Please do not enter both the parameters. |
| connector_id                          | int       | The OCF conector's id that we want to create datasource with. |
| db_username                           | str       | The service account username.                                |
| title                                 | str       | The title of the datasource.                                 |
| description                           | str       | The description of the datasource.                           |
| private                               | bool      | Boolean flag determining if the datasource is private. Defaults to False. |
| is_hidden                             | bool      | Boolean flag determining if the datasource is hidden. Defaults to False. |
| id                                    | int       | Unique  identifier of the datasource. INTERNAL               |
| supports_explain                      | bool      | INTERNAL                                                     |
| data_upload_disabled_message          | bool      | INTERNAL                                                     |
| is_gone                               | bool      | INTERNAL                                                     |
| supports_qli_diagnostics              | bool      | INTERNAL                                                     |
| latest_extraction_time                | str       | INTERNAL                                                     |
| negative_filter_words                 | list[str] | INTERNAL                                                     |
| can_data_upload                       | bool      | INTERNAL                                                     |
| qualified_name                        | str       | INTERNAL                                                     |
| all_schemas                           | str       | INTERNAL                                                     |
| has_previewable_qli                   | bool      | INTERNAL                                                     |
| supports_qli_daterange                | bool      | INTERNAL                                                     |
| latest_extraction_successful          | bool      | INTERNAL                                                     |
| owner_ids                             | list[int] | INTERNAL                                                     |
| favorited_by_list                     | bool      | INTERNAL                                                     |
| supports_compose                      | bool      | INTERNAL                                                     |
| enable_designated_credential          | bool      | INTERNAL                                                     |
| deleted                               | bool      | INTERNAL                                                     |
| limit_schemas                         | str       | INTERNAL                                                     |
| obfuscate_literals                    | list[str] | INTERNAL                                                     |
| remove_filtered_schemas               | bool      | INTERNAL                                                     |
| profiling_tip                         | str       | INTERNAL                                                     |
| supports_profiling                    | str       | INTERNAL                                                     |
| icon                                  | str       | INTERNAL                                                     |
| url                                   | str       | INTERNAL                                                     |
| otype                                 | str       | INTERNAL                                                     |
| exclude_schemas                       | str       | Schemas to exclude in MDE                                    |
| exclude_additional_columns_in_qli     | bool      | INTERNAL                                                     |
| can_toggle_ds_privacy                 | bool      | INTERNAL                                                     |
| supports_md_diagnostics               | bool      | INTERNAL                                                     |
| supports_ocf_query_service_api        | bool      | INTERNAL                                                     |
| uses_ocf_agent                        | bool      | INTERNAL                                                     |
| nosql_mde_sample_size                 | int       | INTERNAL                                                     |
| disable_auto_extraction               | bool      | INTERNAL                                                     |
| unresolved_mention_fingerprint_method | bool      | INTERNAL                                                     |
| enable_default_schema_extraction      | bool      | INTERNAL                                                     |
| enabled_in_compose                    | bool      | INTERNAL                                                     |
| builtin_datasource                    | str       | INTERNAL                                                     |
| cron_extraction                       | str       | INTERNAL                                                     |
| supports_default_schema_extraction    | bool      | INTERNAL                                                     |


### OCFDatasourceParams
Optional item used to filter the response of the returned data from the function `get_ocf_datasources`.

Attributes:

| Name             | Type | Description |
|------------------|------|-------------|
| include_hidden   | bool | Specifies if hidden datasources should be included in retrieved list. Hidden data sources are not visible in the UI. These are the data sources created via the API with the `is_hidden` property set to `True`. |
| exclude_suspended | bool | When enabled, suspended datasources are excluded from the response payload. |

### OCFDatasourcePostItem

Dataclass that represents the payload accepted by `create_ocf_datasource`.

Attributes:

| Name                             | Type      | Description |
|----------------------------------|-----------|-------------|
| connector_id                     | int       | The OCF connector identifier to associate with the new datasource. |
| title                            | str       | Human readable name for the datasource. |
| uri                              | str       | JDBC URI that the datasource should use during extraction. |
| db_username                      | str       | Service account used to connect to the database. |
| description                      | str       | Optional description shown in the catalog. |
| private                          | bool      | Marks the datasource as private in the catalog UI. |
| is_hidden                        | bool      | Hides the datasource from the UI while keeping it accessible through the API. |


Fields that are read-only in the REST API are automatically removed from the generated payload.

### OCFDatasourcePutItem

Dataclass used by `update_ocf_datasource` to represent mutable datasource fields. Only populated attributes are included in the API request.

Attributes:

| Name                | Type      | Description                                    |
|---------------------|-----------|------------------------------------------------|
| title               | str       | Updated datasource title.                      |
| description         | str       | Updated datasource description.                |
| private             | bool      | Updates the privacy setting of the datasource. |
| uri                 | str       | Updated JDBC URI.                              |
| db_username         | str       | Updated service account username.              |
| db_password         | str       | Updated service account password.              |
| compose_default_uri | bool      | Compose default URI                            |

### OCFDatasourceGetParams

Optional query parameters used by `get_ocf_datasource_by_id`.

| Name              | Type | Description |
|-------------------|------|-------------|
| exclude_suspended | bool | When enabled, suspended datasources are excluded from the response payload. |


### NativeDatasource

Individual list item returned in the response of the function `get_native_datasources` that represents a data source in Alation.

Attributes:

| Name                                  | Type      | Description                                                  |
| ------------------------------------- | --------- | ------------------------------------------------------------ |
| dbtype                                | str       | The database type. Currently the certified types are mysql, oracle,  postgresql,     sqlserver, redshift, teradata and snowflake. |
| host                                  | str       | The host of the datasource. Note: Not required if is_virtual == True or  if the 'uri' parameter is provided. |
| port                                  | int       | The port of the datasource. Note: Not required if is_virtual == True or  if the 'uri' parameter is provided. |
| uri                                   | str       | Jdbc uri for connecting to datasources. Please ensure you either give  host, port or just uri parameter. Please do not enter both the parameters. |
| dbname                                | str       | The database name of the datasource. Note: Mandatory for Oracle (service  name is dbname), Redshift and Postgresql datasource. |
| db_username                           | str       | The service account username. Note: Not required if  deployment_setup_complete == False     or is_virtual == True. |
| title                                 | str       | The title of the datasource. Note: Not required if  deployment_setup_complete == False. |
| description                           | str       | The description of the datasource.                           |
| deployment_setup_complete             | bool      | Boolean flag determining if the deployment setup is complete. When set to  true, complete datasource information is required, else, only partial  information is required. Defaults to True. |
| private                               | bool      | Boolean flag determining if the datasource is private. Defaults to False. |
| is_virtual                            | bool      | Boolean flag determining if the datasource is virtual. Defaults to False. |
| is_hidden                             | bool      | Boolean flag determining if the datasource is hidden. Defaults to False. |
| id                                    | int       | Unique  identifier of the datasource. INTERNAL               |
| supports_explain                      | bool      | INTERNAL                                                     |
| data_upload_disabled_message          | str       | INTERNAL                                                     |
| hive_logs_source_type                 | int       | Hive related                                                 |
| metastore_uri                         | bool      | Hive related                                                 |
| is_hive                               | bool      | INTERNAL                                                     |
| is_gone                               | bool      | INTERNAL                                                     |
| webhdfs_server                        | str       | Hive related                                                 |
| supports_qli_diagnostics              | bool      | INTERNAL                                                     |
| is_presto_hive                        | bool      | Presto related                                               |
| latest_extraction_time                | str       | INTERNAL                                                     |
| negative_filter_words                 | list[str] | INTERNAL                                                     |
| has_hdfs_based_qli                    | bool      | Hive related                                                 |
| can_data_upload                       | bool      | INTERNAL                                                     |
| qualified_name                        | str       | INTERNAL                                                     |
| all_schemas                           | str       | INTERNAL                                                     |
| has_previewable_qli                   | bool      | INTERNAL                                                     |
| hive_tez_logs_source                  | str       | Hive related                                                 |
| has_metastore_uri                     | bool      | Hive related                                                 |
| webhdfs_port                          | int       | Hive related                                                 |
| supports_qli_daterange                | bool      | INTERNAL                                                     |
| latest_extraction_successful          | bool      | INTERNAL                                                     |
| owner_ids                             | list[int] | INTERNAL                                                     |
| favorited_by_list                     | bool      | INTERNAL                                                     |
| supports_compose                      | bool      | INTERNAL                                                     |
| hive_logs_source                      | str       | Hive related                                                 |
| enable_designated_credential          | bool      | INTERNAL                                                     |
| deleted                               | bool      | INTERNAL                                                     |
| limit_schemas                         | str       | Schemas to limit in MDE                                      |
| obfuscate_literals                    | list[str] | INTERNAL                                                     |
| remove_filtered_schemas               | bool      | INTERNAL                                                     |
| profiling_tip                         | str       | INTERNAL                                                     |
| supports_profiling                    | bool      | INTERNAL                                                     |
| webhdfs_username                      | str       | Hive related                                                 |
| icon                                  | str       | INTERNAL                                                     |
| url                                   | str       | INTERNAL                                                     |
| otype                                 | str       | INTERNAL                                                     |
| exclude_schemas                       | str       | Schemas to exclude in MDE                                    |
| qli_aws_region                        | str       | Hive related                                                 |
| has_aws_glue_metastore                | bool      | Hive related                                                 |
| exclude_additional_columns_in_qli     | bool      | INTERNAL                                                     |
| can_toggle_ds_privacy                 | bool      | INTERNAL                                                     |
| aws_region                            | str       | Hive related                                                 |
| aws_access_key_id                     | str       | Hive related                                                 |
| supports_md_diagnostics               | bool      | INTERNAL                                                     |
| nosql_mde_sample_size                 | int       | INTERNAL                                                     |
| disable_auto_extraction               | bool      | INTERNAL                                                     |
| metastore_type                        | str       | Hive related                                                 |
| unresolved_mention_fingerprint_method | str       | INTERNAL                                                     |
| qli_hive_connection_source            | str       | Hive related                                                 |
| compose_oauth_enabled                 | bool      | Snowflake and Databricks related                             |
| enable_default_schema_extraction      | bool      | INTERNAL                                                     |
| enabled_in_compose                    | bool      | INTERNAL                                                     |
| builtin_datasource                    | str       | INTERNAL                                                     |
| has_aws_s3_based_qli                  | bool      | Hive related                                                 |
| qli_aws_access_key_id                 | str       | Hive related                                                 |
| jdbc_driver                           | str       | INTERNAL                                                     |
| cron_extraction                       | str       | INTERNAL                                                     |
| supports_default_schema_extraction    | bool      | INTERNAL                                                     |

### NativeDatasourceParams
Optional item used to filter the response of the returned data from the function `get_native_datasources`.

Attributes:

| Name  | Type | Description                                                                                                                |
|-------|------|----------------------------------------------------------------------------------------------------------------------------|
| include_undeployed| bool | Specifies if undeployed datasources should be included in retrieved list. Undeployed data sources are the ones whose configurations and deployment setup is not complete. Admins cannot trigger metadata extraction on undeployed data sources.|
| include_hidden   | bool | Specifies if hidden datasources should be included in retrieved list. Hidden data sources are not visible in the UI. These are the data sources created via the API with the is_hidden property set to True. There is no UI for the Settings page of such sources and they can only be accessed through the API.  |

## Methods

### get_ocf_datasources

```
get_ocf_datasources(self, query_params:OCFDatasourceParams = None) -> list[OCFDatasource]:
```

Query multiple Alation OCF Data Sources and return their details.

Args:
* query_params (`OCFDatasourceParams`): REST API OCF Datasource Query Parameters.
Returns:
* list: Alation OCF Data Sources

### create_ocf_datasource

```
create_ocf_datasource(self, datasource: OCFDatasourcePostItem) -> OCFDatasource:
```

Create a new OCF datasource.

Args:
* datasource (`OCFDatasourcePostItem`): The datasource configuration to submit.
Returns:
* `OCFDatasource`: The created datasource returned by the API.

### get_ocf_datasource_by_id

```
get_ocf_datasource_by_id(self, datasource_id: int, query_params: OCFDatasourceGetParams = None) -> OCFDatasource:
```

Retrieve the details for a single OCF datasource.

Args:
* datasource_id (int): Identifier of the datasource to retrieve.
* query_params (`OCFDatasourceGetParams`): Optional query parameter container.
Returns:
* `OCFDatasource`: The requested datasource.

### update_ocf_datasource

```
update_ocf_datasource(self, datasource_id: int, datasource: OCFDatasourcePutItem) -> OCFDatasource:
```

Update an existing OCF datasource in place.

Args:
* datasource_id (int): Identifier of the datasource to update.
* datasource (`OCFDatasourcePutItem`): Fields to update.
Returns:
* `OCFDatasource`: The updated datasource returned by the API.

### delete_ocf_datasource

```
delete_ocf_datasource(self, datasource_id: int) -> JobDetails:
```

Delete an OCF datasource by identifier.

Args:
* datasource_id (int): Identifier of the datasource to delete.
Returns:
* `JobDetails`: Empty response model confirming the deletion request.

### get_native_datasources

```
get_native_datasources(self, query_params:NativeDatasourceParams = None) -> list[NativeDatasource]:
```

Query multiple Alation Native Data Sources and return their details.

Args:
* query_params (`NativeDatasourceParams`): REST API Native Datasource Query Parameters.
Returns:
* list: Alation Native Data Sources

## Examples

See `/examples/example_data_source.py`.
