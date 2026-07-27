"""Tests for the Data Products API methods."""

import json

import requests

from allie_sdk.methods.data_product import AlationDataProduct
from allie_sdk.models.data_product_model import (
    BulkPublishInfo,
    DataMarketplaceParams,
    DataMarketplaceSpec,
    DataMarketplaceDefinition,
    DataMarketplaceLanguage,
    DataProductCheck,
    DataProductCheckStandard,
    DataProductLanguage,
    DataProductParams,
    DataProductPermission,
    DataProductPermissionParams,
    DataProductPublishParams,
    DataProductRecordSet,
    DataProductRecordSetField,
    DataProductSearchQuery,
    DataProductSpec,
    DataProductSpecDefinition,
    DataProductVersionUpdate,
    ProductReportResult,
    ProductReportResultRead,
    PublishInfo,
    PublishedDataProductParams,
    ReportResult,
    ReportResultsParams,
)


def build_data_product_spec() -> DataProductSpec:
    return DataProductSpec(
        product=DataProductSpecDefinition(
            productId="finance:last_quarter_sales",
            version="1.0.0",
            contactEmail="ann@example.com",
            contactName="Ann",
            en=DataProductLanguage(
                name="Last Quarter Sales",
                description="Data about last quarter sales",
            ),
            recordSets={
                "sales": DataProductRecordSet(
                    name="sales",
                    schema=[
                        DataProductRecordSetField(
                            name="month",
                            type="date",
                        )
                    ],
                )
            },
        )
    )


def build_marketplace_spec() -> DataMarketplaceSpec:
    return DataMarketplaceSpec(
        marketplace=DataMarketplaceDefinition(
            marketplaceId="finance:public",
            contactName="Allie",
            contactEmail="allie@example.com",
            en=DataMarketplaceLanguage(
                name="Finance Marketplace",
                description="Products for finance.",
            ),
        )
    )


def build_permission() -> DataProductPermission:
    return DataProductPermission(
        subject_type="user",
        subject_id="42",
        object_type="data_product",
        object_id="finance:last_quarter_sales",
        role="product_viewer",
    )


