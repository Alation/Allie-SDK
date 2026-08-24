"""Tests for the Data Products API data models."""

from datetime import datetime

import pytest

from allie_sdk.core.custom_exceptions import InvalidPostBody
from allie_sdk.models.data_product_model import (
    BulkPublishInfo,
    DataMarketplace,
    DataMarketplaceDefinition,
    DataMarketplaceLanguage,
    DataMarketplaceSpec,
    DataProduct,
    DataProductCheck,
    DataProductCheckStandard,
    DataProductDescription,
    DataProductMetric,
    DataProductParams,
    DataProductPermission,
    DataProductPermissionParams,
    DataProductRecordSet,
    DataProductRecordSetField,
    DataProductRecordSetSample,
    DataProductSearchQuery,
    DataProductSpec,
    DataProductSpecDefinition,
    DataProductStandard,
    DataProductStandardDisplayName,
    DataProductVersionUpdate,
    ProductReportResultRead,
    PublishInfo,
    ReportResultRead,
)


class TestDataProductModels:
    def test_data_product_spec_generates_payload(self):
        spec = DataProductSpec(
            product=DataProductSpecDefinition(
                productId="finance:arr_sales_churn",
                version="1.0.0",
                contactEmail="data-products@example.com",
                contactName="Jane Doe",
                en=DataProductDescription(
                    name="ARR, Sales, and Churn",
                    shortDescription="Financial KPIs",
                ),
                recordSets={
                    "arr_metrics": DataProductRecordSet(
                        name="ARR Metrics",
                        schema=[
                            DataProductRecordSetField(
                                name="month",
                                type="date",
                                description="The month the metric applies to.",
                            )
                        ],
                        sample=DataProductRecordSetSample(
                            type="mock",
                            data="month\n2024-01-01",
                        ),
                    )
                },
                metadata={
                    "metrics": {
                        "numberOfCustomers": {
                            "displayName": "Number of Customers",
                            "description": "Tracked customers",
                            "expression": "COUNT(DISTINCT customer_id)",
                            "columns": ["customer_id"],
                        }
                    }
                },
            )
        )

        payload = spec.generate_api_payload()

        assert payload == {
            "product": {
                "productId": "finance:arr_sales_churn",
                "version": "1.0.0",
                "contactEmail": "data-products@example.com",
                "contactName": "Jane Doe",
                "en": {
                    "name": "ARR, Sales, and Churn",
                    "shortDescription": "Financial KPIs",
                },
                "recordSets": {
                    "arr_metrics": {
                        "name": "ARR Metrics",
                        "schema": [
                            {
                                "name": "month",
                                "type": "date",
                                "description": "The month the metric applies to.",
                            }
                        ],
                        "sample": {
                            "type": "mock",
                            "data": "month\n2024-01-01",
                        },
                    }
                },
                "metadata": {
                    "metrics": {
                        "numberOfCustomers": {
                            "displayName": "Number of Customers",
                            "description": "Tracked customers",
                            "expression": "COUNT(DISTINCT customer_id)",
                            "columns": ["customer_id"],
                        }
                    }
                },
            }
        }

    def test_data_marketplace_spec_generates_payload(self):
        spec = DataMarketplaceSpec(
            marketplace=DataMarketplaceDefinition(
                marketplaceId="finance:public",
                contactName="Allie",
                contactEmail="allie@example.com",
                en=DataMarketplaceLanguage(
                    name="Finance Marketplace",
                    description="Products for the finance team.",
                ),
                badges=[
                    DataProductStandard(
                        type="static",
                        check="Has contact email",
                        key="product.contactEmail",
                        displayName=DataProductStandardDisplayName(en="Contact email"),
                    )
                ],
                minimumStandard=[
                    DataProductStandard(
                        type="static",
                        check="Has description",
                        key="product.en.description",
                        displayName=DataProductStandardDisplayName(en="Description"),
                        onFail="fail",
                    )
                ],
            )
        )

        payload = spec.generate_api_payload()

        assert payload == {
            "marketplace": {
                "marketplaceId": "finance:public",
                "contactName": "Allie",
                "contactEmail": "allie@example.com",
                "en": {
                    "name": "Finance Marketplace",
                    "description": "Products for the finance team.",
                },
                "badges": [
                    {
                        "type": "static",
                        "check": "Has contact email",
                        "key": "product.contactEmail",
                        "displayName": {"en": "Contact email"},
                    }
                ],
                "minimumStandard": [
                    {
                        "type": "static",
                        "check": "Has description",
                        "key": "product.en.description",
                        "displayName": {"en": "Description"},
                        "onFail": "fail",
                    }
                ],
            }
        }

    def test_data_product_response_maps_nested_models(self):
        api_response = {
            "product_id": "finance:last_quarter_sales",
            "version_id": "1.0.0",
            "status": "draft",
            "spec_json": {
                "product": {
                    "productId": "finance:last_quarter_sales",
                    "version": "1.0.0",
                    "contactEmail": "ann@example.com",
                    "contactName": "Ann",
                    "en": {
                        "name": "Last Quarter Sales",
                        "description": "Data about last quarter sales",
                    },
                }
            },
            "ts_created": "2025-01-24T16:01:28.000000Z",
            "ts_updated": "2025-01-24T16:07:23.000000Z",
            "versions_details": [
                {
                    "version_id": "1.0.0",
                    "name": "Last Quarter Sales",
                    "status": "draft",
                    "ts_created": "2025-01-24T16:01:28.000000Z",
                    "ts_updated": "2025-01-24T16:07:23.000000Z",
                }
            ],
            "marketplace_associations": [
                {
                    "marketplace": {
                        "external_id": "finance:public",
                        "name": "Finance Marketplace",
                    },
                    "state": {
                        "status": "listed",
                        "ts_created": "2025-01-25T10:00:00.000000Z",
                        "ts_updated": "2025-01-25T10:00:00.000000Z",
                    },
                }
            ],
        }

        result = DataProduct.from_api_response(api_response)

        assert result == DataProduct(
            product_id="finance:last_quarter_sales",
            version_id="1.0.0",
            status="draft",
            spec_json=DataProductSpec(
                product=DataProductSpecDefinition(
                    productId="finance:last_quarter_sales",
                    version="1.0.0",
                    contactEmail="ann@example.com",
                    contactName="Ann",
                    en=DataProductDescription(
                        name="Last Quarter Sales",
                        description="Data about last quarter sales",
                    ),
                )
            ),
            ts_created=datetime(2025, 1, 24, 16, 1, 28),
            ts_updated=datetime(2025, 1, 24, 16, 7, 23),
            versions_details=[
                {
                    "version_id": "1.0.0",
                    "name": "Last Quarter Sales",
                    "status": "draft",
                    "ts_created": datetime(2025, 1, 24, 16, 1, 28),
                    "ts_updated": datetime(2025, 1, 24, 16, 7, 23),
                }
            ],
            marketplace_associations=[
                {
                    "marketplace": {
                        "external_id": "finance:public",
                        "name": "Finance Marketplace",
                    },
                    "state": {
                        "status": "listed",
                        "ts_created": datetime(2025, 1, 25, 10, 0, 0),
                        "ts_updated": datetime(2025, 1, 25, 10, 0, 0),
                    },
                }
            ],
        )

    def test_marketplace_response_maps_nested_models(self):
        api_response = {
            "external_marketplace_id": "finance:public",
            "spec": {
                "marketplace": {
                    "marketplaceId": "finance:public",
                    "contactName": "Allie",
                    "contactEmail": "allie@example.com",
                    "en": {"name": "Finance Marketplace"},
                }
            },
            "products": [
                {
                    "product_id": "finance:last_quarter_sales",
                    "version_id": "1.0.0",
                    "status": "ready",
                }
            ],
            "products_total": 1,
        }

        result = DataMarketplace.from_api_response(api_response)

        assert result == DataMarketplace(
            external_marketplace_id="finance:public",
            spec=DataMarketplaceSpec(
                marketplace=DataMarketplaceDefinition(
                    marketplaceId="finance:public",
                    contactName="Allie",
                    contactEmail="allie@example.com",
                    en=DataMarketplaceLanguage(name="Finance Marketplace"),
                )
            ),
            products=[
                DataProduct(
                    product_id="finance:last_quarter_sales",
                    version_id="1.0.0",
                    status="ready",
                )
            ],
            products_total=1,
        )

    def test_bulk_publish_info_generates_payload(self):
        payload = BulkPublishInfo(
            publish=[PublishInfo(product_id="new:product1", version_id="1.0.0")],
            update=[PublishInfo(product_id="existing:product", version_id="2.0.0")],
            unpublish=[PublishInfo(product_id="old:product")],
        ).generate_api_payload()

        assert payload == {
            "publish": [{"product_id": "new:product1", "version_id": "1.0.0"}],
            "update": [{"product_id": "existing:product", "version_id": "2.0.0"}],
            "unpublish": [{"product_id": "old:product"}],
        }

    def test_report_result_read_collects_extra_fields(self):
        product_result = ProductReportResultRead.from_api_response(
            {
                "report_key": "pii_found",
                "value": False,
                "extra_fields": {"severity": "low"},
            }
        )
        multi_result = ReportResultRead.from_api_response(
            {
                "product_id": "finance:last_quarter_sales",
                "report_key": "pii_found",
                "value": False,
                "severity": "low",
            }
        )

        assert product_result.extra_fields == {"severity": "low"}
        assert multi_result.extra_fields == {"severity": "low"}

    def test_permission_params_require_complete_pairs(self):
        with pytest.raises(InvalidPostBody):
            DataProductPermissionParams(subject_type="user").generate_params_dict()

        params = DataProductPermissionParams(
            subject_type="user",
            subject_id="42",
            object_type="data_product",
            object_id="finance:last_quarter_sales",
            role="product_viewer",
        )

        assert params.generate_params_dict() == {
            "subject_type": "user",
            "subject_id": "42",
            "object_type": "data_product",
            "object_id": "finance:last_quarter_sales",
            "role": "product_viewer",
        }

    def test_check_request_and_search_query_require_values(self):
        with pytest.raises(InvalidPostBody):
            DataProductCheck(product_spec=None, standards=[]).generate_api_payload()

        with pytest.raises(InvalidPostBody):
            DataProductSearchQuery(user_query=None).generate_api_payload()

    def test_version_update_and_permission_validate_allowed_values(self):
        with pytest.raises(InvalidPostBody):
            DataProductVersionUpdate(status="archived").generate_api_payload()

        with pytest.raises(InvalidPostBody):
            DataProductPermission(
                subject_type="team",
                subject_id="42",
                object_type="data_product",
                object_id="finance:last_quarter_sales",
                role="product_viewer",
            ).generate_api_payload()

        assert DataProductVersionUpdate(status="ready").generate_api_payload() == {"status": "ready"}
        assert DataProductParams(limit=25, offset=10, group_by_product=False).generate_params_dict() == {
            "limit": 25,
            "skip": 10,
            "group_by_product": False,
        }

    def test_check_request_generates_payload(self):
        check = DataProductCheck(
            product_spec=DataProductSpec(
                product=DataProductSpecDefinition(
                    productId="finance:last_quarter_sales",
                    version="1.0.0",
                    contactEmail="ann@example.com",
                    contactName="Ann",
                    en=DataProductDescription(name="Last Quarter Sales"),
                )
            ),
            standards=[
                DataProductCheckStandard(
                    type="static",
                    check="Has contact email",
                    key="product.contactEmail",
                )
            ],
        )

        assert check.generate_api_payload() == {
            "product_spec": {
                "product": {
                    "productId": "finance:last_quarter_sales",
                    "version": "1.0.0",
                    "contactEmail": "ann@example.com",
                    "contactName": "Ann",
                    "en": {"name": "Last Quarter Sales"},
                }
            },
            "standards": [
                {
                    "type": "static",
                    "check": "Has contact email",
                    "key": "product.contactEmail",
                }
            ],
        }
