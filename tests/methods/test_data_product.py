"""Tests for the Data Products API methods."""

import json
from typing import Literal

import pytest
import requests
import yaml
from requests_mock import Mocker

import allie_sdk as allie
from allie_sdk.core.custom_exceptions import InvalidPostBody
from allie_sdk.methods.data_product import AlationDataProduct
from allie_sdk.models.data_product_model import (
    DataMarketplace,
    DataMarketplaceDefinition,
    DataMarketplaceLanguage,
    DataMarketplaceParams,
    DataMarketplaceSpec,
    DataProduct,
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

    def test_get_data_products(self, requests_mock: Mocker) -> None:
        """List products using the default Token header and requested filters.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Assertions verify product details, authentication, and query parameters.
        """
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
        assert request.headers["Token"] == "test-token"
        assert "Authorization" not in request.headers
        assert request.qs["limit"] == ["50"]
        assert request.qs["skip"] == ["5"]
        assert request.qs["product_ids"] == ["finance:last_quarter_sales"]
        assert request.qs["group_by_product"][0].lower() == "true"

    @pytest.mark.parametrize("explicit_format", [False, True])
    def test_get_data_product_returns_model(self, requests_mock: Mocker, explicit_format: bool) -> None:
        """Keep the default and explicit model output compatible with existing callers.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            explicit_format (bool): Whether to explicitly request model output.

        Returns:
            None: Assertions verify typed product details and an unchanged request.
        """
        requests_mock.get(
            "/dps/integration/data-products/v1/data-product/finance:last_quarter_sales/",
            json={
                "product_id": "finance:last_quarter_sales",
                "version_id": "1.0.0",
                "status": "draft",
                "spec_json": build_data_product_spec().generate_api_payload(),
            },
        )

        if explicit_format:
            result = self.mock_data_product.get_data_product("finance:last_quarter_sales", output_format="dataproduct")
        else:
            result = self.mock_data_product.get_data_product("finance:last_quarter_sales")

        assert isinstance(result, DataProduct)
        assert result.product_id == "finance:last_quarter_sales"
        assert result.version_id == "1.0.0"
        assert result.status == "draft"
        assert isinstance(result.spec_json, DataProductSpec)
        assert result.spec_json.product.en.name == "Last Quarter Sales"
        assert requests_mock.call_count == 1
        assert requests_mock.last_request.qs == {}

    def test_get_data_product_preserves_yaml(self, requests_mock: Mocker) -> None:
        """Return the original YAML specification without remapping its content.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Assertions verify YAML comments, formatting, and extensions survive.
        """
        specification_yaml = """# Sales specification
product:
  productId: 'finance:last_quarter_sales'
  version: "1.0.0"
  x-custom:
    label: "Ventes réalisées"
"""
        requests_mock.get(
            "/dps/integration/data-products/v1/data-product/finance:last_quarter_sales/",
            json={
                "product_id": "finance:last_quarter_sales",
                "spec_json": build_data_product_spec().generate_api_payload(),
                "spec_yaml": specification_yaml,
            },
        )

        result = self.mock_data_product.get_data_product("finance:last_quarter_sales", output_format="yaml")

        assert result == specification_yaml
        assert requests_mock.call_count == 1
        assert requests_mock.last_request.qs == {}

    @pytest.mark.parametrize("specification_yaml", [None, "", " \n"])
    def test_get_data_product_converts_json_to_yaml(self, requests_mock: Mocker, specification_yaml: str | None) -> None:
        """Serialize the raw JSON specification when the API supplies no usable YAML.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            specification_yaml (str | None): Empty YAML field returned by the API.

        Returns:
            None: Assertions verify specification values and extension fields survive.
        """
        specification_json = build_data_product_spec().generate_api_payload()
        specification_json["x-custom"] = {"enabled": True, "values": [None, 42, "001"]}
        specification_json["product"]["x-description"] = "Ventes réalisées"
        response_body = {"product_id": "finance:last_quarter_sales", "spec_json": specification_json}
        if specification_yaml is not None:
            response_body["spec_yaml"] = specification_yaml
        requests_mock.get(
            "/dps/integration/data-products/v1/data-product/finance:last_quarter_sales/",
            json=response_body,
        )

        result = self.mock_data_product.get_data_product("finance:last_quarter_sales", output_format="yaml")

        assert isinstance(result, str)
        assert yaml.safe_load(result) == specification_json
        assert "Ventes réalisées" in result

    @pytest.mark.parametrize("include_yaml", [False, True])
    def test_get_data_product_preserves_json(self, requests_mock: Mocker, include_yaml: bool) -> None:
        """Return the raw JSON specification with all custom fields and values.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            include_yaml (bool): Whether the API also returns a YAML specification.

        Returns:
            None: Assertions verify JSON output preserves extensions and value types.
        """
        specification_json = build_data_product_spec().generate_api_payload()
        specification_json["x-custom"] = {"enabled": True, "values": [None, 42, "001"]}
        specification_json["product"]["x-description"] = "Ventes réalisées"
        response_body = {"product_id": "finance:last_quarter_sales", "spec_json": specification_json}
        if include_yaml:
            response_body["spec_yaml"] = "product:\n  productId: different-product\n"
        requests_mock.get(
            "/dps/integration/data-products/v1/data-product/finance:last_quarter_sales/",
            json=response_body,
        )

        result = self.mock_data_product.get_data_product("finance:last_quarter_sales", output_format="json")

        assert isinstance(result, dict)
        assert result == specification_json
        assert json.loads(json.dumps(result)) == specification_json
        assert requests_mock.call_count == 1
        assert requests_mock.last_request.qs == {}

    @pytest.mark.parametrize(
        "response_body",
        [{}, {"spec_json": None}, {"spec_json": {}}, {"spec_json": []}, {"spec_yaml": "product: {}\n"}, []],
    )
    def test_get_data_product_json_requires_specification(self, requests_mock: Mocker, response_body: dict[str, object] | list[object]) -> None:
        """Reject JSON output when the API returns no non-empty JSON specification.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            response_body (dict[str, object] | list[object]): Response lacking a JSON specification.

        Returns:
            None: An assertion verifies a clear missing specification error.
        """
        requests_mock.get(
            "/dps/integration/data-products/v1/data-product/finance:last_quarter_sales/",
            json=response_body,
        )

        with pytest.raises(ValueError, match="did not include a non-empty 'spec_json'"):
            self.mock_data_product.get_data_product("finance:last_quarter_sales", output_format="json")

    @pytest.mark.parametrize("output_format", [None, "xml", ""])
    def test_get_data_product_rejects_invalid_output_format(self, requests_mock: Mocker, output_format: str | None) -> None:
        """Reject unsupported output formats before making an HTTP request.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            output_format (str | None): Unsupported output format to reject.

        Returns:
            None: Assertions verify a clear error and no network request.
        """
        with pytest.raises(ValueError, match="'output_format' must be 'dataproduct', 'yaml', or 'json'"):
            self.mock_data_product.get_data_product("finance:last_quarter_sales", output_format=output_format)

        assert not requests_mock.called

    @pytest.mark.parametrize(
        "response_body",
        [{}, {"spec_yaml": None}, {"spec_yaml": " \n", "spec_json": {}}, {"spec_yaml": 42, "spec_json": []}, []],
    )
    def test_get_data_product_yaml_requires_specification(self, requests_mock: Mocker, response_body: dict[str, object] | list[object]) -> None:
        """Raise when YAML output has no valid source specification.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            response_body (dict[str, object] | list[object]): Response lacking a usable specification.

        Returns:
            None: An assertion verifies an explicit missing specification error.
        """
        requests_mock.get(
            "/dps/integration/data-products/v1/data-product/finance:last_quarter_sales/",
            json=response_body,
        )

        with pytest.raises(ValueError, match="did not include a non-empty 'spec_yaml' or 'spec_json'"):
            self.mock_data_product.get_data_product("finance:last_quarter_sales", output_format="yaml")

    @pytest.mark.parametrize("output_format", ["dataproduct", "yaml", "json"])
    def test_get_data_product_propagates_http_errors(self, requests_mock: Mocker, output_format: str) -> None:
        """Preserve HTTP failures for model, YAML, and JSON output.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            output_format (str): Output format requested for the missing product.

        Returns:
            None: Assertions verify the API error propagates with its status code.
        """
        requests_mock.get(
            "/dps/integration/data-products/v1/data-product/finance:last_quarter_sales/",
            json={"message": "Product not found."},
            status_code=404,
        )

        with pytest.raises(requests.HTTPError) as error:
            self.mock_data_product.get_data_product("finance:last_quarter_sales", output_format=output_format)

        assert error.value.response.status_code == 404

    @pytest.mark.parametrize("output_format", [None, "dataproduct", "yaml", "json"])
    def test_get_data_product_version_output_formats(
        self, requests_mock: Mocker, output_format: Literal["dataproduct", "yaml", "json"] | None
    ) -> None:
        """Return the requested version in each format while preserving raw specifications.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            output_format (Literal["dataproduct", "yaml", "json"] | None): Requested format,
                or None to exercise the default call without an output argument.

        Returns:
            None: Assertions verify version selection, model details, and raw specifications.
        """
        specification_json = build_data_product_spec().generate_api_payload()
        specification_json["product"]["version"] = "2.0.0"
        specification_json["product"]["x-description"] = "Ventes réalisées"
        specification_json["x-custom"] = {"enabled": True, "values": [None, 42, "001"]}
        specification_yaml = "# Version specification\nproduct:\n  version: '2.0.0'\n  x-custom: true\n"
        requests_mock.get(
            "/dps/integration/data-products/v1/data-product/finance:last_quarter_sales/version/2.0.0/",
            json={
                "product_id": "finance:last_quarter_sales",
                "version_id": "2.0.0",
                "status": "ready",
                "spec_json": specification_json,
                "spec_yaml": specification_yaml,
            },
        )

        result: DataProduct | str | dict[str, object]
        if output_format is None:
            result = self.mock_data_product.get_data_product_version("finance:last_quarter_sales", "2.0.0")
        else:
            result = self.mock_data_product.get_data_product_version("finance:last_quarter_sales", "2.0.0", output_format=output_format)

        if output_format == "yaml":
            assert result == specification_yaml
        elif output_format == "json":
            assert isinstance(result, dict)
            assert result == specification_json
        else:
            assert isinstance(result, DataProduct)
            assert result.product_id == "finance:last_quarter_sales"
            assert result.version_id == "2.0.0"
            assert result.status == "ready"
            assert isinstance(result.spec_json, DataProductSpec)
            assert result.spec_json.product.version == "2.0.0"
        assert requests_mock.call_count == 1
        assert requests_mock.last_request.qs == {}

    @pytest.mark.parametrize("specification_yaml", [None, "", " \n"])
    def test_get_data_product_version_converts_json_to_yaml(self, requests_mock: Mocker, specification_yaml: str | None) -> None:
        """Convert the requested version's raw JSON specification when YAML is absent.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            specification_yaml (str | None): Missing or blank YAML returned by the API.

        Returns:
            None: Assertions verify JSON values and extension fields survive conversion.
        """
        specification_json = build_data_product_spec().generate_api_payload()
        specification_json["product"]["x-description"] = "Ventes réalisées"
        specification_json["x-custom"] = {"enabled": True, "values": [None, 42, "001"]}
        response_body: dict[str, object] = {"spec_json": specification_json}
        if specification_yaml is not None:
            response_body["spec_yaml"] = specification_yaml
        requests_mock.get(
            "/dps/integration/data-products/v1/data-product/finance:last_quarter_sales/version/1.0.0/",
            json=response_body,
        )

        result = self.mock_data_product.get_data_product_version("finance:last_quarter_sales", "1.0.0", output_format="yaml")

        assert yaml.safe_load(result) == specification_json
        assert "Ventes réalisées" in result

    @pytest.mark.parametrize("output_format", [None, "xml", ""])
    def test_get_data_product_version_rejects_invalid_output_format(self, requests_mock: Mocker, output_format: str | None) -> None:
        """Reject unsupported version output formats before requesting the product.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            output_format (str | None): Unsupported output format to reject.

        Returns:
            None: Assertions verify an explicit error and no network request.
        """
        with pytest.raises(ValueError, match="'output_format' must be 'dataproduct', 'yaml', or 'json'"):
            self.mock_data_product.get_data_product_version("finance:last_quarter_sales", "1.0.0", output_format=output_format)

        assert not requests_mock.called

    @pytest.mark.parametrize("output_format", ["yaml", "json"])
    def test_get_data_product_version_requires_specification(self, requests_mock: Mocker, output_format: Literal["yaml", "json"]) -> None:
        """Raise when a version response lacks the requested specification.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            output_format (Literal["yaml", "json"]): Specification format to request.

        Returns:
            None: An assertion verifies a clear missing specification error.
        """
        requests_mock.get(
            "/dps/integration/data-products/v1/data-product/finance:last_quarter_sales/version/1.0.0/",
            json={"product_id": "finance:last_quarter_sales", "version_id": "1.0.0"},
        )

        with pytest.raises(ValueError, match="did not include a non-empty"):
            self.mock_data_product.get_data_product_version("finance:last_quarter_sales", "1.0.0", output_format=output_format)

    @pytest.mark.parametrize("output_format", ["dataproduct", "yaml", "json"])
    def test_get_data_product_version_propagates_http_errors(self, requests_mock: Mocker, output_format: Literal["dataproduct", "yaml", "json"]) -> None:
        """Preserve HTTP failures for all version output formats.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            output_format (Literal["dataproduct", "yaml", "json"]): Requested output format.

        Returns:
            None: Assertions verify the HTTP status propagates to the caller.
        """
        requests_mock.get(
            "/dps/integration/data-products/v1/data-product/finance:last_quarter_sales/version/1.0.0/",
            json={"message": "Version not found."},
            status_code=404,
        )

        with pytest.raises(requests.HTTPError) as error:
            self.mock_data_product.get_data_product_version("finance:last_quarter_sales", "1.0.0", output_format=output_format)

        assert error.value.response.status_code == 404

    @pytest.mark.parametrize(
        ("product_id", "version_id", "missing_field"),
        [(None, "1.0.0", "product_id"), ("", "1.0.0", "product_id"), ("sales", None, "version_id"), ("sales", "", "version_id")],
    )
    def test_get_data_product_version_requires_identifiers(
        self, requests_mock: Mocker, product_id: str | None, version_id: str | None, missing_field: str
    ) -> None:
        """Keep identifier validation when requesting a version's specification.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            product_id (str | None): Product identifier supplied by the caller.
            version_id (str | None): Version identifier supplied by the caller.
            missing_field (str): Identifier expected in the validation error.

        Returns:
            None: Assertions verify missing identifiers fail before a network request.
        """
        with pytest.raises(InvalidPostBody, match=f"'{missing_field}' must be provided"):
            self.mock_data_product.get_data_product_version(product_id, version_id, output_format="yaml")

        assert not requests_mock.called

    def test_create_data_product_from_model(self, requests_mock: Mocker) -> None:
        """Create a product from a typed specification and preserve its response in a job.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Assertions verify the successful job, response payload, and sent specification.
        """
        response_body = {
            "product_id": "finance:last_quarter_sales",
            "version_id": "1.0.0",
            "status": "draft",
        }
        requests_mock.register_uri(
            method="POST",
            url="/dps/integration/data-products/v1/data-product/",
            json=response_body,
            status_code=201,
        )

        result = self.mock_data_product.create_data_product(build_data_product_spec())

        assert result == JobDetails(status="successful", msg="", result=response_body)
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

    @pytest.mark.parametrize(("product_status", "status_code"), [("ready", 201), ("draft", 200)])
    def test_update_data_product_version_status(self, requests_mock: Mocker, product_status: str, status_code: int) -> None:
        """Verify version status updates return a job containing the typed product.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            product_status (str): Product version status to request and return.
            status_code (int): Successful HTTP response status to exercise.

        Returns:
            None: Assertions verify operation status, product details, and payload.
        """
        requests_mock.register_uri(
            method="PUT",
            url="/dps/integration/data-products/v1/data-product/finance:last_quarter_sales/version/1.0.0/",
            json={
                "product_id": "finance:last_quarter_sales",
                "version_id": "1.0.0",
                "status": product_status,
                "spec_json": build_data_product_spec().generate_api_payload(),
            },
            status_code=status_code,
        )

        result = self.mock_data_product.update_data_product_version_status(
            "finance:last_quarter_sales",
            "1.0.0",
            DataProductVersionStatusUpdate(status=product_status),
        )

        assert isinstance(result, JobDetails)
        assert result.status == "successful"
        assert result.msg == ""
        assert isinstance(result.result, DataProduct)
        assert result.result.product_id == "finance:last_quarter_sales"
        assert result.result.version_id == "1.0.0"
        assert result.result.status == product_status
        assert isinstance(result.result.spec_json, DataProductSpec)
        assert result.result.spec_json.product.en.name == "Last Quarter Sales"
        assert json.loads(requests_mock.request_history[0].text) == {"status": product_status}

    def test_update_data_product_version_status_raises_http_error(self, requests_mock: Mocker) -> None:
        """Verify a rejected version update raises instead of returning a success job.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Assertions verify the API error propagates to the caller.
        """
        requests_mock.put(
            "/dps/integration/data-products/v1/data-product/finance:last_quarter_sales/version/1.0.0/",
            json={"message": "Permission denied."},
            status_code=403,
        )

        with pytest.raises(requests.HTTPError) as error:
            self.mock_data_product.update_data_product_version_status(
                "finance:last_quarter_sales",
                "1.0.0",
                DataProductVersionStatusUpdate(status="ready"),
            )

        assert error.value.response.status_code == 403

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
        assert request.headers["Token"] == "test-token"
        assert "Authorization" not in request.headers
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

    @pytest.mark.parametrize("payload_format", ["model", "dict", "yaml"])
    def test_update_data_marketplace_returns_job(self, requests_mock: Mocker, payload_format: str) -> None:
        """Verify marketplace updates return a job containing typed marketplace details.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            payload_format (str): Model, dictionary, or YAML request format.

        Returns:
            None: Assertions verify operation status, nested models, and the request.
        """
        specification = build_marketplace_spec()
        specification_yaml = "marketplace:\n  marketplaceId: finance:public\n"
        requests_mock.put(
            "/dps/integration/data-products/v1/marketplace/",
            json={
                "external_marketplace_id": "finance:public",
                "name": "Finance Marketplace",
                "spec": specification.generate_api_payload(),
                "spec_yaml": specification_yaml,
                "products": [{"product_id": "finance:last_quarter_sales", "version_id": "1.0.0"}],
                "products_total": 1,
            },
            status_code=200,
        )
        marketplace_spec: DataMarketplaceSpec | dict[str, object] | str = specification
        if payload_format == "dict":
            marketplace_spec = specification.generate_api_payload()
        elif payload_format == "yaml":
            marketplace_spec = specification_yaml

        result = self.mock_data_product.update_data_marketplace(marketplace_spec)

        assert isinstance(result, JobDetails)
        assert result.status == "successful"
        assert result.msg == ""
        assert isinstance(result.result, DataMarketplace)
        assert result.result.external_marketplace_id == "finance:public"
        assert result.result.name == "Finance Marketplace"
        assert isinstance(result.result.spec, DataMarketplaceSpec)
        assert result.result.spec.marketplace.en.name == "Finance Marketplace"
        assert result.result.spec_yaml == specification_yaml
        assert isinstance(result.result.products[0], DataProduct)
        assert result.result.products[0].product_id == "finance:last_quarter_sales"
        assert result.result.products_total == 1
        request = requests_mock.request_history[0]
        if payload_format == "yaml":
            assert request.headers["Content-Type"] == "application/x-yaml; charset=utf-8"
            assert request.text == specification_yaml
        else:
            assert json.loads(request.text) == specification.generate_api_payload()

    def test_update_data_marketplace_raises_http_error(self, requests_mock: Mocker) -> None:
        """Verify a rejected marketplace update raises an HTTP error.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Assertions verify the API error propagates to the caller.
        """
        requests_mock.put(
            "/dps/integration/data-products/v1/marketplace/",
            json={"message": "Permission denied."},
            status_code=403,
        )

        with pytest.raises(requests.HTTPError) as error:
            self.mock_data_product.update_data_marketplace(build_marketplace_spec())

        assert error.value.response.status_code == 403

    def test_get_published_marketplace_products(self, requests_mock: Mocker) -> None:
        """Verify published products are returned as product models.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Assertions verify the published product identifier.
        """
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
        published = self.mock_data_product.get_published_data_products(
            "finance:public",
            PublishedDataProductParams(limit=10, offset=0),
        )
        assert published[0].product_id == "finance:last_quarter_sales"

    @pytest.mark.parametrize(
        ("method_name", "http_method", "version"),
        [
            ("publish_data_product", "POST", None),
            ("publish_data_product", "POST", "2.0.0"),
            ("update_published_data_product", "PUT", None),
            ("update_published_data_product", "PUT", "2.0.0"),
            ("unpublish_data_product", "DELETE", None),
        ],
    )
    def test_publication_methods_return_job_details(self, requests_mock: Mocker, method_name: str, http_method: str, version: str | None) -> None:
        """Verify publication jobs preserve the approval message and workflow ID.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            method_name (str): SDK publication method to exercise.
            http_method (str): HTTP method expected for the publication request.
            version (str | None): Explicit version to publish, or None for the API default.

        Returns:
            None: Assertions verify the typed response and version query parameter.
        """
        workflow_request_id = "4459bebd-7f92-443d-b216-289148606301"
        message = f"Approval required to update product 'last-quarter-sales' in marketplace 'acme-market-2'. Workflow request created with ID: {workflow_request_id}"
        requests_mock.register_uri(
            http_method,
            "/dps/integration/data-products/v1/marketplace/acme-market-2/data-product/last-quarter-sales/",
            json={"message": message, "workflow_request_id": workflow_request_id},
            status_code=200,
        )
        query_params = DataProductPublishParams(version=version) if version is not None else None

        publication_method = getattr(self.mock_data_product, method_name)
        if http_method == "DELETE":
            result = publication_method("acme-market-2", "last-quarter-sales")
        else:
            result = publication_method("acme-market-2", "last-quarter-sales", query_params)

        assert isinstance(result, JobDetails)
        assert result.status == "successful"
        assert result.msg == ""
        assert isinstance(result.result, allie.DataProductPublicationResponse)
        assert result.result.message == message
        assert result.result.workflow_request_id == workflow_request_id
        assert requests_mock.call_count == 1
        request = requests_mock.request_history[0]
        assert request.qs == ({"version": [version]} if version is not None else {})
        if http_method != "DELETE":
            assert json.loads(request.text) == {}

    @pytest.mark.parametrize(
        ("method_name", "http_method"),
        [
            ("publish_data_product", "POST"),
            ("update_published_data_product", "PUT"),
            ("unpublish_data_product", "DELETE"),
        ],
    )
    @pytest.mark.parametrize("message", [None, "Publication request accepted."])
    def test_publication_methods_handle_missing_workflow_id(self, requests_mock: Mocker, method_name: str, http_method: str, message: str | None) -> None:
        """Verify message-only and empty responses still yield typed job results.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            method_name (str): SDK publication method to exercise.
            http_method (str): HTTP method expected for the publication request.
            message (str | None): Message-only payload, or None for an empty body.

        Returns:
            None: Assertions verify optional approval fields in the typed result.
        """
        response_options = {"text": "", "status_code": 204} if message is None else {"json": {"message": message}, "status_code": 200}
        requests_mock.register_uri(
            http_method,
            "/dps/integration/data-products/v1/marketplace/acme-market-2/data-product/last-quarter-sales/",
            **response_options,
        )

        result = getattr(self.mock_data_product, method_name)("acme-market-2", "last-quarter-sales")

        assert isinstance(result, JobDetails)
        assert result.status == "successful"
        assert isinstance(result.result, allie.DataProductPublicationResponse)
        assert result.result.message == message
        assert result.result.workflow_request_id is None

    @pytest.mark.parametrize(
        ("method_name", "http_method"),
        [
            ("publish_data_product", "POST"),
            ("update_published_data_product", "PUT"),
            ("unpublish_data_product", "DELETE"),
        ],
    )
    def test_publication_methods_raise_http_errors(self, requests_mock: Mocker, method_name: str, http_method: str) -> None:
        """Verify rejected publication requests propagate the HTTP error.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            method_name (str): SDK publication method to exercise.
            http_method (str): HTTP method expected for the publication request.

        Returns:
            None: Assertions verify no success job is returned for a rejected request.
        """
        requests_mock.register_uri(
            http_method,
            "/dps/integration/data-products/v1/marketplace/acme-market-2/data-product/last-quarter-sales/",
            json={"message": "Permission denied."},
            status_code=403,
        )

        with pytest.raises(requests.HTTPError) as error:
            getattr(self.mock_data_product, method_name)("acme-market-2", "last-quarter-sales")

        assert error.value.response.status_code == 403

    @pytest.mark.parametrize(
        ("method_name", "http_method"),
        [
            ("publish_data_product", "POST"),
            ("update_published_data_product", "PUT"),
            ("unpublish_data_product", "DELETE"),
        ],
    )
    def test_publication_methods_reject_invalid_response(self, requests_mock: Mocker, method_name: str, http_method: str) -> None:
        """Verify invalid publication payloads fail instead of losing response data.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.
            method_name (str): SDK publication method to exercise.
            http_method (str): HTTP method expected for the publication request.

        Returns:
            None: Assertions verify an unexpected response type raises ValueError.
        """
        requests_mock.register_uri(
            http_method,
            "/dps/integration/data-products/v1/marketplace/acme-market-2/data-product/last-quarter-sales/",
            json=[{"message": "Unexpected list response."}],
            status_code=200,
        )

        with pytest.raises(ValueError, match="publication responses must be an object or empty"):
            getattr(self.mock_data_product, method_name)("acme-market-2", "last-quarter-sales")

    def test_check_and_search_data_products(self, requests_mock: Mocker) -> None:
        """Parse the standards evaluation envelope and search for matching products.

        Args:
            requests_mock (Mocker): Fixture intercepting HTTP requests.

        Returns:
            None: Assertions verify the evaluation outcome, search matches, and search payload.
        """
        requests_mock.register_uri(
            method="POST",
            url="/dps/integration/data-products/v1/data-product-check/",
            json={
                "evaluations": [
                    {
                        "key": "product.contactEmail",
                        "check": "Has contact email",
                        "type": "static",
                        "passed": True,
                        "explanation": "Found contact email.",
                    }
                ]
            },
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
        assert request.headers["Token"] == "test-token"
        assert "Authorization" not in request.headers
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
