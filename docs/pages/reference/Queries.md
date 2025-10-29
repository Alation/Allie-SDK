---
title: Queries
parent: SDK Reference
---

# Queries
{:.no_toc}

* TOC
{:toc}

## Models

### QueryItem
Payload model used when creating a query via `create_query`.

| Name         | Required | Type        | Description |
|--------------|:--------:|-------------|-------------|
| datasource_id | TRUE | int | ID of the datasource that owns the query. |
| content | TRUE | str | SQL text that will be stored for the query. |
| saved | FALSE | bool | Whether the query should be saved (defaults to True). |
| published | FALSE | bool | Whether the query should be published (defaults to False). |
| title | FALSE | str | Title that appears in the catalog. |
| description | FALSE | str | Catalog description of the query. |
| tag_names | FALSE | list[str] | Tags to associate with the query. |
| domain_ids | FALSE | list[int] | Domain identifiers to assign. |
| author | FALSE | QueryAuthor | Admin-only field that reassigns authorship. |

### QueryAuthor
Author metadata that can be optionally attached to a query.

| Name | Type | Description |
|------|------|-------------|
| id | int | The numeric ID of the user. |
| email | str | The email address of the user. |
| username | str | The username of the user. |

### Query
Represents the response returned by the create query API.

| Name | Type | Description |
|------|------|-------------|
| id | int | Unique identifier of the query. |
| datasource_id | int | ID of the datasource associated with the query. |
| autosave_content | str | Autosaved SQL content. |
| content | str | Saved SQL content. |
| title | str | Query title. |
| description | str | Query description. |
| saved | bool | Indicates whether the query is saved. |
| published | bool | Indicates whether the query is published. |
| domains | list[QueryDomain] | Domains applied to the query. |
| tags | list[QueryTag] | Tags applied to the query. |
| datasource | QueryDatasource | Datasource context for the query. |
| ts_last_saved | datetime | Timestamp of the last save. |
| has_unsaved_changes | bool | Whether there are outstanding edits. |
| catalog_url | str | Catalog URL for the query object. |
| compose_url | str | Compose URL for editing the query. |
| schedules | list | Schedule metadata associated with the query. |

### QueryDomain
Domain metadata returned alongside a query.

| Name | Type | Description |
|------|------|-------------|
| id | int | Domain identifier. |
| title | str | Domain title. |
| description | str | Domain description. |

### QueryTag
Tag metadata returned alongside a query.

| Name | Type | Description |
|------|------|-------------|
| id | int | Tag identifier. |
| name | str | Tag name. |
| description | str | Tag description. |
| ts_created | datetime | Timestamp for when the tag was created. |
| ts_updated | datetime | Timestamp for when the tag was last updated. |
| url | str | Catalog URL for the tag. |

### QueryDatasource
Datasource reference returned alongside a query.

| Name | Type | Description |
|------|------|-------------|
| id | int | Datasource identifier. |
| title | str | Datasource title. |
| uri | str | Datasource connection URI. |
| url | str | Catalog URL for the datasource. |

## Methods

### create_query

```
create_query(query: QueryCreateRequest) -> Query
```

Create a query in Alation on behalf of the authenticated user (or a specific author when executed by an admin).

Args:
* query (`QueryItem`): Payload describing the query to create.

Returns:
* `Query`: The created query with catalog metadata.

### get_queries

```
get_queries(query_params: QueryParams) -> list[Query]
```

Retrieve the details of queries based on certain parameters.

Args:
* query_params (`QueryParams`): several filter options

Returns:
* `list[Query]`: list of Alation Queries.

### get_query

```
get_query(query_id: int) -> Query
```

Retrieve the query details for the supplied query identifier.

Args:
* query_id (`int`): The catalog ID of the query.

Returns:
* `Query`: Details of the query.

### get_query_sql

```
get_query_sql(query_id: int) -> str
```

Retrieve the saved SQL text for the supplied query identifier.

Args:
* query_id (`int`): The catalog ID of the query.

Returns:
* `str`: The SQL text that was most recently saved.

## TLS considerations for Python 3.13 and Zscaler

When Python 3.13 is used behind Zscaler, the interpreter may ignore the `certifi` bundle and fall back to OpenSSL's default trust store. If HTTPS requests start failing, follow these steps:

1. Export Zscaler's full certificate chain from macOS Keychain.
2. Locate the OpenSSL CA bundle that ships with your Python 3.13 installation.
3. Back up the bundle, then append the Zscaler chain to the end of the file.
4. Re-test the TLS connection. For pip, optionally set the `PIP_CERT` environment variable or `pip.conf` to point at the combined bundle so package installations succeed consistently.

## Examples

See `/examples/example_query.py` for a complete walkthrough.
