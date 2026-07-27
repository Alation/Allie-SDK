---
title: Data Products
parent: SDK Reference
---

# Data Products
{:.no_toc}

* TOC
{:toc}

The Data Products methods use the `/dps/integration/data-products/v1/` API namespace and cover:

- Data product CRUD
- Data product version management
- Marketplace CRUD
- Publishing and bulk publishing
- Standards checks
- Report result logging
- Marketplace search
- Permission management

## Models

### Spec Models

Use `DataProductSpec` when creating or updating a data product. The SDK also accepts a raw `dict` or YAML `str`, but the typed model gives you payload validation before the request is sent.

Core product spec models:

| Model | Purpose |
|------|------|
| `DataProductSpec` | Wrapper for the top-level `product` block. |
| `DataProductSpecDefinition` | Main product definition including `productId`, `version`, owners, delivery systems, record sets, and metadata. |
| `DataProductLanguage` | Localized product text such as `name`, `description`, and `shortDescription`. |
| `DataProductDeliverySystem` | Delivery system entry keyed inside `deliverySystems`. |
| `DataProductAccessRequestInstruction` | Manual or external access request instructions for a delivery system. |
| `DataProductRecordSet` | Record-set definition keyed inside `recordSets`. |
| `DataProductRecordSetField` | Schema field definition for a record set. |
| `DataProductRecordSetSample` | Mock sample data block for a record set. |
| `DataProductDataAccess` | Access details for a record set. |
| `DataProductQualifiedName` | Qualified database/schema/table/column information for SQL access. |
| `DataProductRelationship` | Relationship definition between record sets. |
| `DataProductMetadata` | Optional metadata block. |
| `DataProductMetric` | Metric definition inside `metadata.metrics`. |

### Marketplace Spec Models

Use `DataMarketplaceSpec` when creating or updating a marketplace.

| Model | Purpose |
|------|------|
| `DataMarketplaceSpec` | Wrapper for the top-level `marketplace` block. |
| `DataMarketplaceDefinition` | Main marketplace definition including `marketplaceId`, contact info, standards, and branding. |
| `DataMarketplaceLanguage` | Localized marketplace text such as `name`, `description`, and `heroImage`. |
| `DataProductStandard` | Badge or minimum-standard definition used in marketplace specs. |
| `DataProductStandardDisplayName` | Localized display label for a standard or badge. |

### Response Models

| Model | Purpose |
|------|------|
| `DataProduct` | Data product returned by list, get, create, update, publish, and version endpoints. |
| `DataProductWithMarketplaceInfo` | Data product response that also contains `marketplace_context`. |
| `DataMarketplace` | Marketplace returned by list, get, create, and update endpoints. |
| `DataProductMarketplaceAssociation` | Marketplace association entry attached to a `DataProduct`. |
| `DataProductVersionSummary` | Version summary returned when `group_by_product=True`. |

### Helper Models

| Model | Purpose |
|------|------|
| `DataProductParams` | Optional query parameters for `get_data_products`. |
| `DataMarketplaceParams` | Optional query parameters for `get_data_marketplaces` and `get_data_marketplace`. |
| `PublishedDataProductParams` | Optional query parameters for `get_published_data_products`. |
| `DataProductPublishParams` | Optional `version` query parameter for publish/update-published calls. |
| `DataProductVersionUpdate` | Request body for `update_data_product_version`. |
| `PublishInfo` | Product/version identifier for bulk publish operations. |
| `BulkPublishInfo` | Request body for `bulk_publish_data_products`. |
| `ProductReportResult` | Report payload for a single product. |
| `ProductReportResultRead` | Product-specific report result returned by the API. |
| `ReportResult` | Cross-product report payload. |
| `ReportResultRead` | Cross-product report result returned by the API. |
| `DataProductReportResultsParams` | Optional filter for product-specific report retrieval. |
| `ReportResultsParams` | Optional filters for cross-product report retrieval. |
| `DataProductCheck` | Request body for `check_data_product`. |
| `DataProductCheckStandard` | Standard entry used inside `DataProductCheck`. |
| `DataProductCheckResultItem` | Result row returned by `check_data_product`. |
| `DataProductSearchQuery` | Natural-language marketplace search request. |
| `DataProductPermission` | Permission request and response model. |
| `DataProductPermissionParams` | Optional filters for `get_permissions`. |

