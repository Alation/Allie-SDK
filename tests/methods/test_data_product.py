"""Tests for the Data Products API methods."""

import json

import pytest
import requests
from requests_mock import Mocker

import allie_sdk as allie
from allie_sdk.methods.data_product import AlationDataProduct
from allie_sdk.models.data_product_model import (
    DataMarketplace,
    DataMarketplaceDefinition,
    DataMarketplaceLanguage,
    DataMarketplaceParams,
    DataMarketplaceSpec,
    DataProductCheck,
    DataProductCheckStandard,
    DataProductDescription,
    DataProductParams,
    DataProductPermission,
    DataProductPermissionParams,
    DataProductPublishParams,
    DataProductRecordSet,
    DataProductRecordSetField,
    DataProductSearchQuery,
    DataProductSpec,
    DataProductSpecDefinition,
    DataProductVersionStatusUpdate,
    PublishedDataProductParams,
)
from allie_sdk.models.job_model import JobDetails


def build_data_product_spec() -> DataProductSpec:
    return DataProductSpec(
        product=DataProductSpecDefinition(
            productId="finance:last_quarter_sales",
            version="1.0.0",
            contactEmail="ann@example.com",
            contactName="Ann",
            en=DataProductDescription(
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
            json={
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "product_id": "finance:last_quarter_sales",
                        "version_id": "1.0.0",
                        "status": "draft",
                    }
                ],
            },
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
        assert request.headers["Authorization"] == "Bearer test-token"
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

        result = self.mock_data_product.update_data_product_version_status(
            "finance:last_quarter_sales",
            "1.0.0",
            DataProductVersionStatusUpdate(status="ready"),
        )

        assert result.status == "ready"
        assert json.loads(requests_mock.request_history[0].text) == {"status": "ready"}

    def test_get_and_delete_marketplace(self, requests_mock: Mocker) -> None:
        """Verify marketplace listing and deletion.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Assertions verify the returned models and query parameters.
        """
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
            method="DELETE",
            url="/dps/integration/data-products/v1/marketplace/finance:public/",
            text="",
            status_code=204,
        )

        marketplaces = self.mock_data_product.get_data_marketplaces(
            DataMarketplaceParams(limit=20, offset=0)
        )
        deleted = self.mock_data_product.delete_data_marketplace("finance:public")

        assert marketplaces[0].external_marketplace_id == "finance:public"
        assert deleted.status == "successful"
        assert requests_mock.request_history[0].qs["skip"] == ["0"]

    @pytest.mark.parametrize(
        "query_params",
        [None, DataMarketplaceParams(), DataMarketplaceParams(limit=20), DataMarketplaceParams(offset=0)],
    )
    def test_get_data_marketplaces_with_data_envelope(
        self, requests_mock: Mocker, query_params: DataMarketplaceParams | None
    ) -> None:
        """Verify marketplace envelopes are converted into a list of models.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            query_params (DataMarketplaceParams | None): Optional pagination bounds.

        Returns:
            None: Assertions verify marketplace details and request parameters.
        """
        marketplace_spec = build_marketplace_spec().generate_api_payload()
        specification_yaml = "marketplace:\n  marketplaceId: finance:public\n"
        requests_mock.get(
            "/dps/integration/data-products/v1/marketplace/",
            json={
                "data": [
                    {
                        "id": "bad823ca-e618-4b54-8a1a-c201c2aeb4e3",
                        "defaultMarketplaceTemplate": "mp-tpl-default",
                        "external_marketplace_id": "finance:public",
                        "products": [{"product_id": "finance:last_quarter_sales"}],
                        "products_total": 1,
                        "spec": marketplace_spec,
                        "spec_yaml": specification_yaml,
                    },
                    {"external_marketplace_id": "sales:public", "products": [], "products_total": 0},
                ],
                "total": 2,
            },
        )

        marketplaces = self.mock_data_product.get_data_marketplaces(query_params)

        assert len(marketplaces) == 2
        assert all(isinstance(marketplace, DataMarketplace) for marketplace in marketplaces)
        assert marketplaces[0].external_marketplace_id == "finance:public"
        assert marketplaces[0].spec.marketplace.en.name == "Finance Marketplace"
        assert marketplaces[0].spec_yaml == specification_yaml
        assert marketplaces[0].products[0].product_id == "finance:last_quarter_sales"
        assert marketplaces[0].products_total == 1
        assert marketplaces[1].external_marketplace_id == "sales:public"
        assert marketplaces[1].products == []
        assert requests_mock.call_count == 1
        request = requests_mock.request_history[0]
        assert request.headers["Authorization"] == "Bearer test-token"
        if query_params is not None and query_params.offset is not None:
            assert request.qs == {"skip": ["0"]}
        else:
            expected_limit = query_params.limit if query_params is not None and query_params.limit is not None else self.mock_data_product.page_size
            assert request.qs == {"limit": [str(expected_limit)]}

    def test_get_data_marketplaces_paginates_data_envelopes(self, requests_mock: Mocker) -> None:
        """Verify unbounded listings fetch all marketplaces using total and skip.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Assertions verify all pages are mapped and pagination advances.
        """
        requests_mock.get(
            "/dps/integration/data-products/v1/marketplace/",
            [
                {"json": {"data": [{"external_marketplace_id": "finance:public"}], "total": 2}},
                {"json": {"data": [{"external_marketplace_id": "sales:public"}], "total": 2}},
            ],
        )

        marketplaces = self.mock_data_product.get_data_marketplaces()

        assert [marketplace.external_marketplace_id for marketplace in marketplaces] == ["finance:public", "sales:public"]
        assert requests_mock.call_count == 2
        assert requests_mock.request_history[0].qs == {"limit": [str(self.mock_data_product.page_size)]}
        assert requests_mock.request_history[1].qs == {"limit": [str(self.mock_data_product.page_size)], "skip": ["1"]}

    def test_get_data_marketplaces_with_bounds_fetches_one_page(self, requests_mock: Mocker) -> None:
        """Verify explicit pagination bounds prevent automatic page requests.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Assertions verify only the requested page is fetched.
        """
        requests_mock.get(
            "/dps/integration/data-products/v1/marketplace/",
            json={"data": [{"external_marketplace_id": "finance:public"}], "total": 10},
        )

        marketplaces = self.mock_data_product.get_data_marketplaces(DataMarketplaceParams(limit=1, offset=5))

        assert marketplaces[0].external_marketplace_id == "finance:public"
        assert requests_mock.call_count == 1
        assert requests_mock.request_history[0].qs == {"limit": ["1"], "skip": ["5"]}

    def test_get_data_marketplaces_with_empty_data_envelope(self, requests_mock: Mocker) -> None:
        """Verify an empty marketplace envelope returns an empty list.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Assertions verify the empty result requires only one request.
        """
        requests_mock.get("/dps/integration/data-products/v1/marketplace/", json={"data": [], "total": 0})

        assert self.mock_data_product.get_data_marketplaces() == []
        assert requests_mock.call_count == 1

    @pytest.mark.parametrize(
        "response",
        [
            {},
            {"data": None, "total": 0},
            {"data": {}, "total": 0},
            {"data": ["finance:public"], "total": 1},
            {"data": [], "total": "0"},
            {"data": [], "total": False},
            {"data": [], "total": -1},
        ],
    )
    def test_get_data_marketplaces_rejects_invalid_responses(self, requests_mock: Mocker, response: dict[str, object]) -> None:
        """Verify malformed responses raise a clear validation error.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            response (dict[str, object]): Invalid marketplace response to return.

        Returns:
            None: Assertions verify malformed responses are rejected immediately.
        """
        requests_mock.get("/dps/integration/data-products/v1/marketplace/", json=response)

        with pytest.raises(ValueError, match="Marketplace response"):
            self.mock_data_product.get_data_marketplaces()

        assert requests_mock.call_count == 1

    @pytest.mark.parametrize(
        "second_page, expected_error",
        [
            ({"json": {"data": [], "total": 2}}, ValueError),
            ({"json": {"detail": "Forbidden"}, "status_code": 403}, requests.HTTPError),
        ],
    )
    def test_get_data_marketplaces_raises_on_incomplete_pagination(
        self, requests_mock: Mocker, second_page: dict[str, object], expected_error: type[Exception]
    ) -> None:
        """Verify failed pagination raises instead of returning incomplete data.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            second_page (dict[str, object]): Empty or failed second-page response.
            expected_error (type[Exception]): Error expected from the second page.

        Returns:
            None: Assertions verify errors propagate without further requests.
        """
        requests_mock.get(
            "/dps/integration/data-products/v1/marketplace/",
            [
                {"json": {"data": [{"external_marketplace_id": "finance:public"}], "total": 2}},
                second_page,
            ],
        )

        with pytest.raises(expected_error):
            self.mock_data_product.get_data_marketplaces()

        assert requests_mock.call_count == 2

    @pytest.mark.parametrize("payload_format", ["model", "dict", "yaml"])
    def test_create_data_marketplace_returns_message(self, requests_mock: Mocker, payload_format: str) -> None:
        """Verify marketplace creation returns the API message for each spec format.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            payload_format (str): Model, dictionary, or YAML request format.

        Returns:
            None: Assertions verify the success message and submitted specification.
        """
        message = "Marketplace with ID: finance:public successfully created."
        requests_mock.register_uri(
            method="POST",
            url="/dps/integration/data-products/v1/marketplace/",
            json={"message": message},
            status_code=201,
        )
        marketplace_spec: DataMarketplaceSpec | dict[str, object] | str = build_marketplace_spec()
        if payload_format == "dict":
            marketplace_spec = build_marketplace_spec().generate_api_payload()
        elif payload_format == "yaml":
            marketplace_spec = (
                "marketplace:\n"
                "  marketplaceId: finance:public\n"
                "  contactName: Allie\n"
                "  contactEmail: allie@example.com\n"
                "  en:\n"
                "    name: Finance Marketplace\n"
                "    description: Products for finance.\n"
            )

        result = self.mock_data_product.create_data_marketplace(marketplace_spec)

        assert result == JobDetails(status="successful", msg=message)
        request = requests_mock.request_history[0]
        if payload_format == "yaml":
            assert request.headers["Content-Type"] == "application/x-yaml; charset=utf-8"
            assert request.text == marketplace_spec
        else:
            assert json.loads(request.text) == build_marketplace_spec().generate_api_payload()

    def test_create_data_marketplace_with_empty_response(self, requests_mock: Mocker) -> None:
        """Verify marketplace creation handles an empty successful response.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: An assertion verifies the method returns None without a body.
        """
        requests_mock.register_uri(
            method="POST",
            url="/dps/integration/data-products/v1/marketplace/",
            text="",
            status_code=201,
        )

        assert self.mock_data_product.create_data_marketplace(build_marketplace_spec()) is None

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
        unpublished = self.mock_data_product.unpublish_data_product(
            "finance:public",
            "finance:last_quarter_sales",
        )

        assert published[0].product_id == "finance:last_quarter_sales"
        assert published_product.version_id == "1.0.0"
        assert unpublished.status == "successful"
        assert requests_mock.request_history[1].qs["version"] == ["1.0.0"]

    @pytest.mark.parametrize("version", [None, "2.0.0"])
    def test_update_published_data_product_returns_workflow_response(self, requests_mock: Mocker, version: str | None) -> None:
        """Verify publication updates preserve the approval message and workflow ID.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            version (str | None): Explicit version to publish, or None for the API default.

        Returns:
            None: Assertions verify the typed response and version query parameter.
        """
        workflow_request_id = "4459bebd-7f92-443d-b216-289148606301"
        message = (
            "Approval required to update product 'last-quarter-sales' in marketplace 'acme-market-2'. "
            f"Workflow request created with ID: {workflow_request_id}"
        )
        requests_mock.put(
            "/dps/integration/data-products/v1/marketplace/acme-market-2/data-product/last-quarter-sales/",
            json={"message": message, "workflow_request_id": workflow_request_id},
            status_code=200,
        )
        query_params = DataProductPublishParams(version=version) if version is not None else None

        result = self.mock_data_product.update_published_data_product(
            "acme-market-2",
            "last-quarter-sales",
            query_params,
        )

        assert result.message == message
        assert result.workflow_request_id == workflow_request_id
        assert isinstance(result, allie.DataProductPublicationResponse)
        assert requests_mock.call_count == 1
        request = requests_mock.request_history[0]
        assert request.qs == ({"version": [version]} if version is not None else {})
        assert json.loads(request.text) == {}

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
            json={
                "results": [
                    {
                        "product": {
                            "product_id": "finance:last_quarter_sales",
                            "version_id": "1.0.0",
                            "status": "ready",
                        },
                        "suggestion": "",
                    }
                ],
                "search_id": "13f1a755-f671-4bb4-abaa-4fb88b499c73",
            },
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
        assert search_results.results[0].product.product_id == "finance:last_quarter_sales"
        assert json.loads(requests_mock.request_history[1].text) == {
            "user_query": "Which products have recent sales information?"
        }

    def test_search_data_products_in_marketplace(self, requests_mock: Mocker) -> None:
        """Verify marketplace search returns typed matches and the search identifier.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Assertions verify the response wrapper and submitted query.
        """
        search_id = "13f1a755-f671-4bb4-abaa-4fb88b499c73"
        requests_mock.post(
            "/dps/integration/data-products/v1/search-internally/finance:public/",
            json={
                "results": [
                    {
                        "product": {
                            "product_id": "last-quarter-sales",
                            "version_id": "2.0.0",
                            "status": 1,
                            "marketplace_context": None,
                            "versions_details": None,
                        },
                        "suggestion": "",
                    },
                    {
                        "product": {"product_id": "annual-sales", "version_id": "1.0.0"},
                        "suggestion": "Consider annual sales for a longer time range.",
                    },
                ],
                "search_id": search_id,
            },
        )

        response = self.mock_data_product.search_data_products_in_marketplace(
            "finance:public",
            DataProductSearchQuery(user_query="Which products contain sales data?"),
        )

        assert isinstance(response, allie.DataProductSearchResponse)
        assert response.search_id == search_id
        assert len(response.results) == 2
        match = response.results[0]
        assert isinstance(match, allie.DataProductSearchResultItem)
        assert isinstance(match.product, allie.DataProductWithMarketplaceInfo)
        assert match.product.product_id == "last-quarter-sales"
        assert match.product.version_id == "2.0.0"
        assert match.product.marketplace_context is None
        assert match.suggestion == ""
        assert response.results[1].product.product_id == "annual-sales"
        assert response.results[1].suggestion == "Consider annual sales for a longer time range."
        assert requests_mock.call_count == 1
        request = requests_mock.request_history[0]
        assert request.headers["Authorization"] == "Bearer test-token"
        assert json.loads(request.text) == {"user_query": "Which products contain sales data?"}

    def test_search_data_products_in_marketplace_without_matches(self, requests_mock: Mocker) -> None:
        """Verify an empty results list retains the API search identifier.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Assertions verify the empty typed search response.
        """
        search_id = "13f1a755-f671-4bb4-abaa-4fb88b499c73"
        requests_mock.post(
            "/dps/integration/data-products/v1/search-internally/finance:public/",
            json={"results": [], "search_id": search_id},
        )

        response = self.mock_data_product.search_data_products_in_marketplace(
            "finance:public",
            DataProductSearchQuery(user_query="Products with no matches"),
        )

        assert isinstance(response, allie.DataProductSearchResponse)
        assert response.results == []
        assert response.search_id == search_id

    @pytest.mark.parametrize("response_body", [{}, {"results": None}, {"results": {}}, []])
    def test_search_data_products_in_marketplace_rejects_invalid_response(
        self, requests_mock: Mocker, response_body: dict[str, object] | list[object]
    ) -> None:
        """Verify malformed search responses raise an explicit error.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            response_body (dict[str, object] | list[object]): Invalid API response.

        Returns:
            None: An assertion verifies the response shape error.
        """
        requests_mock.post(
            "/dps/integration/data-products/v1/search-internally/finance:public/",
            json=response_body,
        )

        with pytest.raises(ValueError, match="containing a 'results' list"):
            self.mock_data_product.search_data_products_in_marketplace(
                "finance:public", DataProductSearchQuery(user_query="Sales data")
            )

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