class TestDataProductMethods:
    def setup_method(self):
        self.mock_data_product = AlationDataProduct(
            access_token="test-token",
            session=requests.session(),
            host="https://test.com",
        )

    def test_get_data_products(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/dps/integration/data-products/v1/data-product/",
            json=[
                {
                    "product_id": "finance:last_quarter_sales",
                    "version_id": "1.0.0",
                    "status": "draft",
                }
            ],
            status_code=200,
        )

        result = self.mock_data_product.get_data_products(
            DataProductParams(
                limit=50,
                offset=5,
                product_ids=["finance:last_quarter_sales"],
                group_by_product=True,
            )
        )

        assert result[0].product_id == "finance:last_quarter_sales"
        request = requests_mock.request_history[0]
        assert request.headers["Token"] == "test-token"
        assert request.qs["limit"] == ["50"]
        assert request.qs["skip"] == ["5"]
        assert request.qs["product_ids"] == ["finance:last_quarter_sales"]
        assert request.qs["group_by_product"][0].lower() == "true"

    def test_create_data_product_from_model(self, requests_mock):
        requests_mock.register_uri(
            method="POST",
            url="/dps/integration/data-products/v1/data-product/",
            json={
                "product_id": "finance:last_quarter_sales",
                "version_id": "1.0.0",
                "status": "draft",
            },
            status_code=201,
        )

        result = self.mock_data_product.create_data_product(build_data_product_spec())

        assert result.product_id == "finance:last_quarter_sales"
        request = requests_mock.request_history[0]
        payload = json.loads(request.text)
        assert payload["product"]["productId"] == "finance:last_quarter_sales"
        assert payload["product"]["recordSets"]["sales"]["schema"][0]["name"] == "month"

    def test_create_data_product_from_yaml_string(self, requests_mock):
        requests_mock.register_uri(
            method="POST",
            url="/dps/integration/data-products/v1/data-product/",
            json={
                "product_id": "finance:last_quarter_sales",
                "version_id": "1.0.0",
                "status": "draft",
            },
            status_code=201,
        )

        yaml_payload = "product:\n  productId: finance:last_quarter_sales\n  version: 1.0.0\n"
        self.mock_data_product.create_data_product(yaml_payload)

        request = requests_mock.request_history[0]
        assert request.headers["Content-Type"] == "application/x-yaml; charset=utf-8"
        assert request.text == yaml_payload

    def test_update_data_product_version(self, requests_mock):
        requests_mock.register_uri(
            method="PUT",
            url="/dps/integration/data-products/v1/data-product/finance:last_quarter_sales/version/1.0.0/",
            json={
                "product_id": "finance:last_quarter_sales",
                "version_id": "1.0.0",
                "status": "ready",
            },
            status_code=201,
        )

        result = self.mock_data_product.update_data_product_version(
            "finance:last_quarter_sales",
            "1.0.0",
            DataProductVersionUpdate(status="ready"),
        )

        assert result.status == "ready"
        assert json.loads(requests_mock.request_history[0].text) == {"status": "ready"}

    def test_get_and_log_data_product_report_results(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/dps/integration/data-products/v1/data-product/finance:last_quarter_sales/report-results/",
            json=[
                {
                    "report_key": "pii_found",
                    "value": False,
                    "extra_fields": {"severity": "low"},
                }
            ],
            status_code=200,
        )
        requests_mock.register_uri(
            method="POST",
            url="/dps/integration/data-products/v1/data-product/finance:last_quarter_sales/report-results/",
            text="",
            status_code=201,
        )

        results = self.mock_data_product.get_data_product_report_results(
            "finance:last_quarter_sales",
            query_params=None,
        )
        job = self.mock_data_product.log_data_product_report_results(
            "finance:last_quarter_sales",
            [
                ProductReportResult(
                    report_key="pii_found",
                    value=False,
                    extra_fields={"severity": "low"},
                )
            ],
        )

        assert results == [
            ProductReportResultRead(
                report_key="pii_found",
                value=False,
                extra_fields={"severity": "low"},
            )
        ]
        assert job.status == "successful"
        assert json.loads(requests_mock.request_history[1].text) == [
            {
                "report_key": "pii_found",
                "value": False,
                "severity": "low",
            }
        ]

    def test_get_create_and_delete_marketplace(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/dps/integration/data-products/v1/marketplace/",
            json=[
                {
                    "external_marketplace_id": "finance:public",
                    "products_total": 1,
                }
            ],
            status_code=200,
        )
        requests_mock.register_uri(
            method="POST",
            url="/dps/integration/data-products/v1/marketplace/",
            json={
                "external_marketplace_id": "finance:public",
                "products_total": 0,
            },
            status_code=201,
        )
        requests_mock.register_uri(
            method="DELETE",
            url="/dps/integration/data-products/v1/marketplace/finance:public/",
            text="",
            status_code=204,
        )

        marketplaces = self.mock_data_product.get_data_marketplaces(
            DataMarketplaceParams(limit=20, offset=0)
        )
        created = self.mock_data_product.create_data_marketplace(build_marketplace_spec())
        deleted = self.mock_data_product.delete_data_marketplace("finance:public")

        assert marketplaces[0].external_marketplace_id == "finance:public"
        assert created.external_marketplace_id == "finance:public"
        assert deleted.status == "successful"
        assert requests_mock.request_history[0].qs["skip"] == ["0"]
        assert json.loads(requests_mock.request_history[1].text)["marketplace"]["marketplaceId"] == "finance:public"

    def test_get_and_publish_marketplace_products(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/dps/integration/data-products/v1/marketplace/finance:public/data-product/",
            json=[
                {
                    "product_id": "finance:last_quarter_sales",
                    "version_id": "1.0.0",
                    "status": "ready",
                }
            ],
            status_code=200,
        )
        requests_mock.register_uri(
            method="POST",
            url="/dps/integration/data-products/v1/marketplace/finance:public/data-product/finance:last_quarter_sales/",
            json={
                "product_id": "finance:last_quarter_sales",
                "version_id": "1.0.0",
                "status": "ready",
            },
            status_code=200,
        )
        requests_mock.register_uri(
            method="PUT",
            url="/dps/integration/data-products/v1/marketplace/finance:public/data-product/finance:last_quarter_sales/",
            json={
                "product_id": "finance:last_quarter_sales",
                "version_id": "2.0.0",
                "status": "ready",
            },
            status_code=200,
        )
        requests_mock.register_uri(
            method="DELETE",
            url="/dps/integration/data-products/v1/marketplace/finance:public/data-product/finance:last_quarter_sales/",
            text="",
            status_code=204,
        )

        published = self.mock_data_product.get_published_data_products(
            "finance:public",
            PublishedDataProductParams(limit=10, offset=0),
        )
        published_product = self.mock_data_product.publish_data_product(
            "finance:public",
            "finance:last_quarter_sales",
            DataProductPublishParams(version="1.0.0"),
        )
        updated_product = self.mock_data_product.update_published_data_product(
            "finance:public",
            "finance:last_quarter_sales",
            DataProductPublishParams(version="2.0.0"),
        )
        unpublished = self.mock_data_product.unpublish_data_product(
            "finance:public",
            "finance:last_quarter_sales",
        )

        assert published[0].product_id == "finance:last_quarter_sales"
        assert published_product.version_id == "1.0.0"
        assert updated_product.version_id == "2.0.0"
        assert unpublished.status == "successful"
        assert requests_mock.request_history[1].qs["version"] == ["1.0.0"]
        assert requests_mock.request_history[2].qs["version"] == ["2.0.0"]

    def test_bulk_publish_data_products(self, requests_mock):
        requests_mock.register_uri(
            method="POST",
            url="/dps/integration/data-products/v1/marketplace/finance:public/bulk-publish/",
            json=[
                {
                    "product_id": "finance:last_quarter_sales",
                    "version_id": "1.0.0",
                    "status": "ready",
                }
            ],
            status_code=200,
        )

        result = self.mock_data_product.bulk_publish_data_products(
            "finance:public",
            BulkPublishInfo(
                publish=[PublishInfo(product_id="finance:last_quarter_sales", version_id="1.0.0")]
            ),
        )

        assert result[0].product_id == "finance:last_quarter_sales"
        assert json.loads(requests_mock.request_history[0].text) == {
            "publish": [{"product_id": "finance:last_quarter_sales", "version_id": "1.0.0"}]
        }

    def test_check_and_search_data_products(self, requests_mock):
        requests_mock.register_uri(
            method="POST",
            url="/dps/integration/data-products/v1/data-product-check/",
            json=[
                {
                    "key": "product.contactEmail",
                    "check": "Has contact email",
                    "type": "static",
                    "passed": True,
                    "explanation": "Found contact email.",
                }
            ],
            status_code=200,
        )
        requests_mock.register_uri(
            method="POST",
            url="/dps/integration/data-products/v1/search-internally/finance:public/",
            json=[
                {
                    "product_id": "finance:last_quarter_sales",
                    "version_id": "1.0.0",
                    "status": "ready",
                }
            ],
            status_code=200,
        )

        check_results = self.mock_data_product.check_data_product(
            DataProductCheck(
                product_spec=build_data_product_spec(),
                standards=[
                    DataProductCheckStandard(
                        type="static",
                        check="Has contact email",
                        key="product.contactEmail",
                    )
                ],
            )
        )
        search_results = self.mock_data_product.search_data_products_in_marketplace(
            "finance:public",
            DataProductSearchQuery(user_query="Which products have recent sales information?"),
        )

        assert check_results[0].passed is True
        assert search_results[0].product_id == "finance:last_quarter_sales"
        assert json.loads(requests_mock.request_history[1].text) == {
            "user_query": "Which products have recent sales information?"
        }

    def test_get_and_log_global_report_results(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/dps/integration/data-products/v1/report-results/",
            json=[
                {
                    "product_id": "finance:last_quarter_sales",
                    "report_key": "pii_found",
                    "value": False,
                    "extra_fields": {"severity": "low"},
                }
            ],
            status_code=200,
        )
        requests_mock.register_uri(
            method="POST",
            url="/dps/integration/data-products/v1/report-results/",
            text="",
            status_code=201,
        )

        results = self.mock_data_product.get_report_results(
            ReportResultsParams(
                product_id="finance:last_quarter_sales",
                report_key="pii_found",
            )
        )
        job = self.mock_data_product.log_report_results(
            [
                ReportResult(
                    product_id="finance:last_quarter_sales",
                    report_key="pii_found",
                    value=False,
                    extra_fields={"severity": "low"},
                )
            ]
        )

        assert results[0].product_id == "finance:last_quarter_sales"
        assert results[0].extra_fields == {"severity": "low"}
        assert job.status == "successful"
        assert requests_mock.request_history[0].qs["product_id"] == ["finance:last_quarter_sales"]
        assert json.loads(requests_mock.request_history[1].text) == [
            {
                "report_key": "pii_found",
                "value": False,
                "severity": "low",
                "product_id": "finance:last_quarter_sales",
            }
        ]

    def test_permission_endpoints(self, requests_mock):
        requests_mock.register_uri(
            method="GET",
            url="/dps/integration/data-products/v1/data-products/permissions/",
            json=[
                {
                    "subject_type": "user",
                    "subject_id": "42",
                    "object_type": "data_product",
                    "object_id": "finance:last_quarter_sales",
                    "role": "product_viewer",
                }
            ],
            status_code=200,
        )
        requests_mock.register_uri(
            method="POST",
            url="/dps/integration/data-products/v1/data-products/permissions/",
            text="",
            status_code=201,
        )
        requests_mock.register_uri(
            method="PUT",
            url="/dps/integration/data-products/v1/data-products/permissions/",
            text="",
            status_code=200,
        )
        requests_mock.register_uri(
            method="DELETE",
            url="/dps/integration/data-products/v1/data-products/permissions/",
            text="",
            status_code=204,
        )
        requests_mock.register_uri(
            method="GET",
            url="/dps/integration/data-products/v1/data-products/check-permissions/",
            json=[
                {
                    "subject_type": "everyone",
                    "subject_id": "everyone",
                    "object_type": "app",
                    "object_id": "data_products",
                    "role": "app_viewer",
                }
            ],
            status_code=200,
        )

        permissions = self.mock_data_product.get_permissions(
            DataProductPermissionParams(
                subject_type="user",
                subject_id="42",
                object_type="data_product",
                object_id="finance:last_quarter_sales",
                role="product_viewer",
            )
        )
        created = self.mock_data_product.create_permission(build_permission())
        updated = self.mock_data_product.update_permission(build_permission())
        deleted = self.mock_data_product.delete_permission(build_permission())
        current_user_permissions = self.mock_data_product.get_user_permissions()

        assert permissions[0].role == "product_viewer"
        assert created.status == "successful"
        assert updated.status == "successful"
        assert deleted.status == "successful"
        assert current_user_permissions[0].role == "app_viewer"
        assert requests_mock.request_history[0].qs["role"] == ["product_viewer"]
        assert json.loads(requests_mock.request_history[1].text)["subject_id"] == "42"
