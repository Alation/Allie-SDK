"""Alation Data Products API methods."""

import logging
from typing import Any

import requests

from ..core.custom_exceptions import (
    InvalidPostBody,
    UnsupportedPostBody,
    validate_query_params,
    validate_rest_payload,
)
from ..core.request_handler import RequestHandler
from ..models.data_product_model import (
    BulkPublishInfo,
    DataMarketplace,
    DataMarketplaceParams,
    DataMarketplaceSpec,
    DataProduct,
    DataProductCheck,
    DataProductCheckResultItem,
    DataProductParams,
    DataProductPermission,
    DataProductPermissionParams,
    DataProductPublishParams,
    DataProductReportResultsParams,
    DataProductSearchQuery,
    DataProductSpec,
    DataProductVersionUpdate,
    DataProductWithMarketplaceInfo,
    ProductReportResult,
    ProductReportResultRead,
    PublishedDataProductParams,
    ReportResult,
    ReportResultRead,
    ReportResultsParams,
)
from ..models.job_model import JobDetails

LOGGER = logging.getLogger("allie_sdk_logger")


class AlationDataProduct(RequestHandler):
    """Interact with the Alation Data Products API endpoints."""

    def __init__(self, access_token: str, session: requests.Session, host: str):
        """Create an instance of the Data Products methods wrapper."""

        super().__init__(session=session, host=host, access_token=access_token)

    @staticmethod
    def _validate_identifier(value: str, field_name: str):
        """Validate required string identifiers used in path parameters."""

        if value is None or value == "":
            raise InvalidPostBody(f"'{field_name}' must be provided for the Data Products request.")

    @staticmethod
    def _prepare_spec_payload(
        spec_payload: DataProductSpec | DataMarketplaceSpec | dict[str, Any] | str,
        expected_type: type[DataProductSpec] | type[DataMarketplaceSpec],
        payload_name: str,
    ) -> tuple[dict[str, Any] | str, dict[str, str] | None]:
        """Normalize JSON or YAML spec payloads for create and update requests."""

        if spec_payload is None:
            raise InvalidPostBody(f"'{payload_name}' is required for the Data Products request.")

        if isinstance(spec_payload, str):
            return spec_payload, {"Content-Type": "application/x-yaml; charset=utf-8"}

        if isinstance(spec_payload, dict):
            spec_payload = expected_type.from_api_response(spec_payload)

        if not isinstance(spec_payload, expected_type):
            raise UnsupportedPostBody(
                f"Unsupported type '{type(spec_payload)}' was passed for API Body Payload\n"
                f"Please use:\n - {'.'.join((expected_type.__module__, expected_type.__qualname__))}\n"
                " - dict\n - str"
            )

        validate_rest_payload(payload=[spec_payload], expected_types=(expected_type,))
        return spec_payload.generate_api_payload(), None

    @staticmethod
    def _paginate_when_unbounded(query_params: DataProductParams | DataMarketplaceParams | PublishedDataProductParams | None) -> bool:
        """Only auto-paginate when the caller did not request explicit pagination bounds."""

        if query_params is None:
            return True
        return getattr(query_params, "limit", None) is None and getattr(query_params, "offset", None) is None

    def get_data_products(
        self,
        query_params: DataProductParams = None,
    ) -> list[DataProduct]:
        """Retrieve data products."""

        validate_query_params(query_params, DataProductParams)
        params = query_params.generate_params_dict() if query_params else None
        paginate = self._paginate_when_unbounded(query_params)

        LOGGER.info("Fetching data products.")
        response = self.get(
            url="/dps/integration/data-products/v1/data-product/",
            query_params=params,
            pagination=paginate,
        )

        if response:
            return [DataProduct.from_api_response(item) for item in response]
        return []

    def create_data_product(
        self,
        data_product_spec: DataProductSpec | dict[str, Any] | str,
    ) -> DataProduct:
        """Create a data product from a typed spec, raw dict, or YAML string."""

        payload, headers = self._prepare_spec_payload(
            spec_payload=data_product_spec,
            expected_type=DataProductSpec,
            payload_name="data_product_spec",
        )

        LOGGER.info("Creating a data product.")
        response = self.post(
            url="/dps/integration/data-products/v1/data-product/",
            body=payload,
            headers=headers,
        )
        return DataProduct.from_api_response(response)

    def update_data_product(
        self,
        data_product_spec: DataProductSpec | dict[str, Any] | str,
    ) -> DataProduct:
        """Update a data product from a typed spec, raw dict, or YAML string."""

        payload, headers = self._prepare_spec_payload(
            spec_payload=data_product_spec,
            expected_type=DataProductSpec,
            payload_name="data_product_spec",
        )

        LOGGER.info("Updating a data product.")
        response = self.put(
            url="/dps/integration/data-products/v1/data-product/",
            body=payload,
            headers=headers,
        )
        return DataProduct.from_api_response(response)

    def get_data_product(self, product_id: str) -> DataProduct:
        """Retrieve a single data product."""

        self._validate_identifier(product_id, "product_id")

        LOGGER.info("Fetching data product '%s'.", product_id)
        response = self.get(
            url=f"/dps/integration/data-products/v1/data-product/{product_id}/",
            pagination=False,
        )
        return DataProduct.from_api_response(response)

    def delete_data_product(self, product_id: str) -> JobDetails:
        """Delete a single data product."""

        self._validate_identifier(product_id, "product_id")

        LOGGER.info("Deleting data product '%s'.", product_id)
        response = self.delete(
            url=f"/dps/integration/data-products/v1/data-product/{product_id}/",
        )
        return JobDetails.from_api_response(response)

    def get_data_product_version(self, product_id: str, version_id: str) -> DataProduct:
        """Retrieve a specific data product version."""

        self._validate_identifier(product_id, "product_id")
        self._validate_identifier(version_id, "version_id")

        LOGGER.info("Fetching data product '%s' version '%s'.", product_id, version_id)
        response = self.get(
            url=f"/dps/integration/data-products/v1/data-product/{product_id}/version/{version_id}/",
            pagination=False,
        )
        return DataProduct.from_api_response(response)

    def update_data_product_version(
        self,
        product_id: str,
        version_id: str,
        data_product_version: DataProductVersionUpdate,
    ) -> DataProduct:
        """Update a specific data product version status."""

        self._validate_identifier(product_id, "product_id")
        self._validate_identifier(version_id, "version_id")
        if data_product_version is None:
            raise InvalidPostBody("'data_product_version' is required for the Data Products request.")

        validate_rest_payload(payload=[data_product_version], expected_types=(DataProductVersionUpdate,))
        payload = data_product_version.generate_api_payload()

        LOGGER.info("Updating data product '%s' version '%s'.", product_id, version_id)
        response = self.put(
            url=f"/dps/integration/data-products/v1/data-product/{product_id}/version/{version_id}/",
            body=payload,
        )
        return DataProduct.from_api_response(response)

    def delete_data_product_version(self, product_id: str, version_id: str) -> JobDetails:
        """Delete a specific data product version."""

        self._validate_identifier(product_id, "product_id")
        self._validate_identifier(version_id, "version_id")

        LOGGER.info("Deleting data product '%s' version '%s'.", product_id, version_id)
        response = self.delete(
            url=f"/dps/integration/data-products/v1/data-product/{product_id}/version/{version_id}/",
        )
        return JobDetails.from_api_response(response)

    def get_data_product_report_results(
        self,
        product_id: str,
        query_params: DataProductReportResultsParams = None,
    ) -> list[ProductReportResultRead]:
        """Retrieve report results for a single data product."""

        self._validate_identifier(product_id, "product_id")
        validate_query_params(query_params, DataProductReportResultsParams)
        params = query_params.generate_params_dict() if query_params else None

        LOGGER.info("Fetching report results for data product '%s'.", product_id)
        response = self.get(
            url=f"/dps/integration/data-products/v1/data-product/{product_id}/report-results/",
            query_params=params,
            pagination=False,
        )

        if response:
            return [ProductReportResultRead.from_api_response(item) for item in response]
        return []

    def log_data_product_report_results(
        self,
        product_id: str,
        report_results: list[ProductReportResult],
    ) -> JobDetails:
        """Log report results for a single data product."""

        self._validate_identifier(product_id, "product_id")
        if not report_results:
            raise InvalidPostBody("'report_results' is required for the Data Products request.")

        validate_rest_payload(payload=report_results, expected_types=(ProductReportResult,))
        payload = [item.generate_api_payload() for item in report_results]

        LOGGER.info("Logging %s report result(s) for data product '%s'.", len(report_results), product_id)
        response = self.post(
            url=f"/dps/integration/data-products/v1/data-product/{product_id}/report-results/",
            body=payload,
        )
        mapped_response = self._map_request_success_to_job_details(response if response else None)
        return JobDetails.from_api_response(mapped_response)

    def get_data_marketplaces(
        self,
        query_params: DataMarketplaceParams = None,
    ) -> list[DataMarketplace]:
        """Retrieve data marketplaces."""

        validate_query_params(query_params, DataMarketplaceParams)
        params = query_params.generate_params_dict() if query_params else None
        paginate = self._paginate_when_unbounded(query_params)

        LOGGER.info("Fetching data marketplaces.")
        response = self.get(
            url="/dps/integration/data-products/v1/marketplace/",
            query_params=params,
            pagination=paginate,
        )

        if response:
            return [DataMarketplace.from_api_response(item) for item in response]
        return []

    def create_data_marketplace(
        self,
        marketplace_spec: DataMarketplaceSpec | dict[str, Any] | str,
    ) -> DataMarketplace:
        """Create a data marketplace from a typed spec, raw dict, or YAML string."""

        payload, headers = self._prepare_spec_payload(
            spec_payload=marketplace_spec,
            expected_type=DataMarketplaceSpec,
            payload_name="marketplace_spec",
        )

        LOGGER.info("Creating a data marketplace.")
        response = self.post(
            url="/dps/integration/data-products/v1/marketplace/",
            body=payload,
            headers=headers,
        )
        return DataMarketplace.from_api_response(response)

    def update_data_marketplace(
        self,
        marketplace_spec: DataMarketplaceSpec | dict[str, Any] | str,
    ) -> DataMarketplace:
        """Update a data marketplace from a typed spec, raw dict, or YAML string."""

        payload, headers = self._prepare_spec_payload(
            spec_payload=marketplace_spec,
            expected_type=DataMarketplaceSpec,
            payload_name="marketplace_spec",
        )

        LOGGER.info("Updating a data marketplace.")
        response = self.put(
            url="/dps/integration/data-products/v1/marketplace/",
            body=payload,
            headers=headers,
        )
        return DataMarketplace.from_api_response(response)

    def get_data_marketplace(
        self,
        marketplace_id: str,
        query_params: DataMarketplaceParams = None,
    ) -> DataMarketplace:
        """Retrieve a specific data marketplace."""

        self._validate_identifier(marketplace_id, "marketplace_id")
        validate_query_params(query_params, DataMarketplaceParams)
        params = query_params.generate_params_dict() if query_params else None

        LOGGER.info("Fetching data marketplace '%s'.", marketplace_id)
        response = self.get(
            url=f"/dps/integration/data-products/v1/marketplace/{marketplace_id}/",
            query_params=params,
            pagination=False,
        )
        return DataMarketplace.from_api_response(response)

    def delete_data_marketplace(self, marketplace_id: str) -> JobDetails:
        """Delete a specific data marketplace."""

        self._validate_identifier(marketplace_id, "marketplace_id")

        LOGGER.info("Deleting data marketplace '%s'.", marketplace_id)
        response = self.delete(
            url=f"/dps/integration/data-products/v1/marketplace/{marketplace_id}/",
        )
        return JobDetails.from_api_response(response)

    def get_published_data_products(
        self,
        marketplace_id: str,
        query_params: PublishedDataProductParams = None,
    ) -> list[DataProductWithMarketplaceInfo]:
        """Retrieve data products published in a marketplace."""

        self._validate_identifier(marketplace_id, "marketplace_id")
        validate_query_params(query_params, PublishedDataProductParams)
        params = query_params.generate_params_dict() if query_params else None
        paginate = self._paginate_when_unbounded(query_params)

        LOGGER.info("Fetching published data products for marketplace '%s'.", marketplace_id)
        response = self.get(
            url=f"/dps/integration/data-products/v1/marketplace/{marketplace_id}/data-product/",
            query_params=params,
            pagination=paginate,
        )

        if response:
            return [DataProductWithMarketplaceInfo.from_api_response(item) for item in response]
        return []

    def get_published_data_product(
        self,
        marketplace_id: str,
        product_id: str,
    ) -> DataProductWithMarketplaceInfo:
        """Retrieve a specific published data product from a marketplace."""

        self._validate_identifier(marketplace_id, "marketplace_id")
        self._validate_identifier(product_id, "product_id")

        LOGGER.info(
            "Fetching published data product '%s' from marketplace '%s'.",
            product_id,
            marketplace_id,
        )
        response = self.get(
            url=f"/dps/integration/data-products/v1/marketplace/{marketplace_id}/data-product/{product_id}/",
            pagination=False,
        )
        return DataProductWithMarketplaceInfo.from_api_response(response)

    def publish_data_product(
        self,
        marketplace_id: str,
        product_id: str,
        query_params: DataProductPublishParams = None,
    ) -> DataProduct:
        """Publish a data product into a marketplace."""

        self._validate_identifier(marketplace_id, "marketplace_id")
        self._validate_identifier(product_id, "product_id")
        validate_query_params(query_params, DataProductPublishParams)
        params = query_params.generate_params_dict() if query_params else None

        LOGGER.info("Publishing data product '%s' into marketplace '%s'.", product_id, marketplace_id)
        response = self.post(
            url=f"/dps/integration/data-products/v1/marketplace/{marketplace_id}/data-product/{product_id}/",
            body={},
            query_params=params,
        )
        return DataProduct.from_api_response(response)

    def update_published_data_product(
        self,
        marketplace_id: str,
        product_id: str,
        query_params: DataProductPublishParams = None,
    ) -> DataProduct:
        """Update the published version of a data product in a marketplace."""

        self._validate_identifier(marketplace_id, "marketplace_id")
        self._validate_identifier(product_id, "product_id")
        validate_query_params(query_params, DataProductPublishParams)
        params = query_params.generate_params_dict() if query_params else None

        LOGGER.info(
            "Updating published data product '%s' in marketplace '%s'.",
            product_id,
            marketplace_id,
        )
        response = self.put(
            url=f"/dps/integration/data-products/v1/marketplace/{marketplace_id}/data-product/{product_id}/",
            body={},
            query_params=params,
        )
        return DataProduct.from_api_response(response)

    def unpublish_data_product(self, marketplace_id: str, product_id: str) -> JobDetails:
        """Remove a data product from a marketplace."""

        self._validate_identifier(marketplace_id, "marketplace_id")
        self._validate_identifier(product_id, "product_id")

        LOGGER.info("Unpublishing data product '%s' from marketplace '%s'.", product_id, marketplace_id)
        response = self.delete(
            url=f"/dps/integration/data-products/v1/marketplace/{marketplace_id}/data-product/{product_id}/",
        )
        return JobDetails.from_api_response(response)

    def bulk_publish_data_products(
        self,
        marketplace_id: str,
        bulk_publish_info: BulkPublishInfo,
    ) -> list[DataProduct]:
        """Bulk publish, update, or unpublish data products for a marketplace."""

        self._validate_identifier(marketplace_id, "marketplace_id")
        if bulk_publish_info is None:
            raise InvalidPostBody("'bulk_publish_info' is required for the Data Products request.")

        validate_rest_payload(payload=[bulk_publish_info], expected_types=(BulkPublishInfo,))
        payload = bulk_publish_info.generate_api_payload()

        LOGGER.info("Submitting bulk publish request for marketplace '%s'.", marketplace_id)
        response = self.post(
            url=f"/dps/integration/data-products/v1/marketplace/{marketplace_id}/bulk-publish/",
            body=payload,
        )

        if response:
            return [DataProduct.from_api_response(item) for item in response]
        return []

    def check_data_product(self, data_product_check: DataProductCheck) -> list[DataProductCheckResultItem]:
        """Check a data product spec against a list of standards."""

        if data_product_check is None:
            raise InvalidPostBody("'data_product_check' is required for the Data Products request.")

        validate_rest_payload(payload=[data_product_check], expected_types=(DataProductCheck,))
        payload = data_product_check.generate_api_payload()

        LOGGER.info("Checking data product against supplied standards.")
        response = self.post(
            url="/dps/integration/data-products/v1/data-product-check/",
            body=payload,
        )

        if response:
            return [DataProductCheckResultItem.from_api_response(item) for item in response]
        return []

    def get_report_results(
        self,
        query_params: ReportResultsParams = None,
    ) -> list[ReportResultRead]:
        """Retrieve report results across all data products."""

        validate_query_params(query_params, ReportResultsParams)
        params = query_params.generate_params_dict() if query_params else None

        LOGGER.info("Fetching report results across data products.")
        response = self.get(
            url="/dps/integration/data-products/v1/report-results/",
            query_params=params,
            pagination=False,
        )

        if response:
            return [ReportResultRead.from_api_response(item) for item in response]
        return []

    def log_report_results(self, report_results: list[ReportResult]) -> JobDetails:
        """Log report results across multiple data products."""

        if not report_results:
            raise InvalidPostBody("'report_results' is required for the Data Products request.")

        validate_rest_payload(payload=report_results, expected_types=(ReportResult,))
        payload = [item.generate_api_payload() for item in report_results]

        LOGGER.info("Logging %s cross-product report result(s).", len(report_results))
        response = self.post(
            url="/dps/integration/data-products/v1/report-results/",
            body=payload,
        )
        mapped_response = self._map_request_success_to_job_details(response if response else None)
        return JobDetails.from_api_response(mapped_response)

    def search_data_products_in_marketplace(
        self,
        marketplace_id: str,
        search_query: DataProductSearchQuery,
    ) -> list[DataProductWithMarketplaceInfo]:
        """Search data products inside a marketplace using a natural-language query."""

        self._validate_identifier(marketplace_id, "marketplace_id")
        if search_query is None:
            raise InvalidPostBody("'search_query' is required for the Data Products request.")

        validate_rest_payload(payload=[search_query], expected_types=(DataProductSearchQuery,))
        payload = search_query.generate_api_payload()

        LOGGER.info("Searching data products inside marketplace '%s'.", marketplace_id)
        response = self.post(
            url=f"/dps/integration/data-products/v1/search-internally/{marketplace_id}/",
            body=payload,
        )

        if response:
            return [DataProductWithMarketplaceInfo.from_api_response(item) for item in response]
        return []

    def get_permissions(
        self,
        query_params: DataProductPermissionParams = None,
    ) -> list[DataProductPermission]:
        """Retrieve permissions configured for the Data Products application."""

        validate_query_params(query_params, DataProductPermissionParams)
        params = query_params.generate_params_dict() if query_params else None

        LOGGER.info("Fetching data product permissions.")
        response = self.get(
            url="/dps/integration/data-products/v1/data-products/permissions/",
            query_params=params,
            pagination=False,
        )

        if response:
            return [DataProductPermission.from_api_response(item) for item in response]
        return []

    def create_permission(self, permission: DataProductPermission) -> JobDetails:
        """Create a data products permission."""

        if permission is None:
            raise InvalidPostBody("'permission' is required for the Data Products request.")

        validate_rest_payload(payload=[permission], expected_types=(DataProductPermission,))
        payload = permission.generate_api_payload()

        LOGGER.info("Creating a data product permission.")
        response = self.post(
            url="/dps/integration/data-products/v1/data-products/permissions/",
            body=payload,
        )
        mapped_response = self._map_request_success_to_job_details(response if response else None)
        return JobDetails.from_api_response(mapped_response)

    def update_permission(self, permission: DataProductPermission) -> JobDetails:
        """Update a data products permission."""

        if permission is None:
            raise InvalidPostBody("'permission' is required for the Data Products request.")

        validate_rest_payload(payload=[permission], expected_types=(DataProductPermission,))
        payload = permission.generate_api_payload()

        LOGGER.info("Updating a data product permission.")
        response = self.put(
            url="/dps/integration/data-products/v1/data-products/permissions/",
            body=payload,
        )
        mapped_response = self._map_request_success_to_job_details(response if response else None)
        return JobDetails.from_api_response(mapped_response)

    def delete_permission(self, permission: DataProductPermission) -> JobDetails:
        """Delete a data products permission."""

        if permission is None:
            raise InvalidPostBody("'permission' is required for the Data Products request.")

        validate_rest_payload(payload=[permission], expected_types=(DataProductPermission,))
        payload = permission.generate_api_payload()

        LOGGER.info("Deleting a data product permission.")
        response = self.delete(
            url="/dps/integration/data-products/v1/data-products/permissions/",
            body=payload,
        )
        return JobDetails.from_api_response(response)

    def get_user_permissions(self) -> list[DataProductPermission]:
        """Retrieve effective permissions for the authenticated user."""

        LOGGER.info("Fetching effective data product permissions for the authenticated user.")
        response = self.get(
            url="/dps/integration/data-products/v1/data-products/check-permissions/",
            pagination=False,
        )

        if response:
            return [DataProductPermission.from_api_response(item) for item in response]
        return []
