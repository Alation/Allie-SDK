---
title: BI Source
parent: SDK Reference
---

# BI Source
{:.no_toc}

* TOC
{:toc}



**Module Name:** `allie_sdk.methods.bi_source`

**Description:** Alation REST API BI Source Methods.

-----

## Class: `AlationBISource`

The main class for interacting with Alation BI Source entities via the REST API.

## BI Source Methods

The following methods are defined directly within the `AlationBISource` class for managing BI Servers, Folders, Reports, and Report Columns.

### Create and Update Methods

These methods are generally **not allowed for non-virtual BI Servers**.

| Method | Description | Details |
| :--- | :--- | :--- |
| **`create_bi_servers`** | Post (Create) Alation **BI Servers**. Used for creating **Virtual BI Servers**. | **Args:** `bi_servers` (`list[BIServerItem]`). **Returns:** `JobDetailsBIServerPost`. |
| **`create_or_update_bi_folders_using_external_id`** | Create/Update **BI Folders** via **`external_id`**. Updates if an object with a matching `external_id` exists, otherwise creates it. | **Args:** `bi_server_id` (`int`), `bi_folders` (`list[BIFolderItem]`). **Returns:** `list[JobDetails]`. |
| **`create_or_update_bi_report_columns_using_external_id`** | Create/Update **BI Report Columns** via **`external_id`**. Updates if an object with a matching `external_id` exists, otherwise creates it. | **Args:** `bi_server_id` (`int`), `bi_report_columns` (`list[BIReportColumnItem]`). **Returns:** `list[JobDetails]`. |
| **`create_or_update_bi_reports_using_external_id`** | Create/Update **BI Reports** via **`external_id`**. Updates if an object with a matching `external_id` exists, otherwise creates it. | **Args:** `bi_server_id` (`int`), `bi_reports` (`list[BIReportItem]`). **Returns:** `list[JobDetails]`. |
| **`update_bi_folder_using_internal_id`** | PATCH (Update) an Alation **BI Folder** using its internal ID. | **Args:** `bi_server_id` (`int`), `bi_folder_id` (`int`), `bi_folder` (`BIFolderItem`). **Returns:** `BIFolder`. |
| **`update_bi_report_column_using_internal_id`** | PATCH (Update) a single **BI Report Column** using its internal ID. | **Args:** `bi_server_id` (`int`), `bi_report_column_id` (`int`), `bi_report_column` (`BIReportColumnItem`). **Returns:** `BIReportColumn`. |
| **`update_bi_report_using_internal_id`** | PATCH (Update) an Alation **BI Report** using its internal ID. | **Args:** `bi_server_id` (`int`), `bi_report_id` (`int`), `bi_report` (`BIReportItem`). **Returns:** `BIReport`. |
| **`update_bi_server`** | PATCH (Update) an Alation **BI Server**. | **Args:** `bi_server_id` (`int`), `bi_server` (`BIServerItem`). **Returns:** `JobDetails`. |

-----

### Retrieval (GET) Methods

| Method | Description | Details |
| :--- | :--- | :--- |
| **`get_bi_servers`** | Get multiple Alation **BI Servers**. | **Args:** `query_params` (`BIServerParams` - optional). **Returns:** `list[BIServer]`. |
| **`get_a_bi_folder`** | Get a single Alation **BI Folder**. | **Args:** `bi_server_id` (`int`), `bi_folder_id` (`int`). **Returns:** `BIFolder`. |
| **`get_bi_folders`** | Get multiple Alation **BI Folders**. | **Args:** `bi_server_id` (`int`), `query_params` (`BIFolderParams` - optional). **Returns:** `list[BIFolder]`. |
| **`get_a_bi_report`** | Get a single Alation **BI Report**. | **Args:** `bi_server_id` (`int`), `bi_report_oid` (`int`). **Returns:** `BIReport`. |
| **`get_bi_reports`** | Get multiple Alation **BI Reports**. | **Args:** `bi_server_id` (`int`), `query_params` (`BIReportParams` - optional). **Returns:** `list`. |
| **`get_bi_report_columns`** | GET a set of **report columns** from a specified BI Server. | **Args:** `server_id` (`str`), `query_params` (`BIReportColumnParams` - optional). **Returns:** `list[BIReportColumn]`. |

-----

### Deletion Methods

These methods are generally **not allowed for non-virtual BI Servers**. Bulk delete methods require a range of IDs in `query_params`.

| Method | Description | Details |
| :--- | :--- | :--- |
| **`delete_a_bi_report`** | Delete a single Alation **BI report**. | **Args:** `bi_server_id` (`int`), `bi_report_id` (`int`). **Returns:** `bool` (Success of the API DELETE Call). |
| **`delete_bi_folders`** | Delete Alation **BI Folders**. Requires `query_params`. | **Args:** `bi_server_id` (`int`), `query_params` (`BIFolderParams`). **Returns:** `JobDetails`. |
| **`delete_bi_report_columns`** | Delete Alation **BI report columns**. | **Args:** `bi_server_id` (`int`), `query_params` (`BIReportColumnParams` - optional). **Returns:** `JobDetails`. |
| **`delete_bi_reports`** | Delete Alation **BI reports**. | **Args:** `bi_server_id` (`int`), `query_params` (`BIReportParams` - optional). **Returns:** `JobDetails`. |