## Methods

### Data Products

```python
get_data_products(query_params: DataProductParams = None) -> list[DataProduct]
create_data_product(data_product_spec: DataProductSpec | dict | str) -> DataProduct
update_data_product(data_product_spec: DataProductSpec | dict | str) -> DataProduct
get_data_product(product_id: str) -> DataProduct
delete_data_product(product_id: str) -> JobDetails
```

### Versions

```python
get_data_product_version(product_id: str, version_id: str) -> DataProduct
update_data_product_version(
    product_id: str,
    version_id: str,
    data_product_version: DataProductVersionUpdate,
) -> DataProduct
delete_data_product_version(product_id: str, version_id: str) -> JobDetails
```

### Product Reports

```python
get_data_product_report_results(
    product_id: str,
    query_params: DataProductReportResultsParams = None,
) -> list[ProductReportResultRead]
log_data_product_report_results(
    product_id: str,
    report_results: list[ProductReportResult],
) -> JobDetails
```

### Marketplaces

```python
get_data_marketplaces(query_params: DataMarketplaceParams = None) -> list[DataMarketplace]
create_data_marketplace(marketplace_spec: DataMarketplaceSpec | dict | str) -> DataMarketplace
update_data_marketplace(marketplace_spec: DataMarketplaceSpec | dict | str) -> DataMarketplace
get_data_marketplace(
    marketplace_id: str,
    query_params: DataMarketplaceParams = None,
) -> DataMarketplace
delete_data_marketplace(marketplace_id: str) -> JobDetails
```

### Publishing

```python
get_published_data_products(
    marketplace_id: str,
    query_params: PublishedDataProductParams = None,
) -> list[DataProductWithMarketplaceInfo]
get_published_data_product(
    marketplace_id: str,
    product_id: str,
) -> DataProductWithMarketplaceInfo
publish_data_product(
    marketplace_id: str,
    product_id: str,
    query_params: DataProductPublishParams = None,
) -> DataProduct
update_published_data_product(
    marketplace_id: str,
    product_id: str,
    query_params: DataProductPublishParams = None,
) -> DataProduct
unpublish_data_product(marketplace_id: str, product_id: str) -> JobDetails
bulk_publish_data_products(
    marketplace_id: str,
    bulk_publish_info: BulkPublishInfo,
) -> list[DataProduct]
```

### Checks, Search, and Permissions

```python
check_data_product(data_product_check: DataProductCheck) -> list[DataProductCheckResultItem]
get_report_results(query_params: ReportResultsParams = None) -> list[ReportResultRead]
log_report_results(report_results: list[ReportResult]) -> JobDetails
search_data_products_in_marketplace(
    marketplace_id: str,
    search_query: DataProductSearchQuery,
) -> list[DataProductWithMarketplaceInfo]
get_permissions(query_params: DataProductPermissionParams = None) -> list[DataProductPermission]
create_permission(permission: DataProductPermission) -> JobDetails
update_permission(permission: DataProductPermission) -> JobDetails
delete_permission(permission: DataProductPermission) -> JobDetails
get_user_permissions() -> list[DataProductPermission]
```

## Notes

- The create and update endpoints for products and marketplaces accept either JSON or YAML. Pass a typed model or `dict` for JSON, or pass a raw YAML string when you want the request body sent as `application/x-yaml`.
- Product and marketplace list methods auto-paginate only when you do not set `limit` or `offset`.
- The SDK exposes `offset` in query param models, but the backing API currently expects the query-string key `skip`, so the SDK maps that for you.

## Examples

See `/examples/example_data_product.py`.

For a validation-failure example, see `/example_errors/data_product/create_data_product_invalid_spec.py`.
